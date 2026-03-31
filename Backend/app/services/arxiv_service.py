import time
import requests
import xml.etree.ElementTree as ET


def fetch_papers(query, max_results=3, retries=3):
    url = f"http://export.arxiv.org/api/query?search_query=all:{query}&start=0&max_results={max_results}"

    for attempt in range(retries):
        try:
            response = requests.get(url, timeout=10)

            if response.status_code == 429:
                print("⚠️ Rate limited. Sleeping...")
                time.sleep(5)
                continue

            if response.status_code != 200:
                print("⚠️ API error:", response.status_code)
                return []

            root = ET.fromstring(response.content)

            papers = []
            for entry in root.findall("{http://www.w3.org/2005/Atom}entry"):
                title = entry.find("{http://www.w3.org/2005/Atom}title").text

                pdf_link = None
                for link in entry.findall("{http://www.w3.org/2005/Atom}link"):
                    if link.attrib.get("title") == "pdf":
                        pdf_link = link.attrib["href"]

                papers.append({
                    "title": title,
                    "pdf_link": pdf_link
                })

            return papers

        except requests.exceptions.Timeout:
            print(f"⚠️ Timeout... retry {attempt+1}/{retries}")
            time.sleep(2 * (attempt + 1))  # exponential backoff

        except Exception as e:
            print("⚠️ Error:", str(e))
            return []

    print("❌ Failed after retries")
    return []