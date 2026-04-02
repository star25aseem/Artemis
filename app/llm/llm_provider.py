import os
from langchain_groq import ChatGroq
from langchain_huggingface import HuggingFaceEndpoint

def get_llm():
    groq_key = os.getenv("GROQ_API_KEY")
    hf_token = os.getenv("HUGGINGFACEHUB_API_TOKEN")

    # 🚀 Try Groq first
    if groq_key:
        try:
            print("🚀 Using Groq")
            return ChatGroq(
                groq_api_key=groq_key,
                model_name="llama-3.1-8b-instant"
            )
        except Exception as e:
            print("⚠️ Groq failed:", e)

    # 🔁 Fallback to HuggingFace
    if hf_token:
        try:
            print("🔁 Using HuggingFace")
            return HuggingFaceEndpoint(
                repo_id="HuggingFaceH4/zephyr-7b-beta",
                task="conversational",
                huggingfacehub_api_token=hf_token,
                temperature=0.5,
                max_new_tokens=512
            )
        except Exception as e:
            print("⚠️ HF failed:", e)

    raise RuntimeError("❌ No LLM available. Set GROQ_API_KEY or HF_TOKEN")