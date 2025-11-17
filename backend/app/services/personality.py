from typing import Dict, Any, List


def infer_personality_from_answers(answers: Dict[str, Any]) -> str:
    """
    Déduit un petit profil de personnalité cognitive à partir des réponses aux Q1...Q7.
    `answers` est un dict du type :
    {
        "Q1": "En faisant un plan ou un tableau",
        "Q2": "🧩 Un puzzle où il manque encore une pièce",
        ...
    }

    Pour Q4 (plusieurs choix possibles), la valeur peut être une string ou une liste de strings.
    """
    # Scores par "dimension"
    traits = {
        "structure": 0,
        "visuel": 0,
        "verbal": 0,
        "logique": 0,
        "expérimental": 0,
        "intuitif": 0,
    }

    def add(trait: str, w: float = 1.0):
        if trait in traits:
            traits[trait] += w

    def normalize_answer(val: Any) -> List[str]:
        """
        Normalise une réponse en liste de strings (pour gérer Q4 avec plusieurs choix).
        """
        if isinstance(val, list):
            return [str(v) for v in val]
        if val is None:
            return []
        return [str(val)]

    # --- Q1 ---
    for val in normalize_answer(answers.get("Q1")):
        v = val.lower()
        if "plan" in v or "tableau" in v:
            add("structure", 2)
            add("logique", 1)
        elif "image" in v or "métaphore" in v:
            add("visuel", 2)
        elif "comparant des options" in v or "critères" in v or "comparant" in v:
            add("logique", 2)
            add("structure", 1)
        elif "en parlant" in v:
            add("verbal", 2)
        elif "laissant poser" in v or "revenant plus tard" in v:
            add("intuitif", 2)

    # --- Q2 ---
    for val in normalize_answer(answers.get("Q2")):
        v = val.lower()
        if "brume" in v:
            add("intuitif", 1)
        elif "puzzle" in v:
            add("logique", 2)
        elif "porte" in v:
            add("intuitif", 1)
        elif "vague d'idées" in v or "vague d’idées" in v:
            add("visuel", 1)
            add("intuitif", 1)
        elif "carte" in v or "directions" in v:
            add("structure", 1)
            add("visuel", 1)

    # --- Q3 ---
    for val in normalize_answer(answers.get("Q3")):
        v = val.lower()
        if "relis calmement" in v or "relis" in v:
            add("structure", 1)
        elif "exemple" in v or "version plus simple" in v:
            add("expérimental", 1)
            add("logique", 1)
        elif "tableau" in v:
            add("structure", 2)
        elif "passe à autre chose" in v or "j’y reviens" in v or "jy reviens" in v:
            add("intuitif", 2)
        elif "regard extérieur" in v:
            add("verbal", 1)

    # --- Q4 (plusieurs choix possibles) ---
    for val in normalize_answer(answers.get("Q4")):
        v = val.lower()
        if "expliquer simplement" in v:
            add("verbal", 1)
        elif "appliquer tout de suite" in v:
            add("expérimental", 2)
        elif "visualise clairement" in v:
            add("visuel", 2)
        elif "résumer en 3 points" in v:
            add("structure", 2)
        elif "exemple concret" in v:
            add("expérimental", 1)
            add("logique", 1)
        elif "autre" in v:
            add("intuitif", 0.5)  # neutre

    # --- Q5 ---
    for val in normalize_answer(answers.get("Q5")):
        v = val.lower()
        if "essentiel tout de suite" in v:
            add("structure", 1)
        elif "pas-à-pas" in v or "exemples concrets" in v:
            add("expérimental", 2)
            add("structure", 1)
        elif "explication complète" in v or "logique et les détails" in v:
            add("logique", 2)
        elif "analogie" in v or "image qui parle" in v:
            add("visuel", 2)
        elif "s’adapte" in v or "s adapte" in v:
            add("intuitif", 1)

    # --- Q6 ---
    for val in normalize_answer(answers.get("Q6")):
        v = val.lower()
        if "décortiquer" in v or "fond" in v:
            add("logique", 2)
        elif "improviser" in v:
            add("intuitif", 2)
        elif "tester" in v or "ajuster" in v:
            add("expérimental", 2)
        elif "laisser venir le déclic" in v or "déclic" in v:
            add("intuitif", 2)
        elif "logique sous-jacente" in v:
            add("logique", 2)

    # --- Q7 ---
    for val in normalize_answer(answers.get("Q7")):
        v = val.lower()
        if "visualisant" in v or "visualiser" in v:
            add("visuel", 2)
        elif "écrivant" in v or "dessinant" in v or "écriture" in v:
            add("structure", 1)
            add("visuel", 1)
        elif "en parlant" in v or "expliquer" in v:
            add("verbal", 2)
        elif "observant attentivement" in v:
            add("expérimental", 1)
            add("visuel", 1)
        elif "logique qui relie" in v or "logique" in v:
            add("logique", 2)

    # ---- Construction du texte de personnalité ----
    # On trie les traits par importance
    sorted_traits = sorted(traits.items(), key=lambda kv: kv[1], reverse=True)
    # On garde uniquement ceux qui ont un score significatif
    dominant = [t for t, score in sorted_traits if score >= 2]

    descriptions = []

    if "structure" in dominant:
        descriptions.append(
            "tu apprécies les explications structurées, avec des étapes claires ou des synthèses en quelques points"
        )
    if "visuel" in dominant:
        descriptions.append(
            "tu es très sensible aux images, métaphores et visualisations pour comprendre et mémoriser"
        )
    if "verbal" in dominant:
        descriptions.append(
            "le fait d’expliquer à l’oral ou d’échanger t’aide beaucoup à clarifier tes idées"
        )
    if "logique" in dominant:
        descriptions.append(
            "tu as un profil analytique : tu cherches la logique, les liens et les critères qui structurent les choses"
        )
    if "expérimental" in dominant:
        descriptions.append(
            "tu apprends bien en testant, en voyant des exemples concrets et en appliquant rapidement"
        )
    if "intuitif" in dominant:
        descriptions.append(
            "tu laisses volontiers les idées maturer et tu fais confiance à tes intuitions et à tes déclics"
        )

    if not descriptions:
        # Cas où rien ne ressort fortement
        return (
            "Profil équilibré : tu peux t’adapter à plusieurs types d’explications, "
            "avec une préférence légère pour les exemples concrets et les explications claires."
        )

    # On assemble le tout dans un petit paragraphe
    personality_text = (
        "Profil de réflexion : "
        + "; ".join(descriptions)
        + "."
    )

    return personality_text
