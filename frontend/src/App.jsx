import { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Header from './components/Header';
import ChatInterface from './components/ChatInterface';
import ProfilePage from './components/ProfilePage';
import { fetchQuestions, sendMessage } from './services/api';
import './styles/App.css';

function App() {
  const [apiBase, setApiBase] = useState(
    import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'
  );

  const [questions, setQuestions] = useState(null);
  const [answersDraft, setAnswersDraft] = useState({});
  const [answersValidated, setAnswersValidated] = useState({});
  const [isValidated, setIsValidated] = useState(false);
  const [messages, setMessages] = useState([]);
  const [isLoading, setIsLoading] = useState(false);

  // Charger les questions au montage
  useEffect(() => {
    loadQuestions();
  }, [apiBase]);

  const loadQuestions = async () => {
    try {
      const data = await fetchQuestions(apiBase);
      setQuestions(data);

      // Initialiser les réponses brouillon
      const initialDraft = {};
      data.forEach((q) => {
        if (q.default !== undefined) {
          initialDraft[q.id] = q.default;
        } else if (q.type === 'slider') {
          const min = q.scale_min || 0;
          const max = q.scale_max || 10;
          initialDraft[q.id] = Math.floor((min + max) / 2);
        } else {
          initialDraft[q.id] = '';
        }
      });
      setAnswersDraft(initialDraft);
    } catch (error) {
      console.error('Error loading questions:', error);
      // Questions par défaut en cas d'erreur
      setQuestions([
        {
          id: 'context',
          type: 'textarea',
          label: 'Project Context',
          placeholder: 'Describe your project briefly...',
          default: '',
        },
        {
          id: 'objective',
          type: 'text',
          label: 'Main Objective',
          placeholder: 'What is the main goal?',
          default: '',
        },
        {
          id: 'audience',
          type: 'text',
          label: 'Target Audience',
          placeholder: 'Who is this for?',
          default: '',
        },
      ]);
    }
  };

  const handleAnswerChange = (questionId, value) => {
    setAnswersDraft((prev) => ({
      ...prev,
      [questionId]: value,
    }));
  };

  const handleValidateProfile = () => {
    setAnswersValidated({ ...answersDraft });
    setIsValidated(true);
  };

  const handleEditProfile = () => {
    setIsValidated(false);
  };

  const handleSendMessage = async (userMessage) => {
    if (!userMessage.trim() || !isValidated) return;

    // Ajouter le message utilisateur
    const userMsg = { role: 'user', content: userMessage };
    setMessages((prev) => [...prev, userMsg]);
    setIsLoading(true);

    try {
      const reply = await sendMessage(apiBase, userMessage, answersValidated);

      // Ajouter la réponse de l'assistant
      const assistantMsg = { role: 'assistant', content: reply };
      setMessages((prev) => [...prev, assistantMsg]);
    } catch (error) {
      console.error('Error sending message:', error);
      const errorMsg = {
        role: 'assistant',
        content: `Error: ${error.message}`,
      };
      setMessages((prev) => [...prev, errorMsg]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <Router>
      <div className="app">
        <Header
          apiBase={apiBase}
          setApiBase={setApiBase}
          isValidated={isValidated}
        />

        <Routes>
          <Route
            path="/"
            element={
              <ChatInterface
                messages={messages}
                isValidated={isValidated}
                isLoading={isLoading}
                onSendMessage={handleSendMessage}
              />
            }
          />
          <Route
            path="/profile"
            element={
              <ProfilePage
                questions={questions}
                answersDraft={answersDraft}
                answersValidated={answersValidated}
                isValidated={isValidated}
                onAnswerChange={handleAnswerChange}
                onValidateProfile={handleValidateProfile}
                onEditProfile={handleEditProfile}
              />
            }
          />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
