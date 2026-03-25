import {Composition} from 'remotion';
import {HypeVertical} from './comps/HypeVertical';
import {HypeHorizontal} from './comps/HypeHorizontal';
import {UiParityHarness} from './comps/UiParityHarness';

export const RemotionRoot: React.FC = () => {
  return (
    <>
      <Composition
        id="HypeVertical-9x16"
        component={HypeVertical}
        durationInFrames={20 * 30}
        fps={30}
        width={1080}
        height={1920}
      />
      <Composition
        id="HypeHorizontal-16x9"
        component={HypeHorizontal}
        durationInFrames={20 * 30}
        fps={30}
        width={1920}
        height={1080}
      />
      <Composition
        id="UiParityHarness"
        component={UiParityHarness}
        durationInFrames={5 * 30}
        fps={30}
        width={1080}
        height={1920}
      />
    </>
  );
};

