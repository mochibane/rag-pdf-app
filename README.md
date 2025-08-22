# 📘 RAG PDF App (Streamlit)

Application **Question/Réponse sur PDF** basée sur **LLMs OpenAI**, développée avec **Streamlit**.  
Elle permet de :  
- Importer un PDF et créer un index local (RAG).  
- Poser des questions en langage naturel sur le PDF.  
- Générer un résumé du PDF.  
- Mettre en évidence les passages pertinents liés à la réponse.  
- Utiliser une clé OpenAI via saisie directe dans l’interface.

---

## 🚀 Fonctionnalités
- 📂 **Upload de PDF** depuis l’interface.  
- ❓ **Questions sur le PDF** avec réponses contextuelles.  
- 📑 **Résumé automatique** du PDF.  
- 🖍️ **Surlignage des passages pertinents**.  
- 🔑 **Gestion flexible de la clé OpenAI**   

---

## 📸 Aperçu de l’application

![Aperçu de l'application](img.gif)

---

## 📁 Structure du projet
```bash
rag-pdf-app/
│
├── app.py                      # Interface Streamlit
├── src/
│   ├── utils.py          # Fonctions utilitaires (PDF, nettoyage, chunking, highlight)
│   ├── embeddings.py     # Gestion embeddings + VectorStore
│   ├── llm.py            # Appels OpenAI + génération de prompts
│
└── README.md
```

---
## 🛠️ Installation

### 1. Cloner le projet
```bash
git clone https://github.com/mochibane/rag-pdf-app.git
cd rag-pdf-app
```
### 2. Créer un environnement virtuel (recommandé)
```bash
python -m venv venv
source venv/bin/activate        # Sur macOS/Linux
venv\Scripts\activate           # Sur Windows
```
### 3. Installer les dépendances
```bash
pip install -r requirements.txt
```
### 4. Lancer l’application 
```bash
streamlit run app.py
```
---
### L'application sera accessible sur **http://localhost:8501**
