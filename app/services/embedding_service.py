from sentence_transformers import SentenceTransformer

# load once
model = SentenceTransformer("all-MiniLM-L6-v2")

def embed_text(texts):
    try:
        embeddings = model.encode(texts)
        return embeddings.tolist()
    except Exception as e:
        print("❌ Embedding error:", e)
        return [[0.0]*384 for _ in texts]