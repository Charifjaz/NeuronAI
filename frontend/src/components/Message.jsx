import ReactMarkdown from 'react-markdown';

function Message({ role, content }) {
  return (
    <div className={`message message-${role}`}>
      <div className="message-avatar">
        {role === 'user' ? 'You' : 'AI'}
      </div>
      <div className="message-content">
        <ReactMarkdown
          components={{
            p: ({node, ...props}) => <p style={{margin: '4px 0'}} {...props} />,
            ul: ({node, ...props}) => <ul style={{margin: '4px 0', paddingLeft: '18px'}} {...props} />,
            ol: ({node, ...props}) => <ol style={{margin: '4px 0', paddingLeft: '18px'}} {...props} />,
            li: ({node, ...props}) => <li style={{margin: '0'}} {...props} />,
            h1: ({node, ...props}) => <h1 style={{margin: '6px 0 4px 0', fontSize: '18px'}} {...props} />,
            h2: ({node, ...props}) => <h2 style={{margin: '6px 0 4px 0', fontSize: '16px'}} {...props} />,
            h3: ({node, ...props}) => <h3 style={{margin: '6px 0 4px 0', fontSize: '15px'}} {...props} />,
          }}
        >
          {content}
        </ReactMarkdown>
      </div>
    </div>
  );
}

export default Message;