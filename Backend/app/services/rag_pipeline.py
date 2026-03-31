from app.services.arxiv_service import fetch_papers
from app.services.pdf_parser import parse_pdf
from app.services.embedding_service import embed_text
from app.vectorstore.faiss_store import store_embeddings, search
from app.agents.research_agent import generate_answer

async def process_query(query):
    papers = fetch_papers(query)

    all_chunks = []
    for paper in papers:
        text = parse_pdf(paper)
        chunks = split_text(text)
        all_chunks.extend(chunks)

    embeddings = embed_text(all_chunks)
    store_embeddings(embeddings, all_chunks)

    relevant_chunks = search(query)

    answer = generate_answer(query, relevant_chunks)

    return answer
