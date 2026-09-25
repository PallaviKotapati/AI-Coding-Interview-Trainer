from rag.retriever import retrieve_questions
from llm.ollama_client import generate_response


def generate_rag_feedback(
    question,
    submitted_code,
    test_results,
    complexity_info
):

    # ========================================================
    # RETRIEVE SIMILAR QUESTIONS
    # ========================================================

    query = (
        str(question.get("title", "")) + " "
        + str(question.get("topic", "")) + " "
        + str(question.get("description", ""))
    )

    try:
        retrieved = retrieve_questions(
            query,
            top_k=2
        )
    except Exception:
        retrieved = []

    # ========================================================
    # BUILD SMALL RAG CONTEXT
    # ========================================================

    context = ""

    for item in retrieved:

        document = item.get("document", "")

        if document:
            context += document[:500] + "\n\n"

    if not context:
        context = "No similar questions were retrieved."

    # ========================================================
    # TEST RESULT SUMMARY
    # ========================================================

    passed = test_results.get("passed", 0)
    total = test_results.get("total", 0)

    test_summary = f"{passed}/{total} test cases passed."

    # ========================================================
    # COMPLEXITY
    # ========================================================

    time_complexity = complexity_info.get(
        "time_complexity",
        "Unknown"
    )

    space_complexity = complexity_info.get(
        "space_complexity",
        "Unknown"
    )

    # ========================================================
    # SHORT RAG PROMPT
    # ========================================================

    prompt = (
        "You are an AI coding interview evaluator.\n\n"

        "CURRENT PROBLEM:\n"
        f"Title: {question.get('title', '')}\n"
        f"Topic: {question.get('topic', '')}\n"
        f"Description: {question.get('description', '')}\n\n"

        "SUBMITTED CODE:\n"
        f"{submitted_code}\n\n"

        "TEST RESULT:\n"
        f"{test_summary}\n\n"

        "COMPLEXITY:\n"
        f"Time: {time_complexity}\n"
        f"Space: {space_complexity}\n\n"

        "SIMILAR QUESTIONS FROM KNOWLEDGE BASE:\n"
        f"{context}\n\n"

        "Give concise interview feedback using exactly these sections:\n\n"

        "1. Functional Correctness\n"
        "2. Strengths\n"
        "3. Weaknesses & Code Hygiene\n"
        "4. Complexity Feedback\n"
        "5. Progressive Hint\n"
        "6. Mock Interviewer Recommendation\n\n"

        "Keep the response concise."
    )

    # ========================================================
    # MISTRAL
    # ========================================================

    try:

        response = generate_response(
            prompt=prompt,
            temperature=0.1,
            max_tokens=120,
            timeout=60
        )

        return response

    except Exception as e:

        return (
            "## AI Feedback\n\n"
            "RAG retrieval and code evaluation completed, "
            "but the local LLM timed out.\n\n"
            f"Error: {str(e)}\n\n"
            "### Evaluation Summary\n"
            f"- Test Cases: {test_summary}\n"
            f"- Time Complexity: {time_complexity}\n"
            f"- Space Complexity: {space_complexity}"
        )