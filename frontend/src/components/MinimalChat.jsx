import React, { useState, useRef, useEffect } from "react";
import { ArrowRight } from "lucide-react";

export default function MinimalChat({ apiUrl = "http://localhost:8000/ask" }) {
  const [q, setQ] = useState("");
  const [messages, setMessages] = useState([
    { role: "assistant", text: "Üdvözöl a céges AI asszisztens.", time: new Date().toLocaleTimeString() }
  ]);
  const [loading, setLoading] = useState(false);
  const listRef = useRef();

  useEffect(() => {
    if (listRef.current) listRef.current.scrollTop = listRef.current.scrollHeight;
  }, [messages]);

  async function send(e) {
    e?.preventDefault();
    const text = q.trim();
    if (!text) return;
    const time = new Date().toLocaleTimeString();
    setMessages(prev => [...prev, { role: "user", text, time }]);
    setQ("");
    setLoading(true);

    try {
      const res = await fetch(apiUrl, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ question: text })
      });
      if (!res.ok) throw new Error(`${res.status}`);
      const data = await res.json();
      const answer = data.answer ?? "Nincs válasz a szervertől.";
      setMessages(prev => [...prev, { role: "assistant", text: answer, time: new Date().toLocaleTimeString() }]);
    } catch (err) {
      setMessages(prev => [...prev, { role: "assistant", text: `Hiba: ${err.message}`, time: new Date().toLocaleTimeString() }]);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="min-h-screen flex items-center justify-center bg-[#000000] p-6">
      <div className="w-full max-w-3xl h-[80vh] grid grid-rows-[auto_1fr_auto] border border-white/10 bg-[#0A0A0A] rounded-lg shadow-sm">
        {/* Header */}
        <div className="flex items-center justify-between px-4 py-3 border-b border-white/6">
          <div className="flex items-center gap-3">
            <div className="w-9 h-9 flex items-center justify-center bg-[#171717] border border-white/6 text-white text-sm font-semibold rounded-md">
              AI
            </div>
            <div>
              <div className="text-white tracking-tight font-semibold">Céges AI asszisztens</div>
              <div className="text-neutral-400 text-sm">Gyors, pontos üzleti válaszok</div>
            </div>
          </div>
          <div className="text-neutral-400 text-sm">{new Date().toLocaleDateString()}</div>
        </div>

        {/* Messages */}
        <div ref={listRef} className="px-4 py-3 overflow-y-auto space-y-4">
          {messages.map((m, i) => (
            <div key={i} className="flex items-start gap-3">
              {m.role === "assistant" ? (
                <>
                  <div className="flex-shrink-0 mt-1">
                    <div className="text-xs text-neutral-400 px-2 py-0.5 border border-neutral-700 rounded-md">AI</div>
                  </div>
                  <div className="min-w-0">
                    <div className="text-white leading-relaxed whitespace-pre-wrap">{m.text}</div>
                    <div className="text-neutral-400 text-xs mt-1">{m.time}</div>
                  </div>
                </>
              ) : (
                <>
                  <div className="flex-1 text-right">
                    <div className="text-neutral-400 text-xs mb-1">{m.time}</div>
                    <div className="text-white/90 leading-relaxed whitespace-pre-wrap">{m.text}</div>
                  </div>
                </>
              )}
            </div>
          ))}
        </div>

        {/* Input (sticky-like bottom row) */}
        <form onSubmit={send} className="relative px-4 py-3 border-t border-white/6 bg-[#0A0A0A]">
          <div className="relative max-w-full">
            <textarea
              value={q}
              onChange={(e) => setQ(e.target.value)}
              rows={2}
              className="w-full resize-none bg-[#171717] text-white placeholder:text-neutral-500 border border-white/6 rounded-md px-3 py-2 pr-14 focus:outline-none transition-shadow focus:shadow-[0_0_0_3px_rgba(255,255,255,0.04)]"
              placeholder="Írd be a kérdésed (pl. 'Mennyi volt a Q2 bevétel?')"
            />
            <button
              type="submit"
              disabled={loading}
              className="absolute right-3 top-1/2 -translate-y-1/2 bg-transparent text-white/90 border border-white/8 px-3 py-2 rounded-md hover:bg-white/2 transition"
              aria-label="Küldés"
            >
              <div className="flex items-center gap-2">
                <ArrowRight size={16} />
                <span className="text-xs">Küldés</span>
              </div>
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
