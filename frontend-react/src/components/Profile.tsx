import { useEffect, useMemo, useState } from "react";
import { fetchQuestions } from "../api";
import { QA, Question } from "../type";

type Props = {
  validated: boolean;
  answers: QA;
  setAnswers: (a: QA) => void;
  setValidated: (v: boolean) => void;
};

export default function Profile({ validated, answers, setAnswers, setValidated }: Props) {
  const [questions, setQuestions] = useState<Question[] | null>(null);

  useEffect(() => {
    fetchQuestions().then((qs) => {
      // init brouillon si vide
      if (!answers || Object.keys(answers).length === 0) {
        const init: QA = {};
        qs.forEach((q) => {
          if (q.default !== undefined) init[q.id] = q.default!;
          else if (q.type === "slider") {
            const mn = Number(q.scale_min ?? 0), mx = Number(q.scale_max ?? 10);
            init[q.id] = Math.floor((mn + mx) / 2);
          } else init[q.id] = "";
        });
        setAnswers(init);
      }
      setQuestions(qs);
    });
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  const preview = useMemo(() => {
    const lines = Object.entries(answers || {})
      .filter(([_, v]) => `${v ?? ""}`.trim() !== "")
      .map(([k, v]) => `- ${k}: ${v}`);
    return lines.length ? `Réponses validées (profil utilisateur):\n${lines.join("\n")}` : "";
  }, [answers]);

  if (!questions) return <div className="card">Chargement…</div>;

  if (!validated) {
    return (
      <div className="card">
        <h3>🎯 Profil contextuel</h3>
        <form
          onSubmit={(e) => {
            e.preventDefault();
            setValidated(true);
            localStorage.setItem("answers_validated", JSON.stringify(answers));
          }}
        >
          {questions.map((q) => {
            const id = q.id;
            const val = (answers?.[id] ?? "") as any;
            if (q.type === "textarea") {
              return (
                <div key={id} style={{ marginBottom: 12 }}>
                  <label>{q.label ?? id}</label>
                  <textarea
                    className="input"
                    rows={5}
                    placeholder={q.placeholder ?? ""}
                    value={val}
                    onChange={(e) => setAnswers({ ...answers, [id]: e.target.value })}
                  />
                </div>
              );
            }
            if (q.type === "slider") {
              const mn = Number(q.scale_min ?? 0), mx = Number(q.scale_max ?? 10);
              return (
                <div key={id} style={{ marginBottom: 12 }}>
                  <label>{q.label ?? id} ({val})</label>
                  <input
                    type="range" min={mn} max={mx} value={Number(val)}
                    onChange={(e) => setAnswers({ ...answers, [id]: Number(e.target.value) })}
                    style={{ width: "100%" }}
                  />
                </div>
              );
            }
            return (
              <div key={id} style={{ marginBottom: 12 }}>
                <label>{q.label ?? id}</label>
                <input
                  className="input"
                  placeholder={q.placeholder ?? ""}
                  value={val}
                  onChange={(e) => setAnswers({ ...answers, [id]: e.target.value })}
                />
              </div>
            );
          })}
          <button className="btn" type="submit" style={{ width: "100%", marginTop: 8 }}>
            🚀 Activer le profil
          </button>
        </form>
      </div>
    );
  }

  return (
    <div className="card">
      <h3>📋 Profil actif</h3>
      <div style={{ whiteSpace: "pre-wrap" }}>{preview || "Aucun champ renseigné."}</div>
      <button className="btn" style={{ width: "100%", marginTop: 12 }}
        onClick={() => setValidated(false)}>
        ✏️ Modifier le profil
      </button>
      <div className="card" style={{ marginTop: 12 }}>
        <h4>🔍 Aperçu du prompt</h4>
        <pre style={{ whiteSpace: "pre-wrap", margin: 0 }}>
{preview ? `${preview}\n\nQuestion utilisateur: …` : "Question utilisateur: …"}
        </pre>
      </div>
    </div>
  );
}
