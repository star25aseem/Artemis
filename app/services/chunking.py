from langchain_text_splitters import RecursiveCharacterTextSplitter


def split_text(text):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=300,
        chunk_overlap=50,
        separators=[
            "\n\n",  # paragraphs
            "\n",    # lines
            ". ",    # sentences
            " ",     # words
        ]
    )

    chunks = splitter.split_text(text)

    return chunks