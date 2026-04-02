import os


def run_team_social_drafts() -> None:
    # Backward-compatible entrypoint routed to unified orchestrator.
    from social_agent_orchestrator import run_social_agent  # type: ignore

    run_social_agent(
        mode="daily",
        input_mode=os.getenv("SOCIAL_INPUT_MODE", "brief_only"),  # type: ignore[arg-type]
        strictness=os.getenv("SOCIAL_STRICTNESS", "balanced"),  # type: ignore[arg-type]
        channels=[c.strip() for c in os.getenv("SOCIAL_CHANNELS", "linkedin").split(",") if c.strip()],  # type: ignore[list-item]
    )


if __name__ == "__main__":
    run_team_social_drafts()

