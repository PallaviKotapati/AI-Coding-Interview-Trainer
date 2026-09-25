import logging
from typing import Dict, Any, Optional
from llm.ollama_client import generate_response, OllamaConnectionError, OllamaInferenceError

logger = logging.getLogger(__name__)

def _build_fallback_feedback(
    question: Dict[str, Any],
    submitted_code: str,
    test_results: Dict[str, Any],
    complexity_info: Dict[str, Any]
) -> str:
    """Fallback feedback report when the local LLM is unreachable."""
    passed = test_results.get("passed_tests", 0)
    total = test_results.get("total_tests", 0)
    success = test_results.get("success", False)

    status_badge = "✅ Passed All Tests" if success else f"⚠️ Partially Solved ({passed}/{total} Passed)"
    if test_results.get("error_type"):
        status_badge = f"❌ Execution Failed: {test_results.get('error_type')}"

    ast_text = complexity_info.get("ast_metrics", {}).get("ast_summary", "N/A")

    return f"""### 📝 Interview Evaluation Report

#### 1. Functional Correctness: {status_badge}
- **Tests Passed:** {passed} / {total}
- **Runtime:** {test_results.get('execution_time', 0)}s
{f"- **Error Encountered:** {test_results.get('error_message')}" if test_results.get('error_message') else ""}

#### 2. Structural & Complexity Assessment
- **AST Metrics:** {ast_text}
- **Expected Target Complexity:** Time `{question.get('expected_time_complexity')}` | Space `{question.get('expected_space_complexity')}`

#### 3. Strengths
- Syntactically structured Python code submitted.
- Attempted problem logic aligned with function signature `{question.get('function_name')}`.

#### 4. Weaknesses & Edge Cases to Consider
- Verify handling of extreme input sizes, empty collections, or boundary values specified in problem constraints.

#### 5. Progressive Hint
- Think about whether you can use auxiliary data structures (like a hash map or two pointers) to eliminate redundant loops.

*(Note: Detailed AI critique generated via fallback template as local LLM service was busy or offline)*
"""


def generate_feedback(
    question: Dict[str, Any],
    submitted_code: str,
    test_results: Dict[str, Any],
    complexity_info: Dict[str, Any]
) -> str:
    """
    Synthesizes test results, AST complexity metrics, and submitted code into 
    personalized interview feedback using Mistral 7B.

    Args:
        question (Dict[str, Any]): Problem specification.
        submitted_code (str): Candidate's Python code.
        test_results (Dict[str, Any]): Output from evaluation.code_runner.run_code.
        complexity_info (Dict[str, Any]): Output from evaluation.complexity.analyze_complexity.

    Returns:
        str: Comprehensive Markdown feedback report from the mock interviewer.
    """
    passed = test_results.get("passed_tests", 0)
    total = test_results.get("total_tests", 0)
    err_type = test_results.get("error_type")
    err_msg = test_results.get("error_message")
    test_details = test_results.get("test_details", [])

    # Format test summary
    tests_summary = f"Passed: {passed}/{total}\n"
    if err_type:
        tests_summary += f"Error Type: {err_type}\nError Details: {err_msg}\n"
    for td in test_details:
        status = "PASSED" if td.get("passed") else "FAILED"
        tests_summary += f"- Test {td.get('test_index')}: {status} | Inputs: {td.get('inputs')} | Expected: {td.get('expected')} | Output: {td.get('actual')}\n"

    complexity_text = complexity_info.get("analysis_text", "N/A")
    ast_summary = complexity_info.get("ast_metrics", {}).get("ast_summary", "N/A")

    system_prompt = (
        "You are a seasoned Principal Engineer and technical interviewer conducting a senior-level coding interview. "
        "Review the candidate's Python code submission based on their functional correctness, code quality, "
        "and algorithmic complexity. Be encouraging, thorough, and constructively critical. "
        "IMPORTANT RULE: DO NOT reveal the complete working optimal code solution. Provide guidance, hints, and direction instead."
    )

    user_prompt = f"""Evaluate this candidate's interview submission:

[PROBLEM SPECIFICATION]
Title: {question.get('title')}
Topic: {question.get('topic')}
Difficulty: {question.get('difficulty')}
Constraints: {question.get('constraints')}
Expected Time: {question.get('expected_time_complexity')}
Expected Space: {question.get('expected_space_complexity')}

[TEST EXECUTION RESULTS]
{tests_summary}

[STATIC AST CODE METRICS]
{ast_summary}

[COMPLEXITY ESTIMATE]
{complexity_text}

[CANDIDATE CODE]
```python
{submitted_code}
```

Please structure your feedback into these exact markdown sections:
### 1. Functional Correctness
(Evaluate test results, any failing edge cases, and runtime behavior)

### 2. Strengths
(Highlight good practices, variable names, logic choices, or cleanliness)

### 3. Weaknesses & Code Hygiene
(Constructive feedback on bugs, inefficiency, unhandled constraints, or antipatterns)

### 4. Complexity Feedback
(Compare candidate's complexity against optimal target time and space)

### 5. Progressive Hint
(Offer exactly ONE helpful conceptual hint guiding them toward optimal performance without giving the full code)

### 6. Mock Interviewer Recommendation
(State whether this would be a 'Strong Hire', 'Hire', 'Leaning No Hire', or 'Needs Optimization Round' with a brief justification)
"""

    try:
        feedback = generate_response(
            prompt=user_prompt,
            system_prompt=system_prompt,
            temperature=0.3,
            max_tokens=450
        )
        return feedback
    except (OllamaConnectionError, OllamaInferenceError) as err:
        logger.warning(f"Ollama unavailable for feedback ({err}). Using fallback report.")
        return _build_fallback_feedback(question, submitted_code, test_results, complexity_info)
