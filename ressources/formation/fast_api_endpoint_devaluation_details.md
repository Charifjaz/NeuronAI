# FastAPI – Endpoint d’évaluation : explications détaillées

Ce document explique en profondeur deux éléments de ton code :

1) Le modèle d’entrée Pydantic avec `Field(..., description=...)`  
2) Le décorateur FastAPI `@router.post("", response_model=AssessmentOutput)`

Il inclut : définitions, comportements, différences 400 vs 422, exemples de requêtes/réponses, validations avancées, tests, et conseils d’ingénierie.

---

## 0) Rappel du code

```python
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Dict, Any
from ..services.llm import llm_client

router = APIRouter(prefix="/assessments", tags=["assessments"])

class AssessmentInput(BaseModel):
    answers: Dict[str, Any] = Field(..., description="Mapping question_id -> value")

class AssessmentOutput(BaseModel):
    summary: str

@router.post("", response_model=AssessmentOutput)
async def create_assessment(payload: AssessmentInput):
    if not payload.answers:
        raise HTTPException(status_code=400, detail="answers is required")
    summary = await llm_client.analyze_answers(payload.answers)
    return AssessmentOutput(summary=summary)
```

---

## 1) Pydantic : `Field` et l’ellipsis `...`

### 1.1 Qu’est-ce que `Field` ?
`Field` vient de **Pydantic** et sert à **configurer** un champ de modèle :
- **Présence / défaut** : valeur par défaut, obligatoire, ou générée via `default_factory`.
- **Contraintes** (selon le type) : `min_length`, `max_length`, `ge`, `le`, `pattern`, etc.
- **Métadonnées** : `description`, `examples`, `title`, `deprecated`, `alias`… (affichées dans la doc OpenAPI/Swagger).

Exemples rapides :
```python
name: str = Field(..., description="Nom complet")                # requis
age: int = Field(0, ge=0, description="Âge en années")           # défaut=0, contrainte ge=0
tags: list[str] = Field(default_factory=list)                     # défaut = nouvelle liste vide
```

### 1.2 Que signifie `...` (ellipsis) dans `Field(...)` ?
Le littéral `...` (ellipsis) indique à Pydantic : **« champ requis »**.

- `Field(..., ...)` ⇒ champ **obligatoire** (aucun défaut).  
- `Field(None, ...)` ⇒ défaut = `None` (si typé en `Optional[...]`, le champ devient optionnel et peut être `null`).  
- `Field({}, ...)` ou `default_factory=dict` ⇒ champ **optionnel** avec défaut `{}`.

Dans ton code :
```python
answers: Dict[str, Any] = Field(..., description="...")
```
`answers` est **requis** : s’il manque, FastAPI renvoie **422 Unprocessable Entity** (erreur de **validation de schéma**).

### 1.3 Rôle de `description="..."`
La description est **documentaire** : elle apparaît dans Swagger/Redoc et aide les consommateurs de l’API.

---

## 2) Structure et typage de `answers: Dict[str, Any]`

### 2.1 Intuition
- **Python** : un `dict` avec **clé `str`** et **valeur de n’importe quel type** (`Any`).
- **JSON** : un **objet** (`{}`) avec clés chaîne de caractères (IDs de questions) et valeurs potentiellement hétérogènes : `string`, `number`, `boolean`, `null`, **objet**, **liste**…

### 2.2 Exemples **valides**
```json
{
  "answers": {
    "q1": "Je préfère Python",
    "q2": 5,
    "q3": {"topic": "ML", "level": "intermediate"},
    "q4": ["numpy", "pandas"],
    "q5": true
  }
}
```

### 2.3 Exemple **invalide** (mauvais type pour `answers`)
```json
{ "answers": "pas un objet" }
```
→ 422 : on attendait un **objet JSON** (dict), pas une chaîne.

