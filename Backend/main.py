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

memory = ConversationMemory()

# Track already processed papers
processed_titles = set()
query_cache = set()

def add_papers_to_vectorstore(query, vectorstore):
    if query in query_cache:
        print(" Using cached query, skipping fetch")
        return

    query_cache.add(query)

    papers = fetch_papers(query)
    if not papers:
      print("⚠️ Using previous knowledge (no new papers)")
    IS_PROD = os.getenv("RENDER") is not None
    for paper in papers:
        title = paper["title"]

        # Skip already processed papers
        if title in processed_titles:
            continue

        print("\n Adding new paper:", title)
        if IS_PROD:
            print("⚡ Skipping PDF processing in production")
            continue
        if paper["pdf_link"]:
            pdf_path = download_pdf(paper["pdf_link"])
            text = parse_pdf(pdf_path)

            chunks = split_text(text)
            embeddings = embed_text(chunks)

            metadata = [{"title": title} for _ in chunks]

            vectorstore.add(embeddings, chunks, metadata)

            processed_titles.add(title)


def run_pipeline():
    vectorstore = VectorStore()

    print("\n System ready. Ask anything.\n")

    while True:
        user_query = input("\nAsk something (or type 'exit'): ")

        if user_query.lower() == "exit":
            break

        # Store user query
        memory.add_user_message(user_query)

        history = memory.get_formatted_history()

        # Rewrite query
        rewritten_query = rewrite_query(user_query, history)

        print("\nOriginal Query:", user_query)
        print("Rewritten Query:", rewritten_query)

        # Update knowledge base dynamically
        add_papers_to_vectorstore(rewritten_query, vectorstore)

        # Retrieval
        query_embedding = embed_text([rewritten_query])[0]
        results = vectorstore.search(query_embedding, k=15)  # fetch more
        cleaned_results = []

        for r in results:
            if len(r["text"]) > 100:  # remove useless chunks
               cleaned_results.append(r)

        results = cleaned_results
        # Apply reranking
        results = rerank(rewritten_query, results, top_k=10)

        # Diversity filtering
        seen_titles = set()
        filtered_results = []

        for r in results:
            title = r["metadata"]["title"]

            if title not in seen_titles:
                filtered_results.append(r)
                seen_titles.add(title)

            if len(filtered_results) == 5:
                break

        # Build context
        context = []
        print("\nTop Retrieved Chunks:\n")

        for r in filtered_results:
            print(f"[Score: {r['score']:.4f}] {r['metadata']['title']}")
            print(r["text"][:200])
            print("----")
            text = r["text"]

            #  Keep only informative chunks
            # skip tiny chunks
            if len(text.split()) > 40:  
              context.append(text)

        context_text = "\n\n".join(context)

        # Generate answer
        answer = run_agents(rewritten_query,vectorstore,embed_text,rerank)

        print("\n\nFINAL ANSWER:\n")
        print(answer)

        # Store response
        memory.add_assistant_message(answer)


if __name__ == "__main__":
    run_pipeline()