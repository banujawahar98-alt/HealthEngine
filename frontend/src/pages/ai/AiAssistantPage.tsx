import React, { useEffect, useState, useRef } from 'react';
import {
  Bot,
  Send,
  Plus,
  Trash2,
  ShieldAlert,
  ShieldCheck,
  User,
  Sparkles
} from 'lucide-react';
import { aiService } from '../../services/aiService';
import type { ChatMessage, Conversation } from '../../types';
import { useAuth } from '../../context/AuthContext';
import { LoadingSpinner } from '../../components/Loading/LoadingSpinner';
import './AiAssistantPage.css';

export const AiAssistantPage: React.FC = () => {
  const { openCrisisModal } = useAuth();
  const [conversations, setConversations] = useState<Conversation[]>([]);
  const [activeConvId, setActiveConvId] = useState<string | null>(null);
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [inputText, setInputText] = useState('');
  const [sending, setSending] = useState(false);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  const loadConversations = async () => {
    try {
      const res: any = await aiService.getConversations();
      if (res.success) {
        setConversations(res.data);
        if (res.data.length > 0 && !activeConvId) {
          setActiveConvId(res.data[0].id);
        }
      }
    } catch (err: any) {
      setError('Failed to load conversations');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadConversations();
  }, []);

  useEffect(() => {
    const fetchMessages = async () => {
      if (!activeConvId) {
        setMessages([]);
        return;
      }
      try {
        const res: any = await aiService.getConversationMessages(activeConvId);
        if (res.success) {
          setMessages(res.data);
          scrollToBottom();
        }
      } catch (err) {
        console.error(err);
      }
    };
    fetchMessages();
  }, [activeConvId]);

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSend = async (e?: React.FormEvent, customMsg?: string) => {
    if (e) e.preventDefault();
    const msgToSend = customMsg || inputText;
    if (!msgToSend.trim() || sending) return;

    setInputText('');
    setSending(true);
    setError(null);

    // Optimistic User Message
    const tempUserMsg: ChatMessage = {
      id: 'temp-' + Date.now(),
      conversation_id: activeConvId || '',
      role: 'user',
      message: msgToSend,
      created_at: new Date().toISOString()
    };
    setMessages((prev) => [...prev, tempUserMsg]);

    try {
      const res: any = await aiService.sendMessage(msgToSend, activeConvId || undefined);
      if (res.success && res.data) {
        const botReply: ChatMessage = res.data;
        if (!activeConvId) {
          setActiveConvId(botReply.conversation_id);
          loadConversations();
        }
        setMessages((prev) => [...prev.filter((m) => !m.id.startsWith('temp-')), tempUserMsg, botReply]);
      }
    } catch (err: any) {
      setError(err.message || 'Failed to receive AI response');
    } finally {
      setSending(false);
    }
  };

  const handleNewChat = () => {
    setActiveConvId(null);
    setMessages([]);
  };

  const handleDeleteConv = async (id: string, e: React.MouseEvent) => {
    e.stopPropagation();
    if (!window.confirm('Delete this conversation history?')) return;
    try {
      await aiService.deleteConversation(id);
      if (activeConvId === id) {
        setActiveConvId(null);
        setMessages([]);
      }
      loadConversations();
    } catch (err) {
      alert('Failed to delete conversation');
    }
  };

  if (loading) return <LoadingSpinner message="Connecting to MindCare AI Assistant..." />;

  const promptChips = [
    "Hi, how are you today?",
    "I've been feeling really stressed lately",
    "I can't sleep and my mind won't stop racing",
    "I'm anxious about my exams",
    "I've been feeling sad and lonely",
    "I'm feeling overwhelmed with work"
  ];

  return (
    <div className="ai-chat-layout">
      {/* Sidebar - Conversation List */}
      <aside className="ai-sidebar">
        <button onClick={handleNewChat} className="btn btn-primary" style={{ width: '100%', marginBottom: 16 }}>
          <Plus size={18} /> New Conversation
        </button>

        <div className="sidebar-section-title">CONVERSATION HISTORY</div>
        <div className="conversations-list">
          {conversations.length === 0 ? (
            <div style={{ fontSize: '0.85rem', color: '#94a3b8', padding: 12 }}>No previous conversations</div>
          ) : (
            conversations.map((c) => (
              <div
                key={c.id}
                className={`conv-item ${activeConvId === c.id ? 'active' : ''}`}
                onClick={() => setActiveConvId(c.id)}
              >
                <div className="conv-title">{c.title}</div>
                <button className="btn-icon-del" onClick={(e) => handleDeleteConv(c.id, e)} title="Delete">
                  <Trash2 size={14} />
                </button>
              </div>
            ))
          )}
        </div>
      </aside>

      {/* Main Chat Area */}
      <main className="ai-chat-main">
        {/* Chat Header */}
        <div className="chat-header">
          <div className="chat-header-info">
            <div className="ai-avatar">
              <Bot size={22} color="#ffffff" />
            </div>
            <div>
              <h3>MindCare AI Support Assistant</h3>
              <p>Empathetic & Evidence-Informed Guidance</p>
            </div>
          </div>
          <button onClick={openCrisisModal} className="btn btn-outline-crisis btn-sm">
            <ShieldAlert size={16} /> Crisis Support
          </button>
        </div>

        {/* Safety Disclaimer Banner */}
        <div className="chat-safety-banner">
          <ShieldCheck size={16} color="#0d9488" />
          <span>MindCare AI provides well-being education and support. It does not provide medical diagnoses or replace therapy.</span>
        </div>

        {error && (
          <div style={{ background: '#fef2f2', border: '1px solid #fecaca', color: '#991b1b', padding: 10, margin: '0 20px', borderRadius: 8, fontSize: '0.85rem' }}>
            {error}
          </div>
        )}

        {/* Message History Window */}
        <div className="chat-messages-window">
          {messages.length === 0 ? (
            <div className="chat-welcome">
              <div className="welcome-badge">
                <Sparkles size={18} /> MindCare Virtual Assistant
              </div>
              <h2>How can I support your well-being today?</h2>
              <p>Start a conversation — I'll check in with you and listen:</p>

              <div className="prompt-chips-grid">
                {promptChips.map((chip, idx) => (
                  <button key={idx} className="prompt-chip" onClick={() => handleSend(undefined, chip)}>
                    "{chip}"
                  </button>
                ))}
              </div>
            </div>
          ) : (
            messages.map((m) => {
              const isUser = m.role === 'user';
              const isCrisis = m.safety_analysis?.risk_level === 'IMMEDIATE_SAFETY_CONCERN';

              return (
                <div key={m.id} className={`message-row ${isUser ? 'user-row' : 'bot-row'}`}>
                  <div className={`message-avatar ${isUser ? 'user-av' : 'bot-av'}`}>
                    {isUser ? <User size={16} /> : <Bot size={16} />}
                  </div>

                  <div className={`message-bubble ${isUser ? 'user-bubble' : 'bot-bubble'} ${isCrisis ? 'crisis-bubble' : ''}`}>
                    {isCrisis && (
                      <div className="crisis-warning-header">
                        <ShieldAlert size={18} color="#dc2626" />
                        <span>Safety Response Protocol Triggered</span>
                      </div>
                    )}
                    <div className="message-text" style={{ whiteSpace: 'pre-wrap' }}>
                      {m.message}
                    </div>

                    {isCrisis && (
                      <div className="crisis-action-box">
                        <button onClick={openCrisisModal} className="btn btn-crisis btn-sm">
                          View Verified Emergency Helplines
                        </button>
                      </div>
                    )}
                    <div className="message-time">{m.created_at.slice(11, 16)}</div>
                  </div>
                </div>
              );
            })
          )}
          {sending && (
            <div className="message-row bot-row">
              <div className="message-avatar bot-av">
                <Bot size={16} />
              </div>
              <div className="message-bubble bot-bubble">
                <span className="typing-indicator">MindCare AI is thinking...</span>
              </div>
            </div>
          )}
          <div ref={messagesEndRef} />
        </div>

        {/* Input Bar */}
        <form className="chat-input-bar" onSubmit={(e) => handleSend(e)}>
          <input
            type="text"
            className="form-control chat-input"
            placeholder="Type your question or express how you feel..."
            value={inputText}
            onChange={(e) => setInputText(e.target.value)}
            disabled={sending}
          />
          <button type="submit" className="btn btn-primary btn-send" disabled={!inputText.trim() || sending}>
            <Send size={18} />
          </button>
        </form>
      </main>
    </div>
  );
};
