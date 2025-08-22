import streamlit as st
from src.utils import read_pdf, clean_text, chunk_text, highlight_answer
from src.embeddings import load_embedding_model, embed_texts, VectorStore
from src.llm import get_openai_client, build_rag_prompt, call_llm

# ------------------------------
# CONFIG STREAMLIT
# ------------------------------
st.set_page_config(page_title="Lecteur PDF Intelligent (RAG)", page_icon="📄", layout="wide")
st.title("📄 Lecteur PDF Intelligent (RAG)")
st.caption("Chargez vos PDF et posez vos questions.")

# --- State init ---
st.session_state.setdefault("OPENAI_API_KEY", None)
st.session_state.setdefault("last_passage", None)
st.session_state.setdefault("last_question", "")
st.session_state.setdefault("last_answer", "")

# ------------------------------
#  Interface utilisateur
# ------------------------------
col1, col2 = st.columns([1, 2])

with col1:
    st.header("📂 Préparation")
    files = st.file_uploader("Importer des PDF", type=["pdf"], accept_multiple_files=True)
    build = st.button("📚 Indexer le document")
    st.markdown(
        "🔑 Pour générer une clé OpenAI : "
        "[https://platform.openai.com/api-keys](https://platform.openai.com/api-keys)"
    )
    api_input = st.text_input("Entrer clé OpenAI", type="password")
    if api_input:
        st.session_state.OPENAI_API_KEY = api_input
        st.success("Clé enregistrée en session.")

    if build and files:
        with st.spinner("📚 Construction de l'index..."):
            corpus = "\n\n".join([clean_text(read_pdf(f)) for f in files])
            chunks = chunk_text(corpus)
            model = load_embedding_model()
            vectors = embed_texts(model, chunks)
            vstore = VectorStore(vectors.shape[1])
            vstore.add(vectors, chunks)

            st.session_state.chunks = chunks
            st.session_state.vstore = vstore
            st.session_state.full_text = corpus
        st.success("Index construit ✅")

with col2:
    st.header("💬 Questions")
    user_q = st.chat_input("Votre question…")

    c1, c2 = st.columns([1, 1])
    with c1:
        highlight_btn = st.button("🖍️ Surligner passage pertinent")
    with c2:
        summary_btn = st.button("📝 Résumer le PDF")

    # --- Nouvelle question ---
    if user_q and "vstore" in st.session_state:
        with st.spinner("🤔 Recherche et génération..."):
            model = load_embedding_model()
            qvec = embed_texts(model, [user_q])[0]
            hits = st.session_state.vstore.search(qvec, top_k=5)

            best_idx, _ = hits[0]
            best_excerpt = st.session_state.chunks[best_idx]

            client = get_openai_client()
            prompt = build_rag_prompt(user_q, [best_excerpt])
            answer = call_llm(client, prompt)

        st.chat_message("user").markdown(user_q)
        st.chat_message("assistant").markdown(answer)

        st.session_state.last_passage = best_excerpt
        st.session_state.last_answer = answer

    # --- Surlignage ---
    if highlight_btn and st.session_state.get("last_passage"):
        st.subheader("🖍️ Passage pertinent")
        extrait = st.session_state.last_passage
        answer = st.session_state.last_answer
        st.markdown(highlight_answer(extrait, answer), unsafe_allow_html=True)

    # --- Résumé ---
    if summary_btn and "full_text" in st.session_state:
        st.subheader("Résumé du PDF")
        client = get_openai_client()
        if client:
            prompt = f"Fais un résumé concis du texte suivant en français:\n{st.session_state.full_text}"
            summary = call_llm(client, prompt)
            st.markdown(summary)
        else:
            st.warning("⚠️ Pas de clé OpenAI.")
