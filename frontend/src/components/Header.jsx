import { useNavigate } from 'react-router-dom';

function Header({ isValidated }) {
  const navigate = useNavigate();

  return (
    <header className="header">
      <div className="header-content">
        <div className="header-brand">
          <div className="brand-icon">N</div>
          <div>
            <h1 className="brand-title">Neural Assistant</h1>
            <p className="brand-subtitle">Intelligent conversational interface</p>
          </div>
        </div>

        <div className="header-actions">
          {isValidated && (
            <span className="badge-active">✓ Profile Active</span>
          )}
          
          <button
            className="btn-profile"
            onClick={() => navigate('/profile')}
          >
            {isValidated ? 'Edit Profile' : 'Configure Profile'}
          </button>
        </div>
      </div>
    </header>
  );
}

export default Header;