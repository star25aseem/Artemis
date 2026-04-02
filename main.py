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
import re

def clean_text(text):
    # Convert ### headings → uppercase titles
    text = re.sub(r"###\s*(.*)", r"\n\n\1\n" + "-"*50, text)

    # Convert **bold** → uppercase (or keep as is if UI supports markdown)
    text = re.sub(r"\*\*(.*?)\*\*", lambda m: m.group(1).upper(), text)

    # Convert bullet points properly
    text = re.sub(r"\n\*\s*", "\n• ", text)

    # Fix escaped characters
    text = text.replace("\\n", "\n")
    text = text.replace("\\t", " ")

    # Clean extra spaces/newlines
    text = re.sub(r"\n\s*\n", "\n\n", text)

    return text.strip()
# Global lightweight memory
memory = ConversationMemory()

# Track processed papers
processed_titles = set()
paper_cache = {}

def add_papers_to_vectorstore(query, vectorstore, context, IS_PROD):
    if query in paper_cache:
        print("⚡ Using cached papers")
        context.extend(paper_cache[query])
        return

    papers = fetch_papers(query, max_results=3)

    if not papers:
        print("⚠️ Using previous knowledge (no new papers)")
        return

    summaries = []

    for paper in papers:
        title = paper["title"]

        if title in processed_titles:
            continue

        print("\n Adding new paper:", title)

        summary = paper.get("summary", "")
        summaries.append(summary)
        context.append(summary)

        processed_titles.add(title)

    paper_cache[query] = summaries

# 🚀 MAIN PIPELINE (API READY)
def run_pipeline(user_query: str):


    IS_PROD = os.getenv("SPACE_ID") is not None or os.getenv("RENDER") is not None

    # 🚀 Lazy init
    vectorstore = None if IS_PROD else VectorStore()

    # Memory
    memory.add_user_message(user_query)
    history = memory.get_formatted_history()

    # Rewrite
    try:
        rewritten_query = rewrite_query(user_query, history)
    except Exception as e:
        print("⚠️ Rewrite failed:", e)
        rewritten_query = user_query

    print("\nOriginal Query:", user_query)
    print("Rewritten Query:", rewritten_query)

    # Context container
    context = []

    # ✅ USE YOUR FUNCTION (FIXED)
    add_papers_to_vectorstore(rewritten_query, vectorstore, context, IS_PROD)

    # -------------------------------
    # 🚀 PRODUCTION MODE (HF Spaces)
    # -------------------------------
    if IS_PROD:
        context_text = "\n\n".join(context[:5])

        try:
            answer = generate_answer(rewritten_query, context_text)
        except Exception as e:
            print("⚠️ Generation failed:", e)
            answer = "⚠️ Failed to generate answer."

        memory.add_assistant_message(answer)

        return {
            "query": user_query,
            "rewritten_query": rewritten_query,
            "answer": answer
        }

    # -------------------------------
    # 🧠 LOCAL MODE (FULL RETRIEVAL)
    # -------------------------------
    try:
        query_embedding = embed_text([rewritten_query])[0]
    except Exception as e:
        print("⚠️ Embedding failed:", e)
        query_embedding = [0.0] * 384

    results = vectorstore.search(query_embedding, k=5)

    # Clean
    results = [r for r in results if len(r["text"]) > 100]

    # Rerank
    try:
        results = rerank(rewritten_query, results, top_k=3)
    except Exception as e:
        print("⚠️ Rerank failed:", e)

    # Diversity
    seen_titles = set()
    filtered_results = []

    for r in results:
        title = r["metadata"].get("title", "unknown")

        if title not in seen_titles:
            filtered_results.append(r)
            seen_titles.add(title)

        if len(filtered_results) == 3:
            break

    print("\nTop Retrieved Chunks:\n")

    for r in filtered_results:
        print(f"[Score: {r.get('score', 0):.4f}] {r['metadata'].get('title')}")
        print(r["text"][:200])
        print("----")

        if len(r["text"].split()) > 40:
            context.append(r["text"])

    context_text = "\n\n".join(context[:5])

    # Generate
    try:
        answer = generate_answer(rewritten_query, context_text)
        answer = clean_text(answer)
    except Exception as e:
        print("⚠️ Answer generation failed:", e)
        answer = "⚠️ Failed to generate answer."

    print("\n\nFINAL ANSWER:\n", answer)

    memory.add_assistant_message(answer)

    return {
        "query": user_query,
        "rewritten_query": rewritten_query,
        "answer": answer
    }