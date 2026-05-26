export default function Dashboard() {
  return (
    <section className="page">
      <div className="hero">
        <div>
          <h1>Enterprise Pulse</h1>
          <p>
            A real-time snapshot of cross-domain operations, active pipelines, and
            decision readiness.
          </p>
        </div>
        <div className="hero-panel">
          <div className="hero-label">Active Pipelines</div>
          <div className="hero-value">12</div>
          <div className="hero-meta">2 awaiting approval</div>
        </div>
      </div>
      <div className="grid">
        <article className="card">
          <h3>Ingestion Health</h3>
          <p>96 assets ingested today · 4 flagged for metadata gaps.</p>
          <div className="meter">
            <span style={{ width: "86%" }} />
          </div>
        </article>
        <article className="card">
          <h3>Risk Watch</h3>
          <p>3 high-risk analyses paused for Security approval.</p>
          <div className="tags">
            <span className="tag">compliance</span>
            <span className="tag">regulatory</span>
          </div>
        </article>
        <article className="card">
          <h3>Decision Ledger</h3>
          <p>42 decisions recorded this week · 100% provenance complete.</p>
          <div className="chip">Immutable</div>
        </article>
      </div>
    </section>
  );
}
