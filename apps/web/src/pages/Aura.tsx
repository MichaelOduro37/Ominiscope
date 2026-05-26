export default function Aura() {
  return (
    <section className="page">
      <div className="hero">
        <div>
          <h1>AURA Command Deck</h1>
          <p>
            Translate questions into pipelines with explicit assumptions,
            evidence, and approval gates.
          </p>
        </div>
        <div className="hero-panel">
          <div className="hero-label">Confidence</div>
          <div className="hero-value">0.82</div>
          <div className="hero-meta">Based on last 30 runs</div>
        </div>
      </div>
      <div className="grid">
        <article className="card">
          <h3>Goal Input</h3>
          <p>Describe the question, attach data, and set constraints.</p>
          <div className="ghost-block">"Why did turbine A spike at 2.3 Hz?"</div>
        </article>
        <article className="card">
          <h3>Pipeline Preview</h3>
          <ul className="list">
            <li>Ingest vibration logs</li>
            <li>Run spectral analysis</li>
            <li>Cross-check maintenance records</li>
          </ul>
        </article>
        <article className="card">
          <h3>Approval Gate</h3>
          <p>High-risk actions require Security sign-off.</p>
          <div className="chip">Awaiting approval</div>
        </article>
      </div>
    </section>
  );
}
