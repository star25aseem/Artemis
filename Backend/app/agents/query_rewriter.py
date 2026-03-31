from app.llm.llm_provider import get_llm

llm = get_llm()


def rewrite_query(query, history=None):
    prompt = f"""
You are a research query optimizer.

Convert the user query into a SHORT, CLEAN search query for retrieving academic papers.

Rules:
- ONLY return the rewritten query
- NO explanations
- NO sentences
- ONLY keywords or short phrases
- Keep it under 10 words

Conversation History:
{history if history else "None"}

User Query:
{query}

Rewritten Query:
"""

    response = llm.invoke(prompt)
    cleaned = response.content.strip().split("\n")[0]
    return cleaned