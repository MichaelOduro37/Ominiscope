export default function Reports() {
  return (
    <section className="page">
      <div className="hero">
        <div>
          <h1>Report Library</h1>
          <p>Evidence-backed decisions with traceable provenance.</p>
        </div>
        <div className="hero-panel">
          <div className="hero-label">Reports Ready</div>
          <div className="hero-value">28</div>
          <div className="hero-meta">6 pending review</div>
        </div>
      </div>
      <div className="grid">
        <article className="card">
          <h3>Operational Review</h3>
          <p>Root cause analysis for turbine A vibration spike.</p>
          <div className="tags">
            <span className="tag">engineering</span>
            <span className="tag">approved</span>
          </div>
        </article>
        <article className="card">
          <h3>Supplier Risk</h3>
          <p>Cross-domain procurement anomaly detection.</p>
          <div className="tags">
            <span className="tag">finance</span>
            <span className="tag">pending</span>
          </div>
        </article>
        <article className="card">
          <h3>Compliance Snapshot</h3>
          <p>Quarterly audit trail verification.</p>
          <div className="tags">
            <span className="tag">security</span>
            <span className="tag">ready</span>
          </div>
        </article>
      </div>
    </section>
  );
}
