import { useState } from 'react';

function Header({ apiBase, setApiBase, isValidated }) {
  const [showConfig, setShowConfig] = useState(false);

  return (
    <>
      <header className="header">
        <div className="header-content">
          <h1 className="header-title">
            🧠 Neural Chat Interface
          </h1>
          <p className="header-subtitle">
            Intelligence conversationnelle avec profil contextuel
          </p>
        </div>
        
        <button 
          className="config-toggle"
          onClick={() => setShowConfig(!showConfig)}
          aria-label="Toggle configuration"
        >
          ⚙️
        </button>
      </header>

      {showConfig && (
        <div className="config-panel">
          <div className="config-content">
            <h3>⚙️ Configuration</h3>
            <div className="config-field">
              <label htmlFor="api-base">🔗 API Base URL</label>
              <input
                id="api-base"
                type="text"
                value={apiBase}
                onChange={(e) => setApiBase(e.target.value)}
                placeholder="http://localhost:8000"
              />
            </div>

            <div className="divider"></div>

            <h3>📊 État du système</h3>
            {isValidated ? (
              <div className="status-badge status-success">
                <span className="status-icon">✅</span>
                <div>
                  <div className="status-title">Profil activé</div>
                  <div className="status-caption">Le contexte est appliqué à toutes les requêtes</div>
                </div>
              </div>
            ) : (
              <div className="status-badge status-warning">
                <span className="status-icon">⚠️</span>
                <div>
                  <div className="status-title">Profil inactif</div>
                  <div className="status-caption">Validez votre profil pour activer le chat</div>
                </div>
              </div>
            )}
          </div>
        </div>
      )}

      <div className="divider"></div>
    </>
  );
}

export default Header;
