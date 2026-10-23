import chromadb
from chromadb import Client

client = chromadb.PersistentClient("../../chroma_data")

def get_vectorstore(video_id: str):
    pass
