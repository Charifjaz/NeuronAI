/**
 * Service API pour communiquer avec le backend FastAPI
 */

const API_BASE_URL = "http://localhost:8000";

const QUESTIONS = [
  {
    id: "Q1",
    type: "select",
    label: "Quand tu réfléchis à quelque chose d'important, qu'est-ce qui t'aide le plus à y voir clair ?",
    options: [
      "En faisant un plan ou un tableau",
      "En trouvant une image ou une métaphore",
      "En comparant des options avec des critères",
      "En en parlant pour poser les idées",
      "En laissant poser et en y revenant plus tard"
    ]
  },
  {
    id: "Q2",
    type: "select",
    label: "Si tu devais représenter ta réflexion du moment, ce serait plutôt…",
    options: [
      "Une brume qui se dissipe",
      "Un puzzle où il manque encore une pièce",
      "Une porte à franchir",
      "Une vague d'idées à canaliser",
      "Une carte avec plusieurs directions possibles"
    ]
  },
  {
    id: "Q3",
    type: "select",
    label: "Quand une idée ou une décision ne te semble pas encore claire, que fais-tu le plus souvent ?",
    options: [
      "Je relis calmement ce que j'ai déjà posé",
      "Je cherche un exemple ou une version plus simple",
      "Je mets tout à plat dans un tableau",
      "Je passe à autre chose puis j'y reviens",
      "Je demande un regard extérieur"
    ]
  },
  {
    id: "Q4",
    type: "multiple",
    label: "Quand tu comprends quelque chose en profondeur, qu'est-ce qui te le montre ? (plusieurs choix possibles)",
    options: [
      "Je peux l'expliquer simplement",
      "Je peux l'appliquer tout de suite",
      "Je le visualise clairement",
      "Je peux le résumer en 3 points",
      "Je peux donner un exemple concret",
      "Autre (préciser)"
    ]
  },
  {
    id: "Q5",
    type: "select",
    label: "Quand on t'explique quelque chose, tu préfères plutôt…",
    options: [
      "Avoir l'essentiel tout de suite",
      "Un pas-à-pas avec exemples concrets",
      "Une explication complète avec la logique et les détails",
      "Une analogie / une image qui parle",
      "Une version qui s'adapte selon ce que tu demandes"
    ]
  },
  {
    id: "Q6",
    type: "select",
    label: "Devant une situation qui demande un peu de réflexion, ton réflexe naturel, c'est plutôt…",
    options: [
      "Décortiquer pour comprendre le fond",
      "Improviser et voir ce qui émerge",
      "Tester, observer, ajuster",
      "Laisser venir le déclic",
      "Chercher d'abord la logique sous-jacente"
    ]
  },
  {
    id: "Q7",
    type: "select",
    label: "Par quel chemin passes-tu spontanément pour apprendre et comprendre ?",
    options: [
      "En visualisant comment les choses se passent concrètement",
      "En écrivant ou dessinant les idées",
      "En en parlant pour l'expliquer",
      "En observant attentivement jusqu'à ce que tout prenne sens",
      "En cherchant la logique qui relie tout"
    ]
  }
];

/**
 * Génère un user_id unique ou le récupère du localStorage
 */
export function getUserId() {
  let userId = localStorage.getItem("user_id");
  if (!userId) {
    userId = `user_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
    localStorage.setItem("user_id", userId);
  }
  return userId;
}

/**
 * Récupère la liste des questions (mockées en dur)
 */
export async function fetchQuestions() {
  return QUESTIONS;
}

/**
 * Valide le profil et envoie les réponses au backend
 */
export async function validateProfile(answers) {
  const userId = getUserId();
  const url = `${API_BASE_URL}/profile`;
  
  const payload = {
    user_id: userId,
    Q1: answers.Q1,
    Q2: answers.Q2,
    Q3: answers.Q3,
    Q4: answers.Q4,
    Q5: answers.Q5,
    Q6: answers.Q6,
    Q7: answers.Q7
  };
  
  console.log("=== PAYLOAD ENVOYÉ ===", payload);
  
  try {
    const response = await fetch(url, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(payload),
      signal: AbortSignal.timeout(30000),
    });

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      console.error("Erreur backend:", errorData);
      throw new Error(`HTTP ${response.status}: ${response.statusText}`);
    }

    const data = await response.json();
    return data.personality;
  } catch (error) {
    console.error("Erreur validateProfile:", error);
    throw error;
  }
}

/**
 * Alias pour compatibilité
 */
export const createProfile = validateProfile;

/**
 * Récupère le profil existant
 */
export async function getProfile() {
  const userId = getUserId();
  const url = `${API_BASE_URL}/profile/${userId}`;
  
  try {
    const response = await fetch(url, {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
      },
      signal: AbortSignal.timeout(15000),
    });

    if (!response.ok) {
      if (response.status === 404) {
        return null;
      }
      throw new Error(`HTTP ${response.status}: ${response.statusText}`);
    }

    const data = await response.json();
    return data.personality;
  } catch (error) {
    console.error("Erreur getProfile:", error);
    return null;
  }
}

/**
 * Envoie un message au chat
 */
export async function sendMessage(message) {
  const userId = getUserId();
  const url = `${API_BASE_URL}/chat`;
  
  try {
    const response = await fetch(url, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        user_id: userId,
        question: message
      }),
      signal: AbortSignal.timeout(120000),
    });

    if (!response.ok) {
      throw new Error(`HTTP ${response.status}: ${response.statusText}`);
    }

    const data = await response.json();
    return data.answer || "(Aucune réponse)";
  } catch (error) {
    console.error("Erreur sendMessage:", error);
    throw new Error(`Erreur d'appel API: ${error.message}`);
  }
}

export { QUESTIONS };