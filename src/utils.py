import io
import re
from typing import List
from pypdf import PdfReader

def read_pdf(file: io.BytesIO) -> str:
    """Lit un PDF et retourne le texte extrait."""
    reader = PdfReader(file)
    texts = [page.extract_text() or "" for page in reader.pages]
    return "\n".join(texts)

def clean_text(s: str) -> str:
    """Supprime les espaces et lignes vides inutiles."""
    return "\n".join([line.strip() for line in s.splitlines() if line.strip()])

def chunk_text(text: str, chunk_size: int = 800, overlap: int = 120) -> List[str]:
    """Découpe le texte en chunks avec chevauchement."""
    words = text.split()
    chunks, step, i = [], max(1, chunk_size - overlap), 0
    while i < len(words):
        chunks.append(" ".join(words[i:i + chunk_size]))
        i += step
    return chunks

def highlight_answer(excerpt: str, answer: str) -> str:
    """Surligne les mots-clés de la réponse dans un passage."""
    words = re.findall(r"\b\w+\b", answer.lower())
    keywords = {w for w in words if len(w) > 3}

    def repl(m):
        w = m.group(0)
        return f"<mark>{w}</mark>" if w.lower() in keywords else w

    highlighted = re.sub(r"\b\w+\b", repl, excerpt)
    return (
        "<div style='background-color:#fff3b0;padding:8px;border-radius:8px;margin-bottom:8px;'>"
        + highlighted + "</div>"
    )
