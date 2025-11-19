function Message({ role, content }) {
  return (
    <div className={`message message-${role}`}>
      <div className="message-avatar">
        {role === 'user' ? 'You' : 'AI'}
      </div>
      <div className="message-content">
        {content}
      </div>
    </div>
  );
}

export default Message;