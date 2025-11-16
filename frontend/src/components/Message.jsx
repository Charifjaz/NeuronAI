function Message({ role, content }) {
  const isUser = role === 'user';

  return (
    <div className={`message message-${role}`}>
      <div className="message-avatar">{isUser ? 'You' : 'AI'}</div>
      <div className="message-content">
        <div className="message-author">{isUser ? 'You' : 'Assistant'}</div>
        <div className="message-bubble">{content}</div>
      </div>
    </div>
  );
}

export default Message;
