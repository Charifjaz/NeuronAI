import { useNavigate } from 'react-router-dom';

function Header({ apiBase, setApiBase, isValidated }) {
  const navigate = useNavigate();

  return (
    <header className="header">
      <div className="header-content">
        <div className="header-brand">
          <div className="header-logo">N</div>
          <div>
            <div className="header-title">Neural Assistant</div>
            <div className="header-subtitle">
              Intelligent conversational interface
            </div>
          </div>
        </div>

        <div className="header-actions">
          {isValidated && (
            <span className="badge badge-success">Active</span>
          )}
          
          <button
            className="btn-profile"
            onClick={() => navigate('/profile')}
          >
            Configure Profile
          </button>
        </div>
      </div>
    </header>
  );
}

export default Header;
