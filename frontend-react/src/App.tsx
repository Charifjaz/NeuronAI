import { useEffect, useState } from "react";
import "./theme.css";
import Profile from "./components/Profile";
import Chat from "./components/Chat";
import { QA } from "./type";

export default function App() {
  const [validated, setValidated] = useState(false);
  const [answers, setAnswers] = useState<QA>({});
  const [apiBase, setApiBase] = useState(
    (import.meta.env.VITE_API_BASE_URL as string) || "http://localhost:8000"
  );

  // restaurer le profil validé si présent
  useEffect(() => {
    const saved = localStorage.getItem("answers_validated");
    if (saved) {
      try {
        setAnswers(JSON.parse(saved));
        setValidated(true);
      } catch {}
    }
  }, []);

  return (
    <div className="app">
      <div>
        <header className="card" style={{ textAlign: "center" }}>
          <h1 style={{ margin: 0,
            background: "linear-gradient(90deg,#8b5cf6,#6366f1,#8b5cf6)",
            WebkitBackgroundClip: "text", color: "transparent",
            backgroundSize: "200% auto", animation: "shine 3s linear infinite"
          }}>
            🧠 Neural Chat Interface
          </h1>
          <p style={{ color: "#94a3b8", marginTop: 6 }}>
            Intelligence conversationnelle avec profil contextuel
          </p>
        </header>

        <Chat answers={answers} validated={validated} />
        <div className="footer">🔒 Session en mémoire · Aucune donnée persistée · Alimenté par l'API backend</div>
      </div>

      <aside style={{ display: "flex", flexDirection: "column", gap: 12 }}>
        <div className="card">
          <h3>⚙️ Configuration</h3>
          <label>🔗 API Base URL</label>
          <input className="input" value={apiBase}
            onChange={(e) => setApiBase(e.target.value)} />
          <small style={{ color:"#94a3b8" }}>
            Actuelle: {apiBase}
          </small>
        </div>
        <Profile
          validated={validated}
          answers={answers}
          setAnswers={setAnswers}
          setValidated={setValidated}
        />
      </aside>
    </div>
  );
}
