import { useState, useRef, useEffect, useCallback } from "react";
import "./App.css";

interface Message {
  id: string;
  role: "user" | "assistant" | "error";
  content: string;
  agent?: string;
  timestamp: Date;
}

const AGENTS = [
  { value: "web-search-agent",    label: "Web Search",    tool: "WebsiteSearchTool",          color: "#58a6ff" },
  { value: "file-reader-agent",   label: "File Reader",   tool: "FileReadTool",               color: "#3fb950" },
  { value: "file-writer-agent",   label: "File Writer",   tool: "FileWriterTool",             color: "#a371f7" },
  { value: "pdf-search-agent",    label: "PDF Search",    tool: "PDFSearchTool",              color: "#f0883e" },
  { value: "csv-rag-agent",       label: "CSV RAG",       tool: "CSVSearchTool + LanceDB",    color: "#d29922" },
  { value: "scrape-agent",        label: "Scraper",       tool: "ScrapeWebsiteTool",          color: "#f778ba" },
  { value: "google-search-agent", label: "Google Search", tool: "SerpApiGoogleSearchTool",    color: "#79c0ff" },
  { value: "shopping-agent",      label: "Shopping",      tool: "SerpApiGoogleShoppingTool",  color: "#56d364" },
  { value: "serper-search-agent", label: "Serper Search", tool: "SerperDevTool",              color: "#ff7b72" },
];

const SUGGESTIONS = [
  { title: "Search the web", text: "for latest AI trends in 2026", agent: "web-search-agent" },
  { title: "Analyze CSV data", text: "Who earns the highest salary?", agent: "csv-rag-agent" },
  { title: "Scrape a website", text: "Extract quotes from quotes.toscrape.com", agent: "scrape-agent" },
  { title: "Search Google", text: "Best AI frameworks for agents", agent: "google-search-agent" },
];

function formatTime(date: Date) {
  return date.toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" });
}

