from app.agents.retrieval_agent import retrieve_context
from app.agents.analysis_agent import analyze_context
from app.agents.summarizer_agent import summarize_answer


def run_agents(query, vectorstore, embed_text, rerank):
    
    # 🔍 Step 1: Retrieve
    context = retrieve_context(vectorstore, query, embed_text, rerank)

    context_text = "\n\n".join(context)

    # 📊 Step 2: Analyze
    analysis = analyze_context(query, context_text)

    # ✨ Step 3: Summarize
    answer = summarize_answer(query, analysis)

    return answer