import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { createProfile } from '../services/api';
import { QUESTIONS } from "../services/api";
import './ProfilePage.css';

function ProfilePage() {
  const navigate = useNavigate();
  const [answers, setAnswers] = useState({});
  const [currentQuestion, setCurrentQuestion] = useState(0);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleAnswer = (questionId, value) => {
    setAnswers(prev => ({
      ...prev,
      [questionId]: value
    }));
  };

  const handleMultipleAnswer = (questionId, option) => {
    setAnswers(prev => {
      const current = prev[questionId] || [];
      const newValue = current.includes(option)
        ? current.filter(o => o !== option)
        : [...current, option];
      return { ...prev, [questionId]: newValue };
    });
  };

  const canGoNext = () => {
    const question = QUESTIONS[currentQuestion];
    const answer = answers[question.id];
    
    if (question.type === 'multiple') {
      return answer && answer.length > 0;
    }
    return answer !== undefined && answer !== '';
  };

  const handleNext = () => {
    if (currentQuestion < QUESTIONS.length - 1) {
      setCurrentQuestion(prev => prev + 1);
    }
  };

  const handlePrev = () => {
    if (currentQuestion > 0) {
      setCurrentQuestion(prev => prev - 1);
    }
  };

  const handleSubmit = async () => {
    setLoading(true);
    setError(null);

    try {
      await createProfile(answers);
      navigate('/');
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const question = QUESTIONS[currentQuestion];
  const isLastQuestion = currentQuestion === QUESTIONS.length - 1;

  return (
    <div className="profile-page">
      <div className="profile-card">
        <div className="progress-bar">
          <div 
            className="progress-fill" 
            style={{ width: `${((currentQuestion + 1) / QUESTIONS.length) * 100}%` }}
          />
        </div>

        <h2>Question {currentQuestion + 1} / {QUESTIONS.length}</h2>
        <p className="question-text">{question.label}</p>

        <div className="options">
          {question.options.map((option, idx) => {
            const isSelected = question.type === 'multiple'
              ? (answers[question.id] || []).includes(option)
              : answers[question.id] === option;

            return (
              <label key={idx} className={`option ${isSelected ? 'selected' : ''}`}>
                <input
                  type={question.type === 'multiple' ? 'checkbox' : 'radio'}
                  name={question.id}
                  checked={isSelected}
                  onChange={() => 
                    question.type === 'multiple'
                      ? handleMultipleAnswer(question.id, option)
                      : handleAnswer(question.id, option)
                  }
                />
                <span>{option}</span>
              </label>
            );
          })}
        </div>

        {error && <div className="error">{error}</div>}

        <div className="actions">
          <button 
            onClick={handlePrev} 
            disabled={currentQuestion === 0}
            className="btn-secondary"
          >
            Précédent
          </button>

          {!isLastQuestion ? (
            <button 
              onClick={handleNext} 
              disabled={!canGoNext()}
              className="btn-primary"
            >
              Suivant
            </button>
          ) : (
            <button 
              onClick={handleSubmit} 
              disabled={!canGoNext() || loading}
              className="btn-primary"
            >
              {loading ? 'Envoi...' : 'Activer le profil'}
            </button>
          )}
        </div>
      </div>
    </div>
  );
}

export default ProfilePage;