from app.llm.llm_provider import get_llm

llm = get_llm()


def analyze_context(query, context):
    prompt = f"""
You are a research analyst.

Your job is to extract key technical insights from the context.

Rules:
- Focus on methods, models, and techniques
- Ignore references like figures, tables, citations
- Extract meaningful insights only

Context:
{context}

Query:
{query}

Key Insights:
"""

    return llm.invoke(prompt).content