/**
 * Service API pour communiquer avec le backend
 */

/**
 * Récupère la liste des questions depuis l'API
 */
export async function fetchQuestions(apiBase) {
  const url = `${apiBase.replace(/\/$/, '')}/questions`;
  
  try {
    const response = await fetch(url, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      },
      signal: AbortSignal.timeout(15000), // 15s timeout
    });

    if (!response.ok) {
      throw new Error(`HTTP ${response.status}: ${response.statusText}`);
    }

    const data = await response.json();
    
    if (!Array.isArray(data)) {
      throw new Error('Le format /questions doit être une liste JSON');
    }

    // S'assurer que chaque question a un label
    return data.map(q => ({
      ...q,
      label: q.label || q.text || q.id || 'Question'
    }));
  } catch (error) {
    console.error('Erreur fetchQuestions:', error);
    throw error;
  }
}

/**
 * Envoie un message au backend avec le contexte utilisateur
 */
export async function sendMessage(apiBase, message, answers) {
  const url = `${apiBase.replace(/\/$/, '')}/ask`;
  
  try {
    const response = await fetch(url, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        message,
        answers
      }),
      signal: AbortSignal.timeout(120000), // 120s timeout
    });

    if (!response.ok) {
      throw new Error(`HTTP ${response.status}: ${response.statustext}`);
    }

    const data = await response.json();
    return data.reply || '(Aucune réponse)';
  } catch (error) {
    console.error('Erreur sendMessage:', error);
    throw new Error(`Erreur d'appel API: ${error.message}`);
  }
}

/**
 * Construit le prompt avec le profil utilisateur
 */
export function buildPrompt(userMessage, answers) {
  const profileLines = Object.entries(answers)
    .filter(([_, value]) => value && String(value).trim())
    .map(([key, value]) => `- ${key}: ${value}`);

  const header = profileLines.length > 0
    ? `Réponses validées (profil utilisateur):\n${profileLines.join('\n')}\n\n`
    : '';

  return `${header}Question utilisateur: ${userMessage}`.trim();
}
