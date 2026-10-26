from time import sleep
from langchain_chroma import Chroma
from langchain_core.documents import Document
from app.services import embeddings


def get_vectorstore(video_id: str):
    return Chroma(
        collection_name=f"video_{video_id}",
        persist_directory="../../chroma_data",
        embedding_function=embeddings.get_embeddings(),
    )


def store(video_id: str, chunks: list[dict]):
    vector_store = get_vectorstore(video_id)

    docs: list[Document] = []
    for chunk in chunks:
        document = Document(
            page_content=chunk["content"],
            metadata={
                "source": video_id,
                "start_time": chunk["start"],
                "end_time": chunk["end"],
            },
        )
        docs.append(document)
    vector_store.add_documents(docs)


def search(video_id: str, query: str):
    vector_store = get_vectorstore(video_id)
    results = vector_store.similarity_search(query=query, k=4)
    return results
