import faiss
import numpy as np
import os
import pickle
import uuid


class VectorStore:
    def __init__(self, dim=384, index_path="faiss.index", meta_path="meta.pkl"):
        self.dim = dim
        self.index_path = index_path
        self.meta_path = meta_path

        # cosine similarity
        self.index = faiss.IndexFlatIP(dim)

        # storage
        self.id_to_text = {}
        self.id_to_metadata = {}

        self.ids = []  # maintains order

        self._load()

    # -------------------------
    # Normalize vectors
    # -------------------------
    def _normalize(self, vectors):
        vectors = np.array(vectors).astype("float32")
        faiss.normalize_L2(vectors)
        return vectors

    # -------------------------
    # Add embeddings
    # -------------------------
    def add(self, embeddings, texts, metadatas=None):
        embeddings = self._normalize(embeddings)

        if metadatas is None:
            metadatas = [{} for _ in texts]

        new_ids = [str(uuid.uuid4()) for _ in texts]

        for i, uid in enumerate(new_ids):
            self.id_to_text[uid] = texts[i]
            self.id_to_metadata[uid] = metadatas[i]

        self.ids.extend(new_ids)

        self.index.add(embeddings)

    # -------------------------
    # Search (improved filtering)
    # -------------------------
    def search(self, query_embedding, k=5, filter_fn=None):
        if self.index.ntotal == 0:
            return []

        query_embedding = self._normalize([query_embedding])

        # fetch more results for safe filtering
        search_k = k * 3

        D, I = self.index.search(query_embedding, search_k)

        results = []

        for idx, score in zip(I[0], D[0]):
            if idx == -1 or idx >= len(self.ids):
                continue

            uid = self.ids[idx]

            item = {
                "id": uid,
                "text": self.id_to_text[uid],
                "metadata": self.id_to_metadata[uid],
                "score": float(score)
            }

            if filter_fn is None or filter_fn(item["metadata"]):
                results.append(item)

            if len(results) >= k:
                break

        return results

    # -------------------------
    # Save
    # -------------------------
    def save(self):
        faiss.write_index(self.index, self.index_path)

        with open(self.meta_path, "wb") as f:
            pickle.dump({
                "ids": self.ids,
                "id_to_text": self.id_to_text,
                "id_to_metadata": self.id_to_metadata
            }, f)

    # -------------------------
    # Load
    # -------------------------
    def _load(self):
        if os.path.exists(self.index_path):
            self.index = faiss.read_index(self.index_path)

        if os.path.exists(self.meta_path):
            with open(self.meta_path, "rb") as f:
                data = pickle.load(f)
                self.ids = data["ids"]
                self.id_to_text = data["id_to_text"]
                self.id_to_metadata = data["id_to_metadata"]