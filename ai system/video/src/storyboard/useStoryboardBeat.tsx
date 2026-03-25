import {useCurrentFrame} from 'remotion';
import type {StoryboardBeat, Storyboard} from './schema';

export const useStoryboardBeat = (storyboard: Storyboard): StoryboardBeat | null => {
  const frame = useCurrentFrame();
  return (
    storyboard.beats.find(
      (beat) => frame >= beat.startFrame && frame < beat.startFrame + beat.durationFrames,
    ) ?? null
  );
};

