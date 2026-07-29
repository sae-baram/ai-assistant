import { useState, useRef, useEffect } from 'react'

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/ask'

function Clock() {
  const [t, setT] = useState(new Date())
  useEffect(() => {
    const id = setInterval(() => setT(new Date()), 1000)
    return () => clearInterval(id)
  }, [])
  return <span className="clock">{t.toLocaleTimeString()}</span>
}

function IconLogo() {
  return (
    <svg width="36" height="36" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" aria-hidden>
      <rect x="2" y="2" width="20" height="20" rx="6" fill="url(#g)" />
      <defs>
        <linearGradient id="g" x1="0" x2="1">
          <stop offset="0" stopColor="#4f8bff" />
          <stop offset="1" stopColor="#7d5dff" />
        </linearGradient>
      </defs>
    </svg>
  )
}

function SendIcon({ className = '' }) {
  return (
    <svg className={className} width="18" height="18" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" aria-hidden>
      <path d="M2 21L23 12L2 3L2 10L17 12L2 14L2 21Z" fill="currentColor" />
    </svg>
  )
}

function Spinner() {
  return (
    <svg className="spinner" viewBox="0 0 50 50" width="18" height="18" aria-hidden>
      <circle className="path" cx="25" cy="25" r="20" fill="none" strokeWidth="4" />
    </svg>
  )
}

function App() {
  const [question, setQuestion] = useState('')
  const [messages, setMessages] = useState([
    {
      role: 'assistant',
      content: 'Üdvözöl a cég AI asszisztense! Kérdezz bármit, például céges adatokról vagy általános tényekről.',
      time: new Date().toLocaleTimeString(),
    }
  ])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)
  const messagesRef = useRef(null)

  useEffect(() => {
    // Scroll to bottom when messages change
    if (messagesRef.current) {
      messagesRef.current.scrollTop = messagesRef.current.scrollHeight
    }
  }, [messages, loading])

  const sendQuestion = async (event) => {
    event?.preventDefault()
    const trimmed = question.trim()
    if (!trimmed) return

    const now = new Date().toLocaleTimeString()
    const userMessage = { role: 'user', content: trimmed, time: now }
    setMessages((prev) => [...prev, userMessage])
    setQuestion('')
    setLoading(true)
    setError(null)

    try {
      const response = await fetch(API_URL, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ question: trimmed })
      })

      if (!response.ok) {
        const body = await response.text()
        throw new Error(`Hálózati hiba: ${response.status} ${body}`)
      }

      const data = await response.json()
      const assistantMessage = {
        role: 'assistant',
        content: data.answer || 'A szerver nem adott vissza választ.',
        time: new Date().toLocaleTimeString(),
      }
      setMessages((prev) => [...prev, assistantMessage])
    } catch (err) {
      const message = err instanceof Error ? err.message : 'Ismeretlen hiba'
      setError(message)
      setMessages((prev) => [
        ...prev,
        { role: 'assistant', content: `Hiba történt: ${message}`, time: new Date().toLocaleTimeString() }
      ])
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="app-shell">
      <div className="chat-panel modern">
        <header className="chat-header modern">
          <div className="branding">
            <IconLogo />
            <div>
              <p className="label">Céges AI asszisztens</p>
              <h1>Gyors üzleti válaszok</h1>
            </div>
          </div>
          <div className="header-actions">
            <Clock />
            <button className="icon-btn" title="Információ">
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <circle cx="12" cy="12" r="10" stroke="#9fb0ff" strokeWidth="1.2" />
                <path d="M11 10h2v6h-2zM11 7h2v2h-2z" fill="#9fb0ff" />
              </svg>
            </button>
          </div>
        </header>

        <section className="chat-window">
          <div className="messages" ref={messagesRef}>
            {messages.map((message, index) => (
              <div key={`${message.role}-${index}`} className={`message ${message.role}`}>
                <div className="avatar" aria-hidden>
                  {message.role === 'assistant' ? 'AI' : 'You'}
                </div>
                <div className="message-body">
                  <div className="message-bubble">
                    <p>{message.content}</p>
                  </div>
                  <div className="message-meta">
                    <span className="role">{message.role === 'assistant' ? 'Asszisztens' : 'Te'}</span>
                    <span className="time">{message.time}</span>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </section>

        <form className="chat-input modern" onSubmit={sendQuestion}>
          <textarea
            value={question}
            onChange={(event) => setQuestion(event.target.value)}
            placeholder="Írd be a kérdésed... például: Mennyi volt az Q2 bevétel?"
            rows={2}
            disabled={loading}
            aria-label="Kérdés szövege"
          />
          <button type="submit" className="send-btn" disabled={loading} aria-label="Küldés">
            {loading ? <Spinner /> : <><SendIcon /><span className="send-text">Küldés</span></>}
          </button>
        </form>

        <div className="info-bar modern">
          {error ? <span className="error-text">{error}</span> : <span className="hint">Tip: kérj céges adatokat pontos lekérdezéssel (pl. 'Q2 bevétel')</span>}
        </div>
      </div>
    </div>
  )
}

export default App
