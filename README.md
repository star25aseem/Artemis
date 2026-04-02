# Artemis
Autonomous AI Research Assistant
# Deployed on
https://star25aseem-artemis.hf.space/
# 🚀 Artemis – AI Research Assistant

Artemis is a lightweight AI-powered research assistant that retrieves and summarizes academic knowledge in real time. It is designed to balance **performance, scalability, and resource efficiency**, making it deployable even on constrained environments like Hugging Face Spaces.

---

## 🌟 Features

* 🔍 **Intelligent Query Handling**

  * Cleans and optimizes user queries for academic search
  * Maintains conversation context

* 📄 **Multi-Source Paper Retrieval**

  * Primary: arXiv API
  * Fallback: Semantic Scholar API
  * Ensures robustness even under rate limits

* 🧠 **Context-Aware Answer Generation**

  * Uses retrieved paper summaries as grounding context
  * Generates structured, research-style answers

* ⚡ **Production Optimization**

  * No heavy PDF parsing in deployed mode
  * No FAISS / embeddings in production (memory-efficient)
  * Fast response times on limited hardware

* 🧹 **Clean Output Formatting**

  * Converts raw LLM output into readable structured text
  * Supports headings, bullet points, and sections

---

## 🏗️ Architecture

### 🔵 Production Mode (Hugging Face Spaces)

```
User Query
   ↓
Query Cleaning
   ↓
Paper Retrieval (arXiv → Semantic Scholar fallback)
   ↓
Context Building (summaries only)
   ↓
LLM Answer Generation
   ↓
Formatted Output
```

### 🟢 Local Mode (Full Pipeline)

```
User Query
   ↓
Query Rewriting
   ↓
Paper Retrieval + PDF Parsing
   ↓
Chunking + Embeddings
   ↓
Vector Search (FAISS)
   ↓
Reranking + Filtering
   ↓
LLM Answer Generation
```

---

## ⚙️ Tech Stack

* **Backend:** Python
* **LLM Integration:** Groq / Hugging Face
* **Frontend:** Gradio
* **APIs:**

  * arXiv API
  * Semantic Scholar API
* **Embeddings (Local):**

  * sentence-transformers/all-MiniLM-L6-v2

---

## 🔑 Environment Variables

Set these in your deployment:

```
GROQ_API_KEY=your_key_here
HF_TOKEN=your_token_here
```

---

## 🚀 Deployment (Hugging Face Spaces)

1. Create a new Space (Gradio)
2. Push your code via GitHub
3. Add environment variables in **Settings → Secrets**
4. Deploy

Your app will be live at:

```
https://huggingface.co/spaces/<username>/<space-name>
```

---

## 🧠 Key Design Decisions

* ❌ Removed heavy retrieval (FAISS, reranking) in production
* ✅ Used paper summaries instead of PDFs
* ✅ Added multi-source fallback for reliability
* ✅ Simplified query rewriting to improve retrieval accuracy

---

## 📈 Future Improvements

* 📊 Paper ranking based on relevance
* 📚 Citation generation in answers
* 🧾 “Top Papers” UI section
* 🧠 Smart query expansion (non-LLM based)
* 🔄 Streaming responses

---

## 💡 Inspiration

Artemis follows the design philosophy of modern AI research tools like:

* Perplexity AI
* Elicit
* Research copilots

---

## 👨‍💻 Author

Built as part of an advanced AI systems project focusing on:

* Retrieval-Augmented Generation (RAG)
* System design under constraints
* Real-world deployment challenges

---

## ⭐ Final Note

Artemis is not just a chatbot — it is a **resilient research system** designed to operate effectively even with limited compute resources.

---

