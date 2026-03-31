from app.llm.llm_provider import get_llm

llm = get_llm()


def summarize_answer(query, analysis):
    prompt = f"""
You are a research assistant.

Convert the analysis into a clear and structured answer.

Rules:
- Be concise and technical
- Organize into bullet points if needed
- Do NOT include references like "Figure" or "Fig."

Analysis:
{analysis}

Query:
{query}

Final Answer:
"""

    return llm.invoke(prompt).content