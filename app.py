import gradio as gr

from services.question_generator import (
    generate_question,
    get_available_topics,
    get_available_difficulties,
)
from evaluation.code_runner import run_code
from evaluation.complexity import analyze_complexity
from services.rag_feedback import generate_rag_feedback


# ============================================================
# QUESTION GENERATION
# ============================================================

def generate_new_question(topic, difficulty):
    try:
        question = generate_question(topic, difficulty)

        if not question:
            return (
                "❌ Could not generate a question.",
                "",
                "No question available.",
                {},
            )

        title = question.get("title", "Coding Problem")

        description = question.get(
            "presentation",
            question.get("description", ""),
        )

        function_name = question.get(
            "function_name",
            "solution",
        )

        question_text = (
            f"# 🧩 {title}\n\n"
            f"**Topic:** {question.get('topic', 'N/A')}  \n"
            f"**Difficulty:** {question.get('difficulty', 'N/A')}\n\n"
            "---\n\n"
            "## Problem\n\n"
            f"{description}\n\n"
            "---\n\n"
            "### Expected Complexity\n\n"
            f"- **Time:** {question.get('expected_time', 'N/A')}\n"
            f"- **Space:** {question.get('expected_space', 'N/A')}\n\n"
            "---\n\n"
            "### Function to Implement\n\n"
            "```python\n"
            f"def {function_name}(...):\n"
            "    pass\n"
            "```\n\n"
            "Write your solution in the editor below and click "
            "**Evaluate Solution**."
        )

        starter_code = (
            f"def {function_name}(...):\n"
            "    # Write your solution here\n"
            "    pass\n"
        )

        print(f"[DEBUG] Generated question: {title}")
        print(
            f"[DEBUG] Test cases found: "
            f"{len(question.get('test_cases', []))}"
        )

        return (
            question_text,
            starter_code,
            "✅ Question generated successfully.",
            question,
        )

    except Exception as e:
        print(f"[ERROR] Question generation failed: {e}")

        return (
            "❌ Error generating question.",
            "",
            f"Error: {str(e)}",
            {},
        )


# ============================================================
# SOLUTION EVALUATION
# ============================================================

def evaluate_solution(submitted_code, current_question):

    if not current_question:
        return (
            "⚠️ Please generate a question first.",
            "",
            "",
        )

    if not submitted_code or not submitted_code.strip():
        return (
            "⚠️ Please write your solution before evaluating.",
            "",
            "",
        )

    try:

        title = current_question.get(
            "title",
            "Coding Problem",
        )

        function_name = current_question.get(
            "function_name",
            "solution",
        )

        test_cases = current_question.get(
            "test_cases",
            [],
        )

        print(f"[DEBUG] Evaluating: {title}")
        print(f"[DEBUG] Function: {function_name}")
        print(f"[DEBUG] Test cases: {len(test_cases)}")
        print(f"[DEBUG] Submitted code:\n{submitted_code!r}")

        # ====================================================
        # RUN TEST CASES
        # ====================================================

        result = run_code(
            submitted_code,
            test_cases,
            function_name,
        )

        print(f"[DEBUG] Code runner result: {result}")

        passed = result.get("passed", 0)
        total = result.get("total", 0)
        error = result.get("error")

        if error:

            test_output = (
                "## 🧪 Test Results\n\n"
                "❌ **Evaluation Error**\n\n"
                f"```text\n{error}\n```"
            )

        else:

            if passed == total and total > 0:
                status = "🎉 All test cases passed!"

            elif passed > 0:
                status = "⚠️ Some test cases passed."

            else:
                status = "❌ No test cases passed."

            result_lines = []

            for item in result.get("results", []):

                case_number = item.get("test_case")
                case_status = item.get("status")
                expected = item.get("expected")
                actual = item.get("actual")

                if case_status == "Passed":
                    icon = "✅"
                else:
                    icon = "❌"

                result_lines.append(
                    f"### {icon} Test Case {case_number}\n\n"
                    f"**Status:** {case_status}\n\n"
                    f"**Expected:** `{expected}`\n\n"
                    f"**Actual:** `{actual}`\n\n"
                )

            test_output = (
                "## 🧪 Test Results\n\n"
                f"### {status}\n\n"
                f"**Passed:** `{passed}/{total}`\n\n"
                + "".join(result_lines)
            )

        # ====================================================
        # COMPLEXITY ANALYSIS
        # ====================================================

        try:

            complexity = analyze_complexity(
                submitted_code
            )

            time_complexity = complexity.get(
                "time_complexity",
                "Unable to determine",
            )

            space_complexity = complexity.get(
                "space_complexity",
                "Unable to determine",
            )

            reasoning = complexity.get(
                "reasoning",
                "",
            )

            optimization = complexity.get(
                "optimization_suggestion",
                "",
            )

            complexity_output = (
                "## 📊 Complexity Analysis\n\n"
                "| Metric | Result |\n"
                "|---|---|\n"
                f"| ⏱️ Time Complexity | **{time_complexity}** |\n"
                f"| 💾 Space Complexity | **{space_complexity}** |\n\n"
                "### 🔎 Analysis\n\n"
                f"{reasoning}\n\n"
                "### 🚀 Optimization Suggestion\n\n"
                f"{optimization}"
            )

        except Exception as e:

            print(
                f"[ERROR] Complexity analysis failed: {e}"
            )

            complexity = {}

            complexity_output = (
                "## 📊 Complexity Analysis\n\n"
                "⚠️ Complexity analysis could not be completed.\n\n"
                f"```text\n{str(e)}\n```"
            )

        # ====================================================
        # RAG / AI FEEDBACK
        # ====================================================

        try:

            rag_feedback = generate_rag_feedback(
                current_question,
                submitted_code,
                result,
                complexity,
            )

            feedback_output = (
                "## 🤖 AI Interview Feedback\n\n"
                f"{rag_feedback}"
            )

        except Exception as e:

            print(
                f"[ERROR] RAG feedback failed: {e}"
            )

            feedback_output = (
                "## 🤖 AI Interview Feedback\n\n"
                "⚠️ AI feedback could not be generated.\n\n"
                f"```text\n{str(e)}\n```"
            )

        return (
            test_output,
            complexity_output,
            feedback_output,
        )

    except Exception as e:

        print(
            f"[ERROR] Evaluation failed: {e}"
        )

        return (
            "## ❌ Evaluation Failed\n\n"
            f"```text\n{str(e)}\n```",
            "",
            "",
        )