### 2.4 Choix `Any` : avantages et limites
- **Avantage** : souplesse pour des questionnaires hétérogènes.  
- **Limite** : validation plus faible. Si tu connais la forme attendue, préfère **typer plus strictement** (meilleurs messages d’erreur, meilleure doc).

#### Variante typée (ex.)
```python
from typing import Union, Literal, Any

AnswerValue = Union[str, int, float, bool, None, dict[str, Any], list[str]]

class AssessmentInput(BaseModel):
    answers: dict[str, AnswerValue] = Field(..., description="Mapping question_id -> value")
```

#### Variante avec modèle imbriqué (ex.)
```python
class Q3Detail(BaseModel):
    topic: str
    level: Literal["beginner", "intermediate", "advanced"]

class AssessmentInput(BaseModel):
    answers: dict[str, Union[str, int, Q3Detail]]
```

---

## 3) 400 vs 422 : logique métier vs validation de schéma

Dans ta fonction :
```python
if not payload.answers:
    raise HTTPException(status_code=400, detail="answers is required")
```
- Le champ `answers` **existe** et a le bon **type** (donc la validation Pydantic est OK),
- Mais il est **vide** (`{}`) → tu refuses pour **raison métier** : **400 Bad Request**.

Si tu veux que **Pydantic** rejette aussi `{}` (et donc renvoyer **422**), ajoute un validateur :

**Pydantic v2**
```python
from pydantic import field_validator

class AssessmentInput(BaseModel):
    answers: Dict[str, Any] = Field(..., description="...")

    @field_validator("answers")
    @classmethod
    def must_not_be_empty(cls, v):
        if not v:
            raise ValueError("answers must not be empty")
        return v
```

**Pydantic v1**
```python
from pydantic import validator

class AssessmentInput(BaseModel):
    answers: Dict[str, Any] = Field(..., description="...")

    @validator("answers")
    def must_not_be_empty(cls, v):
        if not v:
            raise ValueError("answers must not be empty")
        return v
```

---

## 4) FastAPI : `@router.post("", response_model=AssessmentOutput)`

### 4.1 Décorateur HTTP
- `@router.post` déclare un **endpoint POST**.
- Le chemin `""` (chaîne vide) signifie : **utiliser exactement le préfixe** du routeur. Avec `prefix="/assessments"`, l’URL finale est :

```
POST /assessments
```

(Si tu avais `@router.post("/create")`, ce serait `POST /assessments/create`.)

### 4.2 `response_model=AssessmentOutput`
- FastAPI **valide** et **sérialise** la réponse selon `AssessmentOutput`.
- Filtre les champs non déclarés, convertit les types si possible.
- Expose automatiquement le schéma de sortie dans **OpenAPI/Swagger** → meilleure DX et clients générés.

**Modèle de sortie :**
```python
class AssessmentOutput(BaseModel):
    summary: str
```
**Ex. de réponse JSON :**
```json
{ "summary": "L’apprenant préfère Python, niveau intermédiaire en ML" }
```

### 4.3 Diagramme de flux (texte)
```
Client → POST /assessments (JSON)
             │
             ▼
  FastAPI parse & valide payload → AssessmentInput
             │ (422 si invalide)
             ▼
   create_assessment(payload)
             │
             ▼
   summary = await llm_client.analyze_answers(...)
             │
             ▼
  return AssessmentOutput(summary=summary)
             │
             ▼
  FastAPI valide & sérialise la réponse (response_model)
             │
             ▼
       HTTP 200 + JSON conforme
```

---

## 5) Exemples de requêtes / réponses

### 5.1 Requête OK
```bash
curl -X POST http://localhost:8000/assessments \
  -H "Content-Type: application/json" \
  -d '{
    "answers": {
      "q1": "Je préfère Python",
      "q2": 5,
      "q3": {"topic": "ML", "level": "intermediate"},
      "q4": ["numpy", "pandas"],
      "q5": true
    }
  }'
```

**Réponse 200**
```json
{ "summary": "L’apprenant préfère Python, niveau intermédiaire en ML, score global 5/10" }
```

