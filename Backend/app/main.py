from app.services.arxiv_service import fetch_papers
from app.services.pdf_parser import download_pdf, parse_pdf
from app.services.chunking import split_text
from app.services.embedding_service import embed_text
from app.vectorstore.faiss_store import VectorStore
from app.agents.research_agent import generate_answer
from app.memory.conversation_memory import ConversationMemory
from app.agents.query_rewriter import rewrite_query
from app.services.reranker import rerank
import os

# Global lightweight memory
memory = ConversationMemory()

# Track processed papers
processed_titles = set()
query_cache = set()


def add_papers_to_vectorstore(query, vectorstore, context, IS_PROD):
    if query in query_cache:
        print(" Using cached query, skipping fetch")
        return

    query_cache.add(query)

    papers = fetch_papers(query, max_results=1)

    if not papers:
        print("⚠️ Using previous knowledge (no new papers)")
        return

    for paper in papers:
        title = paper["title"]

        if title in processed_titles:
            continue

        print("\n Adding new paper:", title)

        # 🚀 PRODUCTION MODE (LIGHTWEIGHT)
        if IS_PROD:
            print("⚡ Using summary instead of PDF")
            context.append(paper.get("summary", ""))
            processed_titles.add(title)
            continue

        # 🧠 LOCAL MODE (FULL PIPELINE)
        if paper["pdf_link"]:
            pdf_path = download_pdf(paper["pdf_link"])
            text = parse_pdf(pdf_path)

            chunks = split_text(text)
            chunks = chunks[:20]  # 🔥 limit chunks

            embeddings = embed_text(chunks)

            metadata = [{"title": title} for _ in chunks]

            vectorstore.add(embeddings, chunks, metadata)

            processed_titles.add(title)


# 🚀 MAIN PIPELINE (API READY)
def run_pipeline(user_query: str):
    IS_PROD = os.getenv("RENDER") is not None

    # 🚀 Lazy init (important for memory)
    vectorstore = VectorStore() if not IS_PROD else None

    # Store user query
    memory.add_user_message(user_query)

    history = memory.get_formatted_history()

    # Rewrite query
    rewritten_query = rewrite_query(user_query, history)

    print("\nOriginal Query:", user_query)
    print("Rewritten Query:", rewritten_query)

    # Build context container
    context = []

    # Update knowledge base
    add_papers_to_vectorstore(rewritten_query, vectorstore, context, IS_PROD)

    # 🚀 PRODUCTION MODE (NO FAISS)
    if IS_PROD:
        context_text = "\n\n".join(context)

        answer = generate_answer(rewritten_query, context_text)

        memory.add_assistant_message(answer)

        return {
            "query": user_query,
            "rewritten_query": rewritten_query,
            "answer": answer
        }

    # 🧠 LOCAL MODE (FULL RETRIEVAL)

    query_embedding = embed_text([rewritten_query])[0]
    results = vectorstore.search(query_embedding, k=10)

    # Clean small chunks
    results = [r for r in results if len(r["text"]) > 100]

    # Rerank
    results = rerank(rewritten_query, results, top_k=5)

    # Diversity filtering
    seen_titles = set()
    filtered_results = []

    for r in results:
        title = r["metadata"]["title"]

        if title not in seen_titles:
            filtered_results.append(r)
            seen_titles.add(title)

        if len(filtered_results) == 3:
            break

    print("\nTop Retrieved Chunks:\n")

    for r in filtered_results:
        print(f"[Score: {r['score']:.4f}] {r['metadata']['title']}")
        print(r["text"][:200])
        print("----")

        if len(r["text"].split()) > 40:
            context.append(r["text"])

    context_text = "\n\n".join(context)

    # Generate answer
    answer = generate_answer(rewritten_query, context_text)

    print("\n\nFINAL ANSWER:\n")
    print(answer)

    # Store response
    memory.add_assistant_message(answer)

    return {
        "query": user_query,
        "rewritten_query": rewritten_query,
        "answer": answer
    }