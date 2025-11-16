/**
 * Script de test pour vérifier la compatibilité de l'API backend
 * Exécuter avec: node test-api.js
 */

const API_BASE_URL = process.env.VITE_API_BASE_URL || 'http://localhost:8000';

// Couleurs pour la console
const colors = {
    reset: '\x1b[0m',
    green: '\x1b[32m',
    red: '\x1b[31m',
    yellow: '\x1b[33m',
    cyan: '\x1b[36m',
};

function log(message, color = colors.reset) {
    console.log(`${color}${message}${colors.reset}`);
}

async function testEndpoint(name, url, options = {}) {
    try {
        log(`\n🔍 Test: ${name}`, colors.cyan);
        log(`   URL: ${url}`);
        
        const response = await fetch(url, {
            ...options,
            headers: {
                'Content-Type': 'application/json',
                ...options.headers,
            },
        });

        log(`   Status: ${response.status}`, response.ok ? colors.green : colors.red);

        if (!response.ok) {
            log(`   ❌ Échec: ${response.statusText}`, colors.red);
            return false;
        }

        const data = await response.json();
        log(`   ✅ Réponse reçue`, colors.green);
        
        if (options.validate) {
            const isValid = options.validate(data);
            if (!isValid) {
                log(`   ⚠️  Format de réponse invalide`, colors.yellow);
                return false;
            }
            log(`   ✅ Format validé`, colors.green);
        }

        return true;
    } catch (error) {
        log(`   ❌ Erreur: ${error.message}`, colors.red);
        return false;
    }
}

async function runTests() {
    log('\n🧪 Tests de compatibilité API', colors.cyan);
    log('='.repeat(50), colors.cyan);
    log(`Base URL: ${API_BASE_URL}\n`);

    const results = {
        passed: 0,
        failed: 0,
    };

    // Test 1: GET /questions
    const test1 = await testEndpoint(
        'GET /questions',
        `${API_BASE_URL}/questions`,
        {
            validate: (data) => {
                if (!Array.isArray(data)) {
                    log(`      Format attendu: Array`, colors.yellow);
                    log(`      Format reçu: ${typeof data}`, colors.yellow);
                    return false;
                }
                
                if (data.length === 0) {
                    log(`      ⚠️  Tableau vide`, colors.yellow);
                }

                // Vérifier le format des questions
                const firstQuestion = data[0];
                if (firstQuestion && !firstQuestion.id) {
                    log(`      ⚠️  Question sans 'id'`, colors.yellow);
                    return false;
                }

                log(`      ${data.length} question(s) trouvée(s)`, colors.green);
                return true;
            },
        }
    );
    test1 ? results.passed++ : results.failed++;

    // Test 2: POST /ask
    const test2 = await testEndpoint(
        'POST /ask',
        `${API_BASE_URL}/ask`,
        {
            method: 'POST',
            body: JSON.stringify({
                message: 'Test message',
                answers: {
                    context: 'Test context',
                },
            }),
            validate: (data) => {
                if (!data.reply) {
                    log(`      ⚠️  Réponse sans champ 'reply'`, colors.yellow);
                    return false;
                }
                log(`      Réponse reçue: "${data.reply.substring(0, 50)}..."`, colors.green);
                return true;
            },
        }
    );
    test2 ? results.passed++ : results.failed++;

    // Résumé
    log('\n' + '='.repeat(50), colors.cyan);
    log('📊 Résultats des tests:', colors.cyan);
    log(`   ✅ Réussis: ${results.passed}`, colors.green);
    log(`   ❌ Échecs: ${results.failed}`, results.failed > 0 ? colors.red : colors.green);

    if (results.failed === 0) {
        log('\n🎉 Tous les tests sont passés !', colors.green);
        log('   Votre backend est compatible avec l\'interface React', colors.green);
    } else {
        log('\n⚠️  Certains tests ont échoué', colors.yellow);
        log('   Vérifiez la configuration de votre backend', colors.yellow);
    }

    log('');
}

// Vérifier que fetch est disponible (Node 18+)
if (typeof fetch === 'undefined') {
    log('❌ fetch n\'est pas disponible', colors.red);
    log('   Utilisez Node.js 18 ou supérieur', colors.yellow);
    log('   Ou installez node-fetch: npm install node-fetch', colors.yellow);
    process.exit(1);
}

// Exécuter les tests
runTests().catch((error) => {
    log(`\n❌ Erreur fatale: ${error.message}`, colors.red);
    process.exit(1);
});
