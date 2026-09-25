from pathlib import Path

# ============================================================
# PROJECT PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parent

DATA_DIR = BASE_DIR / "data"
QUESTIONS_FILE = DATA_DIR / "dsa_questions.json"

CHROMA_DIR = BASE_DIR / "chroma_db"


# ============================================================
# OLLAMA / LLM CONFIGURATION
# ============================================================

OLLAMA_BASE_URL = "http://127.0.0.1:11434"

OLLAMA_GENERATE_ENDPOINT = f"{OLLAMA_BASE_URL}/api/generate"

DEFAULT_MODEL = "mistral:latest"

# Maximum time to wait for Ollama
LLM_TIMEOUT = 60


# ============================================================
# CODE EXECUTION CONFIGURATION
# ============================================================

# Maximum time allowed for submitted code
EXECUTION_TIMEOUT = 5

# Maximum amount of output captured from submitted code
MAX_OUTPUT_LENGTH = 5000


# ============================================================
# EMBEDDINGS / RAG
# ============================================================

EMBEDDING_MODEL = "all-MiniLM-L6-v2"