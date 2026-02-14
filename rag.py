import os
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from pypdf import PdfReader

DATA_DIR = "data"
EMBED_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

embedder = SentenceTransformer(EMBED_MODEL)

documents = []
embeddings = []

def split_text(text, size=400):
    return [text[i:i+size] for i in range(0, len(text), size)]

def load_documents():
    global documents, embeddings

    for fname in os.listdir(DATA_DIR):
        path = os.path.join(DATA_DIR, fname)

        if fname.lower().endswith(".txt"):
            with open(path, "r", encoding="utf-8", errors="ignore") as f:
                text = f.read()

        elif fname.lower().endswith(".pdf"):
            reader = PdfReader(path)
            text = ""
            for page in reader.pages:
                text += page.extract_text() or ""

        else:
            continue

        chunks = split_text(text)
        documents.extend(chunks)
        embeddings.extend(embedder.encode(chunks))

    if not embeddings:
        return None

    dim = len(embeddings[0])
    index = faiss.IndexFlatL2(dim)
    index.add(np.array(embeddings).astype("float32"))
    return index

index = load_documents()

def search_docs(query, top_k=2):
    if index is None:
        return []

    q_emb = embedder.encode([query]).astype("float32")
    _, idxs = index.search(q_emb, top_k)
    return [documents[i] for i in idxs[0]]
