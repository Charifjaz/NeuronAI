import { useState, useRef, useEffect } from 'react';
import Message from './Message';

function ChatInterface({ messages, isValidated, isLoading, onSendMessage }) {
  const [input, setInput] = useState('');
  const messagesEndRef = useRef(null);

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
      <div className="chat-messages">
        {messages.length === 0 ? (
          <div className="chat-empty">
            <div className="empty-icon">N</div>
            <h2 className="empty-title">Start a conversation</h2>
            <p className="empty-description">
              {isValidated
                ? 'Ask me anything. I\'m here to help you with your questions and provide personalized insights based on your profile.'
                : 'Configure your profile first to enable personalized conversations and get the most relevant responses.'}
            </p>
          </div>
        ) : (
          <>
            {messages.map((msg, index) => (
              <Message key={index} role={msg.role} content={msg.content} />
            ))}
            {isLoading && (
              <div className="message message-assistant">
                <div className="message-avatar">AI</div>
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

      <div className="chat-input-container">
        {!isValidated && (
          <div className="chat-info">
            <span className="info-icon">i</span>
            <span>Configure your profile to start the conversation</span>
          </div>
        )}

        <form className="chat-input-wrapper" onSubmit={handleSubmit}>
          <textarea
            className="chat-input"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyPress={handleKeyPress}
            placeholder={
              isValidated
                ? 'Type your message...'
                : 'Configure your profile first'
            }
            disabled={!isValidated || isLoading}
            rows={1}
            style={{
              minHeight: '48px',
              maxHeight: '200px',
              overflow: 'auto',
            }}
          />
          <button
            type="submit"
            className="btn-send"
            disabled={!isValidated || isLoading || !input.trim()}
            aria-label="Send message"
          >
            →
          </button>
        </form>
      </div>
    </div>
  );
}

export default ChatInterface;
