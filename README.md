# Julie-AI-Voice-Assistant
Hackathon project: Julie is an AI voice assistant for insurance call centers that handles simple accident-related claims and frequently asked questions, and escalates complex cases to human agents.

# Julie-AI-Voice-Assistant

Julie est une solution d'assistance vocale intelligente dédiée aux centres d'appels d'assurance. Le système est conçu pour automatiser la gestion des sinistres simples (ex: bris de glace) et répondre aux questions fréquentes (FAQ), tout en assurant le transfert vers un agent humain pour les cas complexes.

---

## Sprint 1 : Développement du Squelette (Jours 1 à 5)
**Objectif :** Mise en place d'un prototype fonctionnel capable d'assurer le flux complet : Entrée vocale -> Transcription -> Réponse IA -> Sortie texte.

### Architecture Technique
* **Environnement de développement :** Cursor / Windsurf.
* **Traitement Audio (STT) :** Hugging Face Hub.
* **Moteur d'Intelligence (LLM) :** Groq (Méthodologie CO-STAR).
* **Interface Utilisateur :** Streamlit.

---

## Protocole d'Intégration (Contrat JSON)
Afin de garantir l'interopérabilité des modules développés en parallèle, l'ensemble des échanges de données doit se conformer strictement à la structure définie dans `contrat.json`.

**Paramètres obligatoires :**
* `transcription` : Résultat de la conversion voix-vers-texte (Expert Audio).
* `reponse_ia` : Contenu généré par le moteur LLM (Expert IA).
* `audio_url` : Chemin d'accès vers le flux de réponse vocale.
* `statut` : État du traitement (catégorisation : sinistre, faq, ou transfert).

---

## Organisation de l'Équipe

### Direction de Projet (Leader)
* Maintien du contrat technique.
* Coordination des livrables et validation de l'intégration globale.

### Expertise Audio (A)
* Implémentation du module Speech-to-Text (STT).
* Développement de la fonction de transcription.

### Expertise IA (B)
* Ingénierie de prompt et configuration du modèle de réponse via Groq.
* Logique de décision et de catégorisation des demandes.

### Développement Backend (C)
* Développement de l'API sous FastAPI.
* Orchestration des flux de données entre les différents modules.

### Développement Frontend (D)
* Conception de l'interface utilisateur sous Streamlit.
* Intégration des fonctions d'enregistrement et d'affichage.

---

## Méthodologie et Reporting
* **Daily Stand-up :** Réunion technique quotidienne à 09h00 pour le suivi des points de blocage.
* **Priorisation :** Focus exclusif sur le traitement des sinistres simples et la base de connaissances FAQ.
* **Plan de Continuité :** Migration vers Google AI Studio prévue au Jour 4 en cas de difficulté majeure sur le module audio.
