import dotenv
from langchain_groq import ChatGroq

dotenv.load_dotenv()

_llm = None


def get_llm():
    global _llm
    if not _llm:
        _llm = ChatGroq(model="openai/gpt-oss-120b", temperature=0.7)
    return _llm
