import type {CSSProperties} from 'react';
import {hostfullyBrand} from './hostfullyBrand';
import {UiFrame} from './UiFrame';

type SceneKey = 'hook' | 'demo' | 'proof' | 'payoff' | 'cta';

type HostfullyAppMockProps = {
  scene: SceneKey;
  headline: string;
  uiState?: string;
};

const cardStyle: CSSProperties = {
  border: `1px solid ${hostfullyBrand.palette.border}`,
  borderRadius: 18,
  backgroundColor: hostfullyBrand.palette.panelSoft,
  padding: 20,
};

const StatCard = ({label, value}: {label: string; value: string}) => {
  return (
    <div style={{...cardStyle, minWidth: 0}}>
      <div style={{fontSize: 18, color: hostfullyBrand.palette.textSecondary}}>{label}</div>
      <div style={{fontSize: 34, color: hostfullyBrand.palette.textPrimary, marginTop: 6, fontWeight: 700}}>
        {value}
      </div>
    </div>
  );
};

export const HostfullyAppMock = ({scene, headline, uiState}: HostfullyAppMockProps) => {
  const hero = scene === 'hook' || scene === 'cta';
  const showMetrics = scene === 'proof' || scene === 'payoff';

  const showStoryList =
    uiState !== 'logo_lockup' && uiState !== 'metrics_before_after' && uiState !== 'multi_screen_montage';

  return (
    <UiFrame>
      <div
        style={{
          display: 'flex',
          flexDirection: 'column',
          height: '100%',
          background: `linear-gradient(180deg, ${hostfullyBrand.palette.bg}, ${hostfullyBrand.palette.panel})`,
        }}
      >
        <div
          style={{
            borderBottom: `1px solid ${hostfullyBrand.palette.border}`,
            padding: '20px 24px',
            display: 'flex',
            justifyContent: 'space-between',
            alignItems: 'center',
          }}
        >
          <div style={{fontSize: 34, color: hostfullyBrand.palette.textPrimary, fontWeight: 700}}>Hostfully</div>
          <div style={{fontSize: 16, color: hostfullyBrand.palette.textSecondary}}>Daily Tech Briefing</div>
        </div>

        <div style={{padding: 24, display: 'flex', flexDirection: 'column', gap: 18, flex: 1}}>
          <div
            style={{
              ...cardStyle,
              backgroundColor: hero ? '#082f49' : hostfullyBrand.palette.panelSoft,
              borderColor: hero ? hostfullyBrand.palette.accentStrong : hostfullyBrand.palette.border,
            }}
          >
            <div style={{fontSize: 16, color: hostfullyBrand.palette.accent, textTransform: 'uppercase', letterSpacing: 1.4}}>
              {hostfullyBrand.tagline}
            </div>
            <div style={{fontSize: 44, color: hostfullyBrand.palette.textPrimary, lineHeight: 1.1, marginTop: 10, fontWeight: 700}}>
              {headline}
            </div>
          </div>

          {showStoryList ? (
            <div style={cardStyle}>
              <div style={{fontSize: 19, color: hostfullyBrand.palette.textSecondary, marginBottom: 10}}>
                Today&apos;s high-signal stories
              </div>
              <div style={{display: 'grid', gap: 10}}>
                <div style={{fontSize: 24, color: hostfullyBrand.palette.textPrimary}}>
                  AI releases that actually matter for builders
                </div>
                <div style={{fontSize: 24, color: hostfullyBrand.palette.textPrimary}}>
                  Cloud pricing shift every CTO should catch
                </div>
                <div style={{fontSize: 24, color: hostfullyBrand.palette.textPrimary}}>
                  Dev tool launch with immediate workflow upside
                </div>
              </div>
            </div>
          ) : null}

          {showMetrics ? (
            <div style={{display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 12}}>
              <StatCard label="Reader trust" value={hostfullyBrand.readerProof.openRate} />
              <StatCard label="Daily read time" value={hostfullyBrand.readerProof.readTime} />
              <StatCard label="Audience" value={hostfullyBrand.advertiserProof.networkReach} />
              <StatCard label="Paid social delta" value={hostfullyBrand.advertiserProof.cpcDeltaVsLinkedIn} />
            </div>
          ) : null}
        </div>
      </div>
    </UiFrame>
  );
};
