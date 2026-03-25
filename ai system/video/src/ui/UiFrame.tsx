import type {ReactNode} from 'react';

type UiFrameProps = {
  children: ReactNode;
};

export const UiFrame = ({children}: UiFrameProps) => {
  return (
    <div
      style={{
        width: 900,
        height: 1600,
        borderRadius: 40,
        overflow: 'hidden',
        border: '2px solid rgba(148, 163, 184, 0.4)',
        boxShadow: '0 40px 120px rgba(15, 23, 42, 0.9)',
        backgroundColor: '#020617',
        display: 'flex',
        flexDirection: 'column',
      }}
    >
      {children}
    </div>
  );
};

