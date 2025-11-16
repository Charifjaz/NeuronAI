import { Question, QA } from "./type";


const API_BASE =
  (import.meta.env.VITE_API_BASE_URL as string) || "http://localhost:8000";

export async function fetchQuestions(): Promise<Question[]> {
  try {
    const r = await fetch(`${API_BASE.replace(/\/$/, "")}/questions`, {
      method: "GET",
    });
    if (!r.ok) throw new Error(String(r.status));
    const data = (await r.json()) as unknown;
    if (!Array.isArray(data)) throw new Error("questions must be an array");
    return (data as Question[]).map((q) => ({
      ...q,
      label: q.label ?? q.text ?? q.id ?? "Question",
    }));
  } catch {
    // fallback parité Streamlit
    return [
      { id: "context", type: "textarea", label: "Contexte du projet", placeholder: "Décrivez brièvement…", default: "" },
      { id: "objective", type: "text", label: "Objectif principal", placeholder: "Quel est l'objectif ?", default: "" },
      { id: "audience", type: "text", label: "Public cible", placeholder: "À qui s'adresse la réponse ?", default: "" },
    ];
  }
}

export async function ask(message: string, answers: QA): Promise<string> {
  try {
    const r = await fetch(`${API_BASE.replace(/\/$/, "")}/ask`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message, answers }),
    });
    if (!r.ok) throw new Error(String(r.status));
    const data = (await r.json()) as { reply?: string };
    return data?.reply ?? "(Aucune réponse)";
  } catch (e: any) {
    return `Erreur d'appel API: ${e?.message ?? e}`;
  }
}
