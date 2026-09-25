import json
from pathlib import Path

from config import QUESTIONS_FILE
from llm.ollama_client import generate_response


# ============================================================
# LOAD QUESTIONS
# ============================================================

def load_all_questions():
    with open(QUESTIONS_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


# ============================================================
# AVAILABLE TOPICS
# ============================================================

def get_available_topics():
    questions = load_all_questions()

    topics = sorted(
        {
            question.get("topic", "General")
            for question in questions
        }
    )

    return ["All Topics"] + topics


# ============================================================
# AVAILABLE DIFFICULTIES
# ============================================================

def get_available_difficulties():
    return [
        "Any Difficulty",
        "Easy",
        "Medium",
        "Hard"
    ]


# ============================================================
# DEFAULT QUESTION PRESENTATION
# ============================================================

def _build_default_presentation(question):

    title = question.get("title", "Coding Problem")
    description = question.get(
        "description",
        "Solve the given problem."
    )

    return f"""
# {title}

## Problem Statement

{description}
"""


# ============================================================
# GENERATE QUESTION
# ============================================================

def generate_question(
    topic="All Topics",
    difficulty="Any Difficulty"
):

    questions = load_all_questions()

    # --------------------------------------------------------
    # FILTER QUESTIONS
    # --------------------------------------------------------

    candidates = questions

    if topic and topic != "All Topics":
        candidates = [
            question
            for question in candidates
            if question.get("topic") == topic
        ]

    if difficulty and difficulty != "Any Difficulty":
        candidates = [
            question
            for question in candidates
            if question.get("difficulty") == difficulty
        ]

    if not candidates:
        raise ValueError(
            "No questions found for the selected "
            "topic and difficulty."
        )

    # --------------------------------------------------------
    # SELECT QUESTION
    # --------------------------------------------------------

    question = candidates[0]

    # Make a copy so we preserve the original data.
    selected_question = dict(question)

    # --------------------------------------------------------
    # NORMALIZE TEST CASES
    # --------------------------------------------------------

    original_test_cases = question.get(
        "test_cases",
        []
    )

    selected_question["test_cases"] = original_test_cases

    # --------------------------------------------------------
    # NORMALIZE COMPLEXITY FIELDS
    # --------------------------------------------------------

    selected_question["expected_time_complexity"] = question.get(
        "expected_time_complexity",
        question.get("expected_time", "Unknown")
    )

    selected_question["expected_space_complexity"] = question.get(
        "expected_space_complexity",
        question.get("expected_space", "Unknown")
    )

    # --------------------------------------------------------
    # NORMALIZE OPTIONAL FIELDS
    # --------------------------------------------------------

    selected_question["examples"] = question.get(
        "examples",
        []
    )

    selected_question["constraints"] = question.get(
        "constraints",
        []
    )

    # --------------------------------------------------------
    # ASK MISTRAL TO PRESENT THE QUESTION
    # --------------------------------------------------------

    prompt = f"""
You are a coding interview question presenter.

Present the following coding problem clearly for a candidate.

Title:
{question.get("title", "")}

Topic:
{question.get("topic", "")}

Difficulty:
{question.get("difficulty", "")}

Problem:
{question.get("description", "")}

Function name:
{question.get("function_name", "")}

Give only the problem statement, function signature,
examples if available, and constraints.

Do not solve the problem.
"""

    try:

        presentation = generate_response(
            prompt=prompt,
            temperature=0.2,
            max_tokens=250
        )

        if presentation and presentation.strip():

            selected_question["presentation"] = presentation

        else:

            selected_question["presentation"] = (
                _build_default_presentation(question)
            )

    except Exception:

        selected_question["presentation"] = (
            _build_default_presentation(question)
        )

    return selected_question