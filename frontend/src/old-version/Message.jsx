function Message({ role, content }) {
  const isUser = role === 'user';
  
  return (
    <div className={`message message-${role}`}>
      <div className="message-avatar">
        {isUser ? '🧑' : '🤖'}
      </div>
      <div className="message-content">
        <div className="message-text">
          {content}
        </div>
      </div>
    </div>
  );
}

export default Message;