function App() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState("");
  const [selectedAgent, setSelectedAgent] = useState(AGENTS[0].value);
  const [loading, setLoading] = useState(false);
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const textareaRef = useRef<HTMLTextAreaElement>(null);

  const scrollToBottom = useCallback(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, []);

  useEffect(() => {
    scrollToBottom();
  }, [messages, loading, scrollToBottom]);

  useEffect(() => {
    if (textareaRef.current) {
      textareaRef.current.style.height = "auto";
      textareaRef.current.style.height = Math.min(textareaRef.current.scrollHeight, 150) + "px";
    }
  }, [input]);

  const sendMessage = async (query?: string, agent?: string) => {
    const text = query || input.trim();
    if (!text || loading) return;

    const agentType = agent || selectedAgent;
    const agentInfo = AGENTS.find((a) => a.value === agentType);

    const userMsg: Message = {
      id: crypto.randomUUID(),
      role: "user",
      content: text,
      agent: agentInfo?.label,
      timestamp: new Date(),
    };

    setMessages((prev) => [...prev, userMsg]);
    setInput("");
    setLoading(true);

    if (agent) setSelectedAgent(agent);

    try {
      const res = await fetch("/api/execute", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ agent_type: agentType, query: text }),
      });

      const data = await res.json();

      if (!res.ok) throw new Error(data.detail || "Request failed");

      setMessages((prev) => [
        ...prev,
        {
          id: crypto.randomUUID(),
          role: "assistant",
          content: data.result,
          agent: agentInfo?.label,
          timestamp: new Date(),
        },
      ]);
    } catch (err: unknown) {
      const errMsg = err instanceof Error ? err.message : "An unexpected error occurred";
      setMessages((prev) => [
        ...prev,
        {
          id: crypto.randomUUID(),
          role: "error",
          content: errMsg,
          timestamp: new Date(),
        },
      ]);
    } finally {
      setLoading(false);
    }
  };

  const clearChat = () => {
    setMessages([]);
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  const currentAgent = AGENTS.find((a) => a.value === selectedAgent);

  return (
    <div className="app">
      {/* Mobile overlay */}
      {sidebarOpen && (
        <div className="sidebar-overlay" onClick={() => setSidebarOpen(false)} />
      )}

      {/* Sidebar */}
      <aside className={`sidebar ${sidebarOpen ? "open" : ""}`}>
        <div className="sidebar-header">
          <div className="sidebar-logo">
            <div className="logo-icon">⚡</div>
            <div>
              <h1>CrewAI Platform</h1>
              <span>Multi-Agent System</span>
            </div>
          </div>
          <button className="new-chat-btn" onClick={clearChat}>
            ＋ New Chat
          </button>
        </div>

        <div className="sidebar-agents">
          <div className="agents-label">Agents</div>
          {AGENTS.map((agent) => (
            <div
              key={agent.value}
              className={`agent-item ${selectedAgent === agent.value ? "active" : ""}`}
              onClick={() => {
                setSelectedAgent(agent.value);
                setSidebarOpen(false);
              }}
            >
              <div className="agent-dot" style={{ background: agent.color }} />
              <div className="agent-item-info">
                <div className="agent-item-name">{agent.label}</div>
                <div className="agent-item-tool">{agent.tool}</div>
              </div>
            </div>
          ))}
        </div>

        <div className="sidebar-footer">
          <div className="status-indicator">
            <div className="status-dot" />
            <span>System Online</span>
          </div>
        </div>
      </aside>

      {/* Main chat area */}
      <main className="main">
        <div className="chat-header">
          <div className="chat-header-left">
            <button className="mobile-menu-btn" onClick={() => setSidebarOpen(true)}>
              ☰
            </button>
            <span className="chat-header-title">Chat</span>
            <div className="chat-agent-badge">
              <span className="badge-dot" style={{ background: currentAgent?.color }} />
              {currentAgent?.label}
            </div>
          </div>
        </div>

        {/* Messages */}
        <div className="messages">
          {messages.length === 0 && !loading ? (
            <div className="messages-empty">
              <div className="empty-icon">🤖</div>
              <h2>How can I help you?</h2>
              <p>
                Select an agent from the sidebar and ask your question.
                Each agent has specialized tools for different tasks.
              </p>
              <div className="suggestions">
                {SUGGESTIONS.map((s, i) => (
                  <button
                    key={i}
                    className="suggestion-chip"
                    onClick={() => sendMessage(s.text, s.agent)}
                  >
                    <strong>{s.title}</strong>
                    {s.text}
                  </button>
                ))}
              </div>
            </div>
          ) : (
            <>
              {messages.map((msg) => (
                <div key={msg.id} className={`message ${msg.role}`}>
                  <div className="message-avatar">
                    {msg.role === "user" ? "U" : msg.role === "error" ? "!" : "AI"}
                  </div>
                  <div className="message-content">
                    <div className="message-bubble">{msg.content}</div>
                    <div className="message-meta">
                      <span>{formatTime(msg.timestamp)}</span>
                      {msg.agent && (
                        <span className="message-agent-tag">{msg.agent}</span>
                      )}
                    </div>
                  </div>
                </div>
              ))}

              {loading && (
                <div className="typing-indicator">
                  <div className="message-avatar" style={{ background: "linear-gradient(135deg, #a371f7, #58a6ff)", color: "white", width: 32, height: 32, borderRadius: "50%", display: "flex", alignItems: "center", justifyContent: "center", fontSize: 14 }}>
                    AI
                  </div>
                  <div className="typing-bubble">
                    <div className="typing-dots">
                      <span /><span /><span />
                    </div>
                    <span className="typing-text">{currentAgent?.label} is thinking...</span>
                  </div>
                </div>
              )}

              <div ref={messagesEndRef} />
            </>
          )}
        </div>

        {/* Input */}
        <div className="input-area">
          <div className="input-container">
            <div className="input-box">
              <textarea
                ref={textareaRef}
                value={input}
                onChange={(e) => setInput(e.target.value)}
                onKeyDown={handleKeyDown}
                placeholder={`Ask ${currentAgent?.label} anything...`}
                rows={1}
                disabled={loading}
              />
              <button
                className="send-btn"
                onClick={() => sendMessage()}
                disabled={loading || !input.trim()}
              >
                ➤
              </button>
            </div>
            <div className="input-hint">
              <kbd>Enter</kbd> to send · <kbd>Shift+Enter</kbd> for new line
            </div>
          </div>
        </div>
      </main>
    </div>
  );
}

export default App;
