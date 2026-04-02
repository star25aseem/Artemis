def retrieve_context(vectorstore, query, embed_text, rerank):
    query_embedding = embed_text([query])[0]

    results = vectorstore.search(query_embedding, k=15)

    # rerank
    results = rerank(query, results, top_k=10)

    # diversity filter
    seen_titles = set()
    filtered_results = []

    for r in results:
        title = r["metadata"]["title"]

        if title not in seen_titles:
            filtered_results.append(r)
            seen_titles.add(title)

        if len(filtered_results) == 7:
            break

    # build context
    context = []
    for r in filtered_results:
        text = r["text"]

        if len(text.split()) > 40:
            context.append(text)

    return context