import { useState, useEffect, useRef } from 'react';
import { useNavigate } from 'react-router-dom';
import { sendMessage, getProfile } from '../services/api';
import './ChatPage.css';

function ChatPage() {
  const navigate = useNavigate();
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [hasProfile, setHasProfile] = useState(false);
  const messagesEndRef = useRef(null);

  useEffect(() => {
    checkProfile();
  }, []);

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const checkProfile = async () => {
    const profile = await getProfile();
    if (!profile) {
      navigate('/profile');
    } else {
      setHasProfile(true);
    }
  };

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  const handleSend = async () => {
    if (!input.trim() || loading) return;

    const userMessage = input.trim();
    setInput('');
    
    setMessages(prev => [...prev, { role: 'user', content: userMessage }]);
    setLoading(true);

    try {
      const response = await sendMessage(userMessage);
      setMessages(prev => [...prev, { role: 'assistant', content: response.answer }]);
    } catch (error) {
      setMessages(prev => [...prev, { 
        role: 'assistant', 
        content: `Erreur: ${error.message}` 
      }]);
    } finally {
      setLoading(false);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  if (!hasProfile) {
    return null;
  }

  return (
    <div className="chat-page">
      <div className="chat-container">
        <div className="chat-header">
          <h1>Chat Assistant</h1>
          <button onClick={() => navigate('/profile')} className="btn-profile">
            Profil
          </button>
        </div>

        <div className="messages">
          {messages.length === 0 && (
            <div className="welcome">
              <h2>Bienvenue</h2>
              <p>Posez votre question, l'assistant s'adaptera à votre profil.</p>
            </div>
          )}

          {messages.map((msg, idx) => (
            <div key={idx} className={`message ${msg.role}`}>
              <div className="message-content">{msg.content}</div>
            </div>
          ))}

          {loading && (
            <div className="message assistant">
              <div className="message-content loading">
                <span></span>
                <span></span>
                <span></span>
              </div>
            </div>
          )}

          <div ref={messagesEndRef} />
        </div>

        <div className="input-area">
          <textarea
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyPress={handleKeyPress}
            placeholder="Écrivez votre message..."
            disabled={loading}
            rows={3}
          />
          <button 
            onClick={handleSend} 
            disabled={!input.trim() || loading}
            className="btn-send"
          >
            Envoyer
          </button>
        </div>
      </div>
    </div>
  );
}

export default ChatPage;
