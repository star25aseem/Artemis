from sentence_transformers import CrossEncoder

# very strong reranker model
reranker_model = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")


def rerank(query, results, top_k=5):
    pairs = [(query, r["text"]) for r in results]

    scores = reranker_model.predict(pairs)

    # attach scores
    for i, r in enumerate(results):
        r["rerank_score"] = float(scores[i])

    # sort by rerank score
    results = sorted(results, key=lambda x: x["rerank_score"], reverse=True)

    return results[:top_k]