# ============================================================
# CUSTOM CSS
# ============================================================

CSS = """
.gradio-container {
    max-width: 1200px !important;
    margin: auto !important;
}

#title {
    text-align: center;
    margin-bottom: 5px;
}

#subtitle {
    text-align: center;
    opacity: 0.75;
    margin-bottom: 25px;
}

textarea {
    font-family: "Consolas", "Courier New", monospace !important;
}

#question-box {
    min-height: 420px;
}

#code-editor {
    min-height: 420px;
}

#evaluate-btn {
    min-height: 50px;
    font-size: 17px;
    font-weight: bold;
}

.status-box {
    text-align: center;
}
"""


# ============================================================
# GRADIO UI
# ============================================================

with gr.Blocks(
    title="AI Coding Interview Trainer",
    css=CSS,
    theme=gr.themes.Soft(),
) as demo:

    current_question_state = gr.State({})

    # ========================================================
    # HEADER
    # ========================================================

    gr.Markdown(
        "# 🧠 AI Coding Interview Trainer",
        elem_id="title",
    )

    gr.Markdown(
        "Practice DSA problems, submit your solution, "
        "run test cases, analyze complexity, and receive "
        "AI-powered interview feedback.",
        elem_id="subtitle",
    )

    # ========================================================
    # QUESTION SELECTION
    # ========================================================

    with gr.Row():

        with gr.Column(scale=1):

            gr.Markdown("### 🎯 Choose Your Problem")

            topic_dropdown = gr.Dropdown(
                choices=get_available_topics(),
                value="All Topics",
                label="Topic",
            )

            difficulty_dropdown = gr.Dropdown(
                choices=get_available_difficulties(),
                value="Any Difficulty",
                label="Difficulty",
            )

            generate_button = gr.Button(
                "🎲 Generate Question",
                variant="primary",
            )

            status_output = gr.Markdown(
                "Ready to generate a coding problem.",
                elem_classes="status-box",
            )

        with gr.Column(scale=2):

            question_output = gr.Markdown(
                "# 👋 Welcome!\n\n"
                "Choose a topic and difficulty, then click "
                "**Generate Question** to start your interview.",
                elem_id="question-box",
            )

    gr.Markdown("---")

    # ========================================================
    # CODE EDITOR
    # ========================================================

    gr.Markdown("## 💻 Your Solution")

    code_input = gr.Code(
        label="Python",
        language="python",
        value="",
        lines=18,
        elem_id="code-editor",
    )

    evaluate_button = gr.Button(
        "🚀 Evaluate Solution",
        variant="primary",
        elem_id="evaluate-btn",
    )

    gr.Markdown("---")

    # ========================================================
    # RESULTS
    # ========================================================

    gr.Markdown("## 📋 Evaluation Results")

    with gr.Tabs():

        with gr.Tab("🧪 Test Cases"):

            test_output = gr.Markdown(
                "Submit your solution to see test results."
            )

        with gr.Tab("📊 Complexity"):

            complexity_output = gr.Markdown(
                "Complexity analysis will appear here."
            )

        with gr.Tab("🤖 AI Feedback"):

            feedback_output = gr.Markdown(
                "AI interview feedback will appear here."
            )

    # ========================================================
    # BUTTON EVENTS
    # ========================================================

    generate_button.click(
        fn=generate_new_question,
        inputs=[
            topic_dropdown,
            difficulty_dropdown,
        ],
        outputs=[
            question_output,
            code_input,
            status_output,
            current_question_state,
        ],
    )

    evaluate_button.click(
        fn=evaluate_solution,
        inputs=[
            code_input,
            current_question_state,
        ],
        outputs=[
            test_output,
            complexity_output,
            feedback_output,
        ],
    )


# ============================================================
# LAUNCH
# ============================================================

if __name__ == "__main__":
    demo.launch()