### 5.2 Erreur de schéma (422)
```bash
curl -X POST http://localhost:8000/assessments \
  -H "Content-Type: application/json" \
  -d '{ "answers": "pas un objet" }'
```
**Réponse 422** (ex. abrégé)
```json
{
  "detail": [
    {
      "type": "dict_type",
      "loc": ["body", "answers"],
      "msg": "Input should be a valid dictionary",
      "input": "pas un objet"
    }
  ]
}
```

### 5.3 Erreur métier (400, answers vide)
```bash
curl -X POST http://localhost:8000/assessments \
  -H "Content-Type: application/json" \
  -d '{ "answers": {} }'
```
**Réponse 400**
```json
{ "detail": "answers is required" }
```

---

## 6) Version robuste (timeouts & erreurs LLM)

```python
import asyncio
from fastapi import status

@router.post("", response_model=AssessmentOutput)
async def create_assessment(payload: AssessmentInput):
    if not payload.answers:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="answers must not be empty")

    try:
        summary = await asyncio.wait_for(
            llm_client.analyze_answers(payload.answers),
            timeout=20
        )
    except asyncio.TimeoutError:
        raise HTTPException(status_code=status.HTTP_504_GATEWAY_TIMEOUT, detail="LLM timeout")
    except llm_client.UpstreamError as e:  # exemple d’exception spécifique
        raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY, detail=f"Upstream error: {e}")

    return AssessmentOutput(summary=summary)
```

> Astuce : adapte le `timeout` à ton SLO et journalise l’erreur côté serveur (observabilité).

---

## 7) OpenAPI : aperçu généré (illustratif)

```yaml
/assessments:
  post:
    tags: [assessments]
    summary: Create Assessment
    requestBody:
      required: true
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/AssessmentInput'
    responses:
      '200':
        description: Successful Response
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/AssessmentOutput'
components:
  schemas:
    AssessmentInput:
      type: object
      properties:
        answers:
          type: object
          additionalProperties: true
          description: Mapping question_id -> value
      required: [answers]
    AssessmentOutput:
      type: object
      properties:
        summary:
          type: string
      required: [summary]
```

---

## 8) Tests rapides avec `TestClient`

```python
from fastapi.testclient import TestClient
from myapp.main import app  # ou assemble router→app et importe-la

client = TestClient(app)

def test_assessment_ok(mocker):
    mocker.patch("myapp.services.llm.llm_client.analyze_answers", return_value="OK")
    resp = client.post("/assessments", json={"answers": {"q1": "X"}})
    assert resp.status_code == 200
    assert resp.json() == {"summary": "OK"}

def test_schema_error():
    resp = client.post("/assessments", json={"answers": "oops"})
    assert resp.status_code == 422

def test_business_error():
    resp = client.post("/assessments", json={"answers": {}})
    assert resp.status_code == 400
```

---

## 9) Bonnes pratiques
- **Typer plus strictement** si la forme de `answers` est connue (meilleure DX, meilleure doc, moins d’ambiguïtés).
- **Séparer logique métier / I/O** : garde `llm_client` encapsulé et teste-le isolément.
- **Gestion d’erreurs explicite** pour les dépendances externes (timeouts, codes 5xx appropriés).
- **Observabilité** : log, métriques (latence LLM), corrélation requêtes.
- **Sécurité** : taille max de payload, limitation du nombre d’items dans `answers`, sanitation si nécessaire.

---

## 10) TL;DR
- `Field(..., ...)` ⇒ champ **requis** + métadonnées/contraintes.
- `answers: Dict[str, Any]` ⇒ **objet JSON** clé (string) → valeur de **tout type**.
- `@router.post("", response_model=...)` ⇒ crée **POST /assessments** et **valide la réponse** selon `AssessmentOutput`.
- **422** = schéma invalide (Pydantic) ; **400** = schéma OK mais contenu **métier** refusé (ex. `{}`).

