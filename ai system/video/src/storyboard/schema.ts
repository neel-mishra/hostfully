export type MotionStyle =
  | 'hero-zoom'
  | 'fast-pan'
  | 'wipe'
  | 'type-on'
  | 'count-up';

export type SceneId = 'hook' | 'demo' | 'proof' | 'payoff' | 'cta';

export type StoryboardBeat = {
  id: string;
  startFrame: number;
  durationFrames: number;
  scene: SceneId;
  copy: string;
  uiState: string;
  motionStyle: MotionStyle;
  sfx?: string;
  musicCue?: string;
};

export type Storyboard = {
  fps: number;
  totalFrames: number;
  beats: StoryboardBeat[];
};

