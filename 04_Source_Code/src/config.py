import os
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY") or os.getenv("OPENROUTER_API_KEY")
if not GROQ_API_KEY:
    raise RuntimeError("Set GROQ_API_KEY or OPENROUTER_API_KEY in .env (see .env.example)")

MODEL_NAME = os.getenv("MODEL_NAME")
if not MODEL_NAME:
    raise RuntimeError("Set MODEL_NAME in .env")

EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL")
if not EMBEDDING_MODEL:
    raise RuntimeError("Set EMBEDDING_MODEL in .env")

CHROMA_PATH = os.getenv("CHROMA_PATH")
if not CHROMA_PATH:
    raise RuntimeError("Set CHROMA_PATH in .env")

_confidence_raw = os.getenv("CONFIDENCE_THRESHOLD")
if not _confidence_raw:
    raise RuntimeError("Set CONFIDENCE_THRESHOLD in .env")
CONFIDENCE_THRESHOLD = float(_confidence_raw)

_top_k_raw = os.getenv("RETRIEVAL_TOP_K")
if not _top_k_raw:
    raise RuntimeError("Set RETRIEVAL_TOP_K in .env")
RETRIEVAL_TOP_K = int(_top_k_raw)

_auto_respond_raw = os.getenv("AUTO_RESPOND")
if not _auto_respond_raw:
    raise RuntimeError("Set AUTO_RESPOND in .env")
AUTO_RESPOND = _auto_respond_raw.lower() != "false"

LOG_LEVEL = os.getenv("LOG_LEVEL")
if not LOG_LEVEL:
    raise RuntimeError("Set LOG_LEVEL in .env")


def require_api_key() -> str:
    if not GROQ_API_KEY:
        raise RuntimeError("Set GROQ_API_KEY in .env (see .env.example)")
    return GROQ_API_KEY
