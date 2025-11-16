import { useNavigate } from 'react-router-dom';
import { buildPrompt } from '../services/api';
import '../styles/ProfilePage.css';

function ProfilePage({
  questions,
  answersDraft,
  answersValidated,
  isValidated,
  onAnswerChange,
  onValidateProfile,
  onEditProfile,
}) {
  const navigate = useNavigate();

  const handleSubmit = (e) => {
    e.preventDefault();
    onValidateProfile();
    navigate('/');
  };

  const renderQuestionInput = (question) => {
    const { id, type, label, placeholder, scale_min, scale_max } = question;
    const value = answersDraft[id] || '';

    switch (type) {
      case 'textarea':
        return (
          <div key={id} className="form-group">
            <label htmlFor={id} className="form-label">
              {label}
            </label>
            <textarea
              id={id}
              value={value}
              onChange={(e) => onAnswerChange(id, e.target.value)}
              placeholder={placeholder}
              className="form-textarea"
              rows={4}
            />
          </div>
        );

      case 'slider':
        const min = scale_min || 0;
        const max = scale_max || 10;
        return (
          <div key={id} className="form-group">
            <div className="form-label-row">
              <label htmlFor={id} className="form-label">
                {label}
              </label>
              <span className="slider-value-display">{value}</span>
            </div>
            <input
              type="range"
              id={id}
              min={min}
              max={max}
              value={value}
              onChange={(e) => onAnswerChange(id, parseInt(e.target.value))}
              className="form-slider"
            />
            <div className="slider-labels">
              <span>{min}</span>
              <span>{max}</span>
            </div>
          </div>
        );

      default:
        return (
          <div key={id} className="form-group">
            <label htmlFor={id} className="form-label">
              {label}
            </label>
            <input
              type="text"
              id={id}
              value={value}
              onChange={(e) => onAnswerChange(id, e.target.value)}
              placeholder={placeholder}
              className="form-input"
            />
          </div>
        );
    }
  };

  if (!questions) {
    return (
      <div className="profile-page">
        <div className="profile-container">
          <div className="loading-state">Loading configuration...</div>
        </div>
      </div>
    );
  }

  return (
    <div className="profile-page">
      <div className="profile-header-section">
        <div className="profile-header-content">
          <button className="btn-back" onClick={() => navigate('/')}>
            ← Back to Chat
          </button>
          <div>
            <h1 className="profile-page-title">Profile Configuration</h1>
            <p className="profile-page-subtitle">
              Customize your assistant's behavior by providing context and preferences
            </p>
          </div>
        </div>
      </div>

      <div className="profile-container">
        {!isValidated ? (
          <div className="profile-card">
            <div className="profile-card-header">
              <h2 className="profile-card-title">Your Profile</h2>
              <p className="profile-card-description">
                Fill in the information below to personalize your experience
              </p>
            </div>

            <form onSubmit={handleSubmit} className="profile-form">
              {questions.map(renderQuestionInput)}

              <div className="form-actions">
                <button type="submit" className="btn btn-primary btn-lg btn-full-width">
                  Activate Profile
                </button>
              </div>
            </form>
          </div>
        ) : (
          <div className="profile-card">
            <div className="profile-card-header">
              <div className="profile-status">
                <span className="badge badge-success">Active Profile</span>
              </div>
              <h2 className="profile-card-title">Your Profile</h2>
              <p className="profile-card-description">
                Your profile is currently active and being used in conversations
              </p>
            </div>

            <div className="profile-summary">
              {questions.map((q) => {
                const value = answersValidated[q.id];
                const displayValue =
                  value && String(value).trim() ? value : 'Not specified';

                return (
                  <div key={q.id} className="summary-item">
                    <div className="summary-label">{q.label}</div>
                    <div className="summary-value">{displayValue}</div>
                  </div>
                );
              })}
            </div>

            <div className="profile-actions">
              <button
                onClick={() => {
                  onEditProfile();
                }}
                className="btn btn-outline btn-full-width"
              >
                Edit Profile
              </button>
              <button
                onClick={() => navigate('/')}
                className="btn btn-primary btn-full-width"
              >
                Back to Chat
              </button>
            </div>

            <details className="profile-details">
              <summary className="profile-details-summary">
                View Generated Prompt
              </summary>
              <pre className="profile-details-content">
                {buildPrompt('Your next message...', answersValidated)}
              </pre>
            </details>
          </div>
        )}
      </div>
    </div>
  );
}

export default ProfilePage;
