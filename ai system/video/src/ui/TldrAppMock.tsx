import type {CSSProperties} from 'react';
import {tldrBrand} from './tldrBrand';
import {UiFrame} from './UiFrame';

type SceneKey = 'hook' | 'demo' | 'proof' | 'payoff' | 'cta';

type TldrAppMockProps = {
  scene: SceneKey;
  headline: string;
};

const cardStyle: CSSProperties = {
  border: `1px solid ${tldrBrand.palette.border}`,
  borderRadius: 18,
  backgroundColor: tldrBrand.palette.panelSoft,
  padding: 20,
};

const StatCard = ({label, value}: {label: string; value: string}) => {
  return (
    <div style={{...cardStyle, minWidth: 0}}>
      <div style={{fontSize: 18, color: tldrBrand.palette.textSecondary}}>{label}</div>
      <div style={{fontSize: 34, color: tldrBrand.palette.textPrimary, marginTop: 6, fontWeight: 700}}>
        {value}
      </div>
    </div>
  );
};

export const TldrAppMock = ({scene, headline}: TldrAppMockProps) => {
  const hero = scene === 'hook' || scene === 'cta';
  const showMetrics = scene === 'proof' || scene === 'payoff';

  return (
    <UiFrame>
      <div
        style={{
          display: 'flex',
          flexDirection: 'column',
          height: '100%',
          background: `linear-gradient(180deg, ${tldrBrand.palette.bg}, ${tldrBrand.palette.panel})`,
        }}
      >
        <div
          style={{
            borderBottom: `1px solid ${tldrBrand.palette.border}`,
            padding: '20px 24px',
            display: 'flex',
            justifyContent: 'space-between',
            alignItems: 'center',
          }}
        >
          <div style={{fontSize: 34, color: tldrBrand.palette.textPrimary, fontWeight: 700}}>TLDR</div>
          <div style={{fontSize: 16, color: tldrBrand.palette.textSecondary}}>Daily Tech Briefing</div>
        </div>

        <div style={{padding: 24, display: 'flex', flexDirection: 'column', gap: 18, flex: 1}}>
          <div
            style={{
              ...cardStyle,
              backgroundColor: hero ? '#082f49' : tldrBrand.palette.panelSoft,
              borderColor: hero ? tldrBrand.palette.accentStrong : tldrBrand.palette.border,
            }}
          >
            <div style={{fontSize: 16, color: tldrBrand.palette.accent, textTransform: 'uppercase', letterSpacing: 1.4}}>
              {tldrBrand.tagline}
            </div>
            <div style={{fontSize: 44, color: tldrBrand.palette.textPrimary, lineHeight: 1.1, marginTop: 10, fontWeight: 700}}>
              {headline}
            </div>
          </div>

          <div style={cardStyle}>
            <div style={{fontSize: 19, color: tldrBrand.palette.textSecondary, marginBottom: 10}}>Today&apos;s high-signal stories</div>
            <div style={{display: 'grid', gap: 10}}>
              <div style={{fontSize: 24, color: tldrBrand.palette.textPrimary}}>AI releases that actually matter for builders</div>
              <div style={{fontSize: 24, color: tldrBrand.palette.textPrimary}}>Cloud pricing shift every CTO should catch</div>
              <div style={{fontSize: 24, color: tldrBrand.palette.textPrimary}}>Dev tool launch with immediate workflow upside</div>
            </div>
          </div>

          {showMetrics ? (
            <div style={{display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 12}}>
              <StatCard label="Reader trust" value={tldrBrand.readerProof.openRate} />
              <StatCard label="Daily read time" value={tldrBrand.readerProof.readTime} />
              <StatCard label="Audience" value={tldrBrand.advertiserProof.networkReach} />
              <StatCard label="Paid social delta" value={tldrBrand.advertiserProof.cpcDeltaVsLinkedIn} />
            </div>
          ) : null}
        </div>
      </div>
    </UiFrame>
  );
};

