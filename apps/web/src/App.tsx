import { NavLink, Route, Routes } from "react-router-dom";

import Aura from "./pages/Aura";
import Dashboard from "./pages/Dashboard";
import Reports from "./pages/Reports";

const navItems = [
  { label: "Dashboard", to: "/" },
  { label: "AURA", to: "/aura" },
  { label: "Reports", to: "/reports" }
];

export default function App() {
  return (
    <div className="app-shell">
      <aside className="side-rail">
        <div className="brand">
          <span className="brand-mark">O</span>
          <div>
            <div className="brand-title">OmniScope</div>
            <div className="brand-sub">Internal v1</div>
          </div>
        </div>
        <nav className="nav">
          {navItems.map((item) => (
            <NavLink
              key={item.to}
              to={item.to}
              end={item.to === "/"}
              className={({ isActive }) =>
                isActive ? "nav-link active" : "nav-link"
              }
            >
              {item.label}
            </NavLink>
          ))}
        </nav>
        <div className="rail-foot">
          <div className="chip">System Pulse</div>
          <div className="rail-metrics">All engines idle · 99.99%</div>
        </div>
      </aside>
      <main className="main-panel">
        <header className="top-bar">
          <div>
            <div className="top-title">OmniScope Operations</div>
            <div className="top-sub">Unified analysis workspace</div>
          </div>
          <div className="top-actions">
            <button className="ghost">New Pipeline</button>
            <button className="primary">Ask AURA</button>
          </div>
        </header>
        <div className="content">
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/aura" element={<Aura />} />
            <Route path="/reports" element={<Reports />} />
          </Routes>
        </div>
      </main>
    </div>
  );
}
