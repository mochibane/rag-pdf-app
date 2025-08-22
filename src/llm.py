import os
import streamlit as st
from openai import OpenAI
from typing import List

def get_openai_client(api_key: str = None):
    """Initialise le client OpenAI avec une clé depuis l’env ou Streamlit."""
    key = api_key or st.session_state.get("OPENAI_API_KEY")
    if not key:
        key = st.secrets.get("OPENAI_API_KEY") or os.getenv("OPENAI_API_KEY")
    return OpenAI(api_key=key) if key else None

def build_rag_prompt(question: str, contexts: List[str], language: str = "fr") -> str:
    """Construit un prompt RAG avec les passages contextuels."""
    sources = "\n\n".join([f"[Source {i+1}]\n{c}" for i, c in enumerate(contexts)])
    return (
        f"Réponds en {language} uniquement à partir du CONTEXTE ci-dessous.\n"
        f"Ne rajoute pas d'informations extérieures.\n\n"
        f"CONTEXTE:\n{sources}\n\n"
        f"QUESTION:\n{question}\n"
    )

def call_llm(client: OpenAI, prompt: str, temperature: float = 0.2, max_tokens: int = 500) -> str:
    """Appelle le modèle OpenAI pour générer une réponse."""
    if not client:
        return "⚠️ Pas de clé OpenAI."
    resp = client.chat.completions.create(
        model="gpt-4o-mini",
        temperature=temperature,
        max_tokens=max_tokens,
        messages=[
            {"role": "system", "content": "Tu es un assistant utile et factuel."},
            {"role": "user", "content": prompt},
        ],
    )
    return resp.choices[0].message.content
