from langchain_huggingface import HuggingFaceEmbeddings
from app import config

_embeddings = None

def get_embeddings():
    global _embeddings
    if not _embeddings:
        _embeddings = HuggingFaceEmbeddings(
            model_name=config.EMBEDDINGS_MODEL,
            model_kwargs={
                "device": "cpu"
            }
        )
    return _embeddings