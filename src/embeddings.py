import numpy as np
from typing import List
from sklearn.neighbors import NearestNeighbors
from sentence_transformers import SentenceTransformer
import streamlit as st

@st.cache_resource(show_spinner=False)
def load_embedding_model():
    """Charge et met en cache le modèle d'embeddings."""
    return SentenceTransformer("all-MiniLM-L6-v2")

def embed_texts(model, texts: List[str]):
    """Encode une liste de textes en vecteurs normalisés."""
    return model.encode(texts, show_progress_bar=False, normalize_embeddings=True)

class VectorStore:
    """Stocke des vecteurs et permet la recherche de similarité."""

    def __init__(self, dim: int):
        self.dim = dim
        self.texts: List[str] = []
        self.vectors: List[np.ndarray] = []
        self.nn = None

    def add(self, vectors, payloads: List[str]):
        self.vectors.extend(vectors)
        self.texts.extend(payloads)
        self.nn = NearestNeighbors(
            n_neighbors=min(5, len(self.vectors)), metric="cosine"
        )
        self.nn.fit(np.array(self.vectors))

    def search(self, qvec, top_k: int = 5):
        if not self.nn:
            return []
        n_neighbors = min(max(1, top_k), len(self.vectors))
        distances, idx = self.nn.kneighbors([qvec], n_neighbors=n_neighbors)
        return [(int(i), 1 - float(d)) for i, d in zip(idx[0], distances[0])]
