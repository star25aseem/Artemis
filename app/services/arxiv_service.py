import requests
import time

def fetch_from_arxiv(query, max_results=2):
    try:
        url = f"http://export.arxiv.org/api/query?search_query=all:{query}&start=0&max_results={max_results}"
        response = requests.get(url, timeout=8)

        if response.status_code != 200:
            return []

        import xml.etree.ElementTree as ET
        root = ET.fromstring(response.content)

        papers = []
        for entry in root.findall("{http://www.w3.org/2005/Atom}entry"):
            title = entry.find("{http://www.w3.org/2005/Atom}title").text
            summary = entry.find("{http://www.w3.org/2005/Atom}summary").text

            papers.append({
                "title": title.strip(),
                "summary": summary.strip(),
                "pdf_link": None
            })

        return papers

    except Exception as e:
        print("⚠️ arXiv failed:", e)
        return []


def fetch_from_semantic_scholar(query, max_results=2):
    try:
        url = "https://api.semanticscholar.org/graph/v1/paper/search"
        params = {
            "query": query,
            "limit": max_results,
            "fields": "title,abstract"
        }

        response = requests.get(url, params=params, timeout=8)

        if response.status_code != 200:
            return []

        data = response.json()

        papers = []
        for p in data.get("data", []):
            papers.append({
                "title": p.get("title", ""),
                "summary": p.get("abstract", ""),
                "pdf_link": None
            })

        return papers

    except Exception as e:
        print("⚠️ Semantic Scholar failed:", e)
        return []


def fetch_papers(query, max_results=2):
    # Try arXiv first
    papers = fetch_from_arxiv(query, max_results)

    if papers:
        print("✅ Got papers from arXiv")
        return papers

    print("🔁 Falling back to Semantic Scholar...")

    papers = fetch_from_semantic_scholar(query, max_results)

    if papers:
        print("✅ Got papers from Semantic Scholar")
        return papers

    print("❌ No papers found anywhere")
    return []