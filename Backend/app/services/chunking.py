from langchain.text_splitter import RecursiveCharacterTextSplitter


def split_text(text):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=100,
        separators=[
            "\n\n",  # paragraphs
            "\n",    # lines
            ". ",    # sentences
            " ",     # words
        ]
    )

    chunks = splitter.split_text(text)

    return chunks