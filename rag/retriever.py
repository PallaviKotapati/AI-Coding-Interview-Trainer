import json
from pathlib import Path

import chromadb
from sentence_transformers import SentenceTransformer


# ============================================================
# PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent

QUESTIONS_FILE = BASE_DIR / "data" / "dsa_questions.json"

CHROMA_DIR = BASE_DIR / "chroma_db"


# ============================================================
# MODELS
# ============================================================

EMBEDDING_MODEL = "all-MiniLM-L6-v2"


# ============================================================
# INITIALIZE
# ============================================================

embedding_model = SentenceTransformer(
    EMBEDDING_MODEL
)

chroma_client = chromadb.PersistentClient(
    path=str(CHROMA_DIR)
)

collection = chroma_client.get_or_create_collection(
    name="dsa_questions"
)


# ============================================================
# LOAD DATASET
# ============================================================

def load_questions():

    with open(
        QUESTIONS_FILE,
        "r",
        encoding="utf-8"
    ) as file:

        return json.load(file)


# ============================================================
# BUILD DOCUMENT
# ============================================================

def question_to_document(question):

    title = question.get(
        "title",
        ""
    )

    topic = question.get(
        "topic",
        ""
    )

    difficulty = question.get(
        "difficulty",
        ""
    )

    description = question.get(
        "description",
        ""
    )

    tags = ", ".join(
        question.get(
            "tags",
            []
        )
    )

    return (
        f"Title: {title}\n"
        f"Topic: {topic}\n"
        f"Difficulty: {difficulty}\n"
        f"Description: {description}\n"
        f"Tags: {tags}"
    )


# ============================================================
# BUILD / UPDATE VECTOR DATABASE
# ============================================================

def build_vector_database():

    questions = load_questions()

    documents = []
    ids = []
    metadatas = []

    for question in questions:

        question_id = str(
            question["id"]
        )

        documents.append(
            question_to_document(
                question
            )
        )

        ids.append(
            question_id
        )

        metadatas.append(
            {
                "id": question_id,
                "title": question.get(
                    "title",
                    ""
                ),
                "topic": question.get(
                    "topic",
                    ""
                ),
                "difficulty": question.get(
                    "difficulty",
                    ""
                ),
                "function_name": question.get(
                    "function_name",
                    ""
                )
            }
        )

    embeddings = embedding_model.encode(
        documents
    ).tolist()

    collection.upsert(
        ids=ids,
        documents=documents,
        embeddings=embeddings,
        metadatas=metadatas
    )

    return len(documents)


# ============================================================
# RETRIEVE QUESTIONS
# ============================================================

def retrieve_questions(
    query,
    top_k=3
):

    query_embedding = embedding_model.encode(
        [query]
    ).tolist()

    results = collection.query(
        query_embeddings=query_embedding,
        n_results=top_k
    )

    retrieved = []

    documents = results.get(
        "documents",
        [[]]
    )[0]

    metadatas = results.get(
        "metadatas",
        [[]]
    )[0]

    for document, metadata in zip(
        documents,
        metadatas
    ):

        retrieved.append(
            {
                "document": document,
                "metadata": metadata
            }
        )

    return retrieved


# ============================================================
# SIMPLE TEST
# ============================================================

if __name__ == "__main__":

    count = build_vector_database()

    print(
        f"Indexed {count} questions."
    )

    results = retrieve_questions(
        "array problem using a hash map",
        top_k=3
    )

    print("\nRetrieved questions:\n")

    for result in results:

        print(
            result["metadata"]["title"]
        )

        print(
            result["document"]
        )

        print("-" * 50)