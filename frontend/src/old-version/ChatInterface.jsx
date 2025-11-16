import { useState, useRef, useEffect } from 'react';
import Message from './Message';

function ChatInterface({ messages, isValidated, isLoading, onSendMessage }) {
  const [input, setInput] = useState('');
  const messagesEndRef = useRef(null);
  const chatContainerRef = useRef(null);

  // Auto-scroll vers le bas quand de nouveaux messages arrivent
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!input.trim() || !isValidated || isLoading) return;

    onSendMessage(input);
    setInput('');
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmit(e);
    }
  };

  return (
    <div className="chat-container">
      <div className="chat-header">
        <h2>💬 Conversation</h2>
      </div>

      <div className="chat-messages" ref={chatContainerRef}>
        {messages.length === 0 ? (
          <div className="chat-empty">
            <div className="chat-empty-icon">💭</div>
            <p>Aucun message pour le moment</p>
            <p className="chat-empty-hint">
              {isValidated 
                ? 'Commencez la conversation en envoyant un message'
                : 'Activez votre profil pour démarrer'}
            </p>
          </div>
        ) : (
          <>
            {messages.map((msg, index) => (
              <Message key={index} role={msg.role} content={msg.content} />
            ))}
            {isLoading && (
              <div className="message message-assistant">
                <div className="message-avatar">🤖</div>
                <div className="message-content">
                  <div className="typing-indicator">
                    <span></span>
                    <span></span>
                    <span></span>
                  </div>
                </div>
              </div>
            )}
            <div ref={messagesEndRef} />
          </>
        )}
      </div>

      <form className="chat-input-container" onSubmit={handleSubmit}>
        {!isValidated && (
          <div className="chat-info">
            <span className="info-icon">ℹ️</span>
            <span>Activez votre profil dans le panneau de droite pour démarrer la conversation</span>
          </div>
        )}
        
        <div className="chat-input-wrapper">
          <textarea
            className="chat-input"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyPress={handleKeyPress}
            placeholder={isValidated ? "💭 Écrivez votre message..." : "Activez d'abord votre profil"}
            disabled={!isValidated || isLoading}
            rows={1}
            style={{
              minHeight: '50px',
              maxHeight: '150px',
              resize: 'none',
              overflow: 'auto'
            }}
          />
          <button
            type="submit"
            className="chat-send-button"
            disabled={!isValidated || isLoading || !input.trim()}
            aria-label="Envoyer le message"
          >
            {isLoading ? '⏳' : '📤'}
          </button>
        </div>
      </form>
    </div>
  );
}

export default ChatInterface;
