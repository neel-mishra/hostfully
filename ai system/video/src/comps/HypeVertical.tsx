import {AbsoluteFill, interpolate, useCurrentFrame} from 'remotion';
import {useFastPan, useHeroZoom} from './animations';
import {default20sStoryboard} from '../storyboard/default20s';
import {useStoryboardBeat} from '../storyboard/useStoryboardBeat';
import {HostfullyAppMock} from '../ui/HostfullyAppMock';

export const HypeVertical: React.FC = () => {
  const frame = useCurrentFrame();
  const beat = useStoryboardBeat(default20sStoryboard);
  const zoom = useHeroZoom();
  const pan = useFastPan();

  const globalFade = interpolate(frame, [0, 8, 24], [0, 1, 1], {
    extrapolateRight: 'clamp',
  });
  const sceneOpacity = beat ? 1 : 0.5;

  const motionStyle = beat?.motionStyle;
  const isZoom =
    motionStyle === 'hero-zoom' || motionStyle === 'count-up' || motionStyle === 'type-on';
  const isPan = motionStyle === 'fast-pan' || motionStyle === 'wipe';

  const motionScale = isZoom ? zoom.scale : 1;
  const translateX = isPan ? pan.translateX : 0;

  const headline =
    beat?.copy ?? 'Keep up with tech in five minutes. Free forever.';

  const scene =
    beat?.scene === 'hook' ||
    beat?.scene === 'demo' ||
    beat?.scene === 'proof' ||
    beat?.scene === 'payoff' ||
    beat?.scene === 'cta'
      ? beat.scene
      : 'hook';

  return (
    <AbsoluteFill
      style={{
        background: 'linear-gradient(180deg, #020617, #0f172a)',
        color: 'white',
        justifyContent: 'center',
        alignItems: 'center',
        fontFamily: 'system-ui, -apple-system, BlinkMacSystemFont, sans-serif',
      }}
    >
      <div
        style={{
          width: '100%',
          height: '100%',
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          justifyContent: 'center',
          gap: 30,
          transform: `translateX(${translateX}px) scale(${motionScale})`,
          opacity: globalFade * sceneOpacity,
        }}
      >
        <HostfullyAppMock scene={scene} headline={headline} uiState={beat?.uiState} />
        <div style={{fontSize: 22, letterSpacing: 2, textTransform: 'uppercase', opacity: 0.8}}>
          {beat?.scene === 'proof' ? 'Proof, not fluff' : 'Signal over noise'}
        </div>
        <div style={{fontSize: 38, fontWeight: 700, lineHeight: 1.1, maxWidth: 900, textAlign: 'center'}}>
          {beat?.scene === 'cta'
            ? 'Join the 1.6M+ readers who start smarter every morning.'
            : 'Curated tech intelligence that respects your time.'}
        </div>
      </div>
    </AbsoluteFill>
  );
};

