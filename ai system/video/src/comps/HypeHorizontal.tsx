import {AbsoluteFill} from 'remotion';

export const HypeHorizontal: React.FC = () => {
  return (
    <AbsoluteFill
      style={{
        background: 'black',
        color: 'white',
        justifyContent: 'center',
        alignItems: 'center',
        fontFamily: 'system-ui, -apple-system, BlinkMacSystemFont, sans-serif',
      }}
    >
      <div style={{fontSize: 40, fontWeight: 600}}>Horizontal hype variant (stub)</div>
    </AbsoluteFill>
  );
};

