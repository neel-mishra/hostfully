interface RateLimitConfig {
  maxScore: number;
  decayTimeMs: number;
  blockTimeMs: number;
  readCallScore: number;
  writeCallScore: number;
}

interface RateLimitState {
  currentScore: number;
  lastDecayTime: number;
  isBlocked: boolean;
  blockUntil: number;
}

export class RateLimiter {
  private config: RateLimitConfig;
  private accountStates: Map<string, RateLimitState> = new Map();

  constructor(isDevelopmentTier: boolean = false) {
    this.config = isDevelopmentTier
      ? {
          maxScore: 60,
          decayTimeMs: 300000,
          blockTimeMs: 300000,
          readCallScore: 1,
          writeCallScore: 3,
        }
      : {
          maxScore: 9000,
          decayTimeMs: 300000,
          blockTimeMs: 60000,
          readCallScore: 1,
          writeCallScore: 3,
        };
  }

  private getAccountState(accountId: string): RateLimitState {
    if (!this.accountStates.has(accountId)) {
      this.accountStates.set(accountId, {
        currentScore: 0,
        lastDecayTime: Date.now(),
        isBlocked: false,
        blockUntil: 0,
      });
    }
    return this.accountStates.get(accountId)!;
  }

  private updateScore(accountId: string): void {
    const state = this.getAccountState(accountId);
    const now = Date.now();

    const timeSinceLastDecay = now - state.lastDecayTime;
    const decayPeriods = Math.floor(timeSinceLastDecay / this.config.decayTimeMs);

    if (decayPeriods > 0) {
      state.currentScore = Math.max(0, state.currentScore * Math.pow(0.5, decayPeriods));
      state.lastDecayTime = now;
    }

    if (state.isBlocked && now >= state.blockUntil) {
      state.isBlocked = false;
      state.blockUntil = 0;
    }
  }

  async checkRateLimit(accountId: string, isWriteCall: boolean = false): Promise<void> {
    this.updateScore(accountId);
    const state = this.getAccountState(accountId);

    if (state.isBlocked) {
      const waitTime = Math.max(0, state.blockUntil - Date.now());
      throw new RateLimitError(
        `Rate limit exceeded for account ${accountId}. Please wait ${Math.ceil(waitTime / 1000)} seconds.`,
        waitTime,
      );
    }

    const callScore = isWriteCall ? this.config.writeCallScore : this.config.readCallScore;

    if (state.currentScore + callScore > this.config.maxScore) {
      state.isBlocked = true;
      state.blockUntil = Date.now() + this.config.blockTimeMs;

      throw new RateLimitError(
        `Rate limit exceeded for account ${accountId}. Blocked for ${this.config.blockTimeMs / 1000} seconds.`,
        this.config.blockTimeMs,
      );
    }

    state.currentScore += callScore;
  }

  getCurrentScore(accountId: string): number {
    this.updateScore(accountId);
    return this.getAccountState(accountId).currentScore;
  }

  getRemainingCapacity(accountId: string): number {
    this.updateScore(accountId);
    const state = this.getAccountState(accountId);
    return Math.max(0, this.config.maxScore - state.currentScore);
  }

  isAccountBlocked(accountId: string): boolean {
    this.updateScore(accountId);
    return this.getAccountState(accountId).isBlocked;
  }

  getBlockTimeRemaining(accountId: string): number {
    this.updateScore(accountId);
    const state = this.getAccountState(accountId);
    if (!state.isBlocked) return 0;
    return Math.max(0, state.blockUntil - Date.now());
  }

  async waitForCapacity(accountId: string, requiredScore: number = 1): Promise<void> {
    const maxWaitTime = 60000;
    const pollInterval = 1000;
    let waitTime = 0;

    while (waitTime < maxWaitTime) {
      this.updateScore(accountId);
      const state = this.getAccountState(accountId);

      if (!state.isBlocked && state.currentScore + requiredScore <= this.config.maxScore) {
        return;
      }

      if (state.isBlocked) {
        const blockTimeRemaining = this.getBlockTimeRemaining(accountId);
        if (blockTimeRemaining > maxWaitTime - waitTime) {
          throw new RateLimitError(
            `Rate limit block time (${Math.ceil(blockTimeRemaining / 1000)}s) exceeds maximum wait time`,
            blockTimeRemaining,
          );
        }
      }

      await new Promise((resolve) => setTimeout(resolve, pollInterval));
      waitTime += pollInterval;
    }

    throw new RateLimitError(
      `Could not acquire rate limit capacity after ${maxWaitTime / 1000} seconds`,
      0,
    );
  }
}

export class RateLimitError extends Error {
  constructor(message: string, public readonly retryAfterMs: number) {
    super(message);
    this.name = "RateLimitError";
  }
}

export const globalRateLimiter = new RateLimiter(process.env.META_API_TIER === "development");

