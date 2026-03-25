import {interpolate, useCurrentFrame, useVideoConfig} from 'remotion';

type PresetProps = {
  from?: number;
  durationInFrames?: number;
};

export const useHeroZoom = ({from = 0, durationInFrames = 30}: PresetProps = {}) => {
  const frame = useCurrentFrame() - from;
  const scale = interpolate(frame, [0, durationInFrames], [1.15, 1], {
    extrapolateRight: 'clamp',
  });
  const opacity = interpolate(frame, [0, Math.min(10, durationInFrames)], [0, 1], {
    extrapolateRight: 'clamp',
  });
  return {scale, opacity};
};

export const useFastPan = ({from = 0, durationInFrames = 20}: PresetProps = {}) => {
  const frame = useCurrentFrame() - from;
  const translateX = interpolate(frame, [0, durationInFrames], [80, 0], {
    extrapolateRight: 'clamp',
  });
  const opacity = interpolate(frame, [0, 6], [0, 1], {
    extrapolateRight: 'clamp',
  });
  return {translateX, opacity};
};

export const useCountUp = ({
  from = 0,
  durationInFrames = 40,
  start = 0,
  end = 100,
}: PresetProps & {start?: number; end?: number} = {}) => {
  const frame = useCurrentFrame() - from;
  const {fps} = useVideoConfig();
  const value = interpolate(frame, [0, durationInFrames], [start, end], {
    extrapolateRight: 'clamp',
  });
  const rounded = Math.round(value / (fps / 10)) * (fps / 10);
  return {value: value < end ? rounded : end};
};

