import type {Storyboard} from './schema';

const FPS = 30;
const TOTAL_SECONDS = 20;

export const default20sStoryboard: Storyboard = {
  fps: FPS,
  totalFrames: TOTAL_SECONDS * FPS,
  beats: [
    {
      id: 'hook-macro-zoom',
      startFrame: 0,
      durationFrames: 2 * FPS,
      scene: 'hook',
      copy: 'News that actually moves the needle.',
      uiState: 'hero_dashboard_zoomed_out',
      motionStyle: 'hero-zoom',
      sfx: 'whoosh_soft',
      musicCue: 'intro_hit',
    },
    {
      id: 'demo-search',
      startFrame: 2 * FPS,
      durationFrames: 3 * FPS,
      scene: 'demo',
      copy: 'Ask one question. Get the signal, not the noise.',
      uiState: 'search_results_focus',
      motionStyle: 'fast-pan',
    },
    {
      id: 'demo-save-share',
      startFrame: 5 * FPS,
      durationFrames: 3 * FPS,
      scene: 'demo',
      copy: 'Save, brief, and share in one click.',
      uiState: 'brief_view_with_sharing',
      motionStyle: 'wipe',
    },
    {
      id: 'proof-metrics',
      startFrame: 8 * FPS,
      durationFrames: 3 * FPS,
      scene: 'proof',
      copy: 'Teams cut report prep from hours to minutes.',
      uiState: 'metrics_before_after',
      motionStyle: 'count-up',
    },
    {
      id: 'payoff-montage',
      startFrame: 11 * FPS,
      durationFrames: 3 * FPS,
      scene: 'payoff',
      copy: 'From “what happened?” to “what should we do?”',
      uiState: 'multi_screen_montage',
      motionStyle: 'fast-pan',
    },
    {
      id: 'cta',
      startFrame: 14 * FPS,
      durationFrames: 6 * FPS,
      scene: 'cta',
      copy: 'Hostfully: News that ships work, not hot takes.',
      uiState: 'logo_lockup',
      motionStyle: 'hero-zoom',
      musicCue: 'outro_hit',
    },
  ],
};

