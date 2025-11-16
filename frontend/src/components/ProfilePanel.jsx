import { useState } from 'react';
import { buildPrompt } from '../services/api';

function ProfilePanel({
  questions,
  answersDraft,
  answersValidated,
  isValidated,
  onAnswerChange,
  onValidateProfile,
  onEditProfile
}) {
  const [showPromptPreview, setShowPromptPreview] = useState(false);

  if (!questions) {
    return (
      <div className="profile-panel">
        <div className="profile-header">
          <h2>🎯 Profil Contextuel</h2>
        </div>
        <div className="loading-spinner">Chargement...</div>
      </div>
    );
  }

  const renderQuestionInput = (question) => {
    const { id, type, label, placeholder, scale_min, scale_max } = question;
    const value = answersDraft[id] || '';

    switch (type) {
      case 'textarea':
        return (
          <div key={id} className="form-field">
            <label htmlFor={id}>{label}</label>
            <textarea
              id={id}
              value={value}
              onChange={(e) => onAnswerChange(id, e.target.value)}
              placeholder={placeholder}
              rows={4}
            />
          </div>
        );

      case 'slider':
        const min = scale_min || 0;
        const max = scale_max || 10;
        return (
          <div key={id} className="form-field">
            <label htmlFor={id}>
              {label}
              <span className="slider-value">{value}</span>
            </label>
            <input
              type="range"
              id={id}
              min={min}
              max={max}
              value={value}
              onChange={(e) => onAnswerChange(id, parseInt(e.target.value))}
              className="slider-input"
            />
            <div className="slider-labels">
              <span>{min}</span>
              <span>{max}</span>
            </div>
          </div>
        );

      default:
        return (
          <div key={id} className="form-field">
            <label htmlFor={id}>{label}</label>
            <input
              type="text"
              id={id}
              value={value}
              onChange={(e) => onAnswerChange(id, e.target.value)}
              placeholder={placeholder}
            />
          </div>
        );
    }
  };

  return (
    <div className="profile-panel">
      <div className="profile-header">
        <h2>🎯 Profil Contextuel</h2>
      </div>

      {!isValidated ? (
        <form
          className="profile-form"
          onSubmit={(e) => {
            e.preventDefault();
            onValidateProfile();
          }}
        >
          {questions.map(renderQuestionInput)}

          <button type="submit" className="btn-primary btn-full-width">
            🚀 Activer le profil
          </button>
        </form>
      ) : (
        <div className="profile-validated">
          <div className="profile-summary">
            <div className="summary-header">
              <h3>📋 Profil actif</h3>
            </div>
            <div className="summary-content">
              {questions.map((q) => {
                const value = answersValidated[q.id];
                const displayValue = value && String(value).trim() 
                  ? value 
                  : '(non renseigné)';
                
                return (
                  <div key={q.id} className="summary-item">
                    <div className="summary-label">{q.label}</div>
                    <div className="summary-value">
                      {displayValue}
                    </div>
                  </div>
                );
              })}
            </div>
          </div>

          <button 
            onClick={onEditProfile}
            className="btn-secondary btn-full-width"
          >
            ✏️ Modifier le profil
          </button>

          <div className="divider"></div>

          <details className="prompt-preview">
            <summary className="prompt-preview-header">
              🔍 Aperçu du prompt
            </summary>
            <pre className="prompt-preview-content">
              {buildPrompt('Votre prochain message...', answersValidated)}
            </pre>
          </details>
        </div>
      )}
    </div>
  );
}

export default ProfilePanel;
