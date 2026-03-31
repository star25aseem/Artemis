import os

# 🔥 Try Groq first
def get_llm():
    try:
        from langchain_groq import ChatGroq

        return ChatGroq(
            model="llama-3.1-8b-instant",
            temperature=0
        )

    except Exception as e:
        print("⚠️ Groq not available, switching to HuggingFace...")

        from langchain_huggingface import HuggingFaceEndpoint

        return HuggingFaceEndpoint(
           repo_id="google/flan-t5-base",
           temperature=0.3,
           max_new_tokens=256
        )
