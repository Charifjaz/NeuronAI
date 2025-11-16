import { useRef, useState } from "react";
import { ask } from "../api";
import { Message, QA } from "../type";

export default function Chat({ answers, validated }: { answers: QA; validated: boolean }) {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState("");
  const scroller = useRef<HTMLDivElement>(null);

  async function send() {
    if (!validated || !input.trim()) return;
    const u: Message = { role: "user", content: input };
    setMessages((m) => [...m, u]);
    setInput("");

    const reply = await ask(u.content, answers);
    const a: Message = { role: "assistant", content: reply };
    setMessages((m) => [...m, a]);
    setTimeout(() => scroller.current?.scrollTo({ top: 999999, behavior: "smooth" }), 50);
  }

  return (
    <div className="card chat">
      <div>
        <h3>💬 Conversation</h3>
      </div>
      <div className="chat-scroll" ref={scroller}>
        {messages.map((m, i) => (
          <div key={i} className={`msg ${m.role}`}>{m.content}</div>
        ))}
      </div>
      <div style={{ display: "flex", gap: 8 }}>
        <input
          className="input"
          placeholder={validated ? "Écrivez votre message…" : "Activez votre profil pour commencer"}
          disabled={!validated}
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={(e) => (e.key === "Enter" ? send() : null)}
        />
        <button className="btn" onClick={send} disabled={!validated}>Envoyer</button>
      </div>
      {!validated && (
        <div className="card" style={{ marginTop: 10 }}>👉 Activez votre profil à droite pour démarrer la conversation</div>
      )}
    </div>
  );
}
