import { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, useLocation } from 'react-router-dom';
import Header from './components/Header';
import ChatInterface from './components/ChatInterface';
import ProfilePage from './components/ProfilePage';
import { fetchQuestions, sendMessage, validateProfile, getProfile } from './services/api';
import './styles/App.css';

function AppContent() {
  const location = useLocation();
  const [questions, setQuestions] = useState(null);
  const [answersDraft, setAnswersDraft] = useState({});
  const [answersValidated, setAnswersValidated] = useState({});
  const [isValidated, setIsValidated] = useState(false);
  const [messages, setMessages] = useState([]);
  const [isLoading, setIsLoading] = useState(false);

  // Charger les questions au montage
  useEffect(() => {
    loadQuestions();
  }, []);

  // Vérifier si le profil existe à chaque changement de route
  useEffect(() => {
    checkIfProfileExists();
  }, [location.pathname]);

  const checkIfProfileExists = async () => {
    const profile = await getProfile();
    if (profile) {
      setIsValidated(true);
    }
  };

  const loadQuestions = async () => {
    try {
      const data = await fetchQuestions();
      setQuestions(data);

      // Initialiser les réponses brouillon
      const initialDraft = {};
      data.forEach((q) => {
        if (q.type === 'multiple') {
          initialDraft[q.id] = [];
        } else {
          initialDraft[q.id] = '';
        }
      });
      setAnswersDraft(initialDraft);
    } catch (error) {
      console.error('Error loading questions:', error);
    }
  };

  const handleAnswerChange = (questionId, value) => {
    setAnswersDraft((prev) => ({
      ...prev,
      [questionId]: value,
    }));
  };

  const handleValidateProfile = async () => {
    try {
      await validateProfile(answersDraft);
      setAnswersValidated({ ...answersDraft });
      setIsValidated(true);
    } catch (error) {
      console.error('Error validating profile:', error);
      alert('Erreur lors de la validation du profil');
    }
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
      const reply = await sendMessage(userMessage);

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
    <div className="app">
      <Header isValidated={isValidated} />

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
  );
}

function App() {
  return (
    <Router>
      <AppContent />
    </Router>
  );
}

export default App;