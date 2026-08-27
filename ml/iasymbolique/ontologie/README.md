# Ontologie & Graphe de Connaissances — ORIENT'IA

Ce module constitue la composante d'**IA Symbolique** du projet, conformément à l'Article 12 du sujet. Elle permet d'ajouter une couche de raisonnement logique, d'explicabilité et de vérification de prérequis au-dessus du modèle statistique (Machine Learning).

## 1. Structure du Graphe
L'ontologie relie les concepts clés de l'orientation à l'ISPM :
*   **Étudiant** : Profil, notes, série de Bac, intérêts.
*   **Parcours & Mention** : L'offre de formation officielle (16 parcours).
*   **Matière** : Programme universitaire et matières de lycée.
*   **Compétence & Métier** : Relations sémantiques entre apprentissage et débouchés.
*   **Prérequis** : Séries de Baccalauréat admises par parcours.

## 2. Rôle dans l'Architecture Hybride
L'ontologie n'est pas seulement un document passif ; elle est activement utilisée par le backend (FastAPI) comme **moteur d'inférence** :
1.  **Vérification Croisée** : Lors d'une recommandation ML, le système interroge l'ontologie pour vérifier si la série de Bac du candidat est administrativement compatible avec le parcours suggéré.
2.  **Explicabilité (XAI)** : Le graphe permet de retrouver les "ponts" logiques (ex: "Vous aimez les Maths" -> "Ce parcours enseigne les Maths") pour justifier la réponse.
3.  **Aide à la Décision** : Détection automatique des incohérences entre le profil réel et les prérequis officiels.

## 3. Utilisation & Scripts
*   `scripts/build_ontology.py` : Construit le graphe à partir du corpus JSON et du dataset de profils.
*   `scripts/run_queries_demo.py` : Exécute 6 scénarios de raisonnement (SPARQL) démontrant la valeur ajoutée de l'extension (validation des prérequis, suggestion de métiers, etc.).

## 4. Formats Disponibles
*   **Turtle (.ttl) / RDF/XML (.owl)** : Formats standards pour intégration dans des outils comme Protégé.
*   **Graph CSV (nodes/edges)** : Pour analyse via NetworkX ou Neo4j.
*   **JSON Compact (`full_kb.json`)** : Utilisé par le backend FastAPI pour des recherches ultra-rapides.

## 5. Cas d'Usage Démontrés (Article 12)
1.  Vérification automatique des prérequis de Bac.
2.  Explication logique d'une recommandation.
3.  Parcours des relations formations ↔ métiers.
4.  Détection d'incohérences de parcours.
5.  Calcul d'un score de recoupement symbolique.
6.  Raisonnement multi-étape (Étudiant → Matière → Parcours → Métier).

---
**Note sur l'hébergement** : Cette base de connaissance est synchronisée avec l'API backend distante pour garantir que les conseils de l'assistant ORIENT'IA sont toujours conformes aux référentiels officiels de l'ISPM.
