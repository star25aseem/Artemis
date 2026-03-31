import requests
from app.llm.llm_provider import get_llm

llm = get_llm()

def generate_answer(query, context):
    prompt = f"""
You are an expert AI research assistant specialized in analyzing academic papers.

Your task is to generate a precise, factual, and context-grounded answer.

Guidelines:
- Use ONLY the provided context to construct the answer
- Extract and synthesize the most relevant technical information
- Prefer concrete concepts, methods, and insights over generic statements
- If multiple ideas are present, organize them clearly
- When possible, explicitly list techniques, models, or key methods mentioned in the context

Strict Constraints:
- Do NOT introduce any external knowledge
- Do NOT invent details, references, figures, or citations
- Do NOT assume missing information
- If the context is incomplete, provide the best possible partial answer using available information

Output Requirements:
- Be clear, concise, and technically informative
- Use structured formatting when helpful (e.g., bullet points)
- Focus on usefulness and clarity

Context:
{context}

Query:
{query}

Answer:
"""

    return llm.invoke(prompt).content
