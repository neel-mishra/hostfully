import {AbsoluteFill} from 'remotion';

export const UiParityHarness: React.FC = () => {
  return (
    <AbsoluteFill
      style={{
        background: '#020617',
        color: 'white',
        justifyContent: 'center',
        alignItems: 'center',
        fontFamily: 'system-ui, -apple-system, BlinkMacSystemFont, sans-serif',
      }}
    >
      <div style={{textAlign: 'center', maxWidth: 600, padding: 32}}>
        <div style={{fontSize: 24, marginBottom: 8}}>UI Parity Harness</div>
        <div style={{fontSize: 16, opacity: 0.8}}>
          Drop your real app UI wrappers here and overlay screenshots to chase pixel-perfect parity.
        </div>
      </div>
    </AbsoluteFill>
  );
};

