import unittest
from llm.ollama_client import check_connection, generate_response
from evaluation.code_runner import run_code, validate_code_ast, SecurityValidationError
from evaluation.complexity import inspect_code_ast
from services.question_generator import load_all_questions, generate_question

class TestAICodingInterviewTrainer(unittest.TestCase):

    def test_01_ollama_reachable(self):
        """Verify that local Ollama instance is reachable."""
        is_up = check_connection()
        self.assertTrue(is_up, "Local Ollama service on port 11434 should be running and reachable.")

    def test_02_generate_response(self):
        """Verify that Mistral responds via generate_response()."""
        prompt = "Reply with exactly the single word 'CONFIRMED' and nothing else."
        response = generate_response(prompt=prompt, temperature=0.0)
        self.assertIsNotNone(response)
        self.assertGreater(len(response.strip()), 0)
        self.assertIn("CONFIRMED", response.upper())

    def test_03_dataset_loading(self):
        """Verify that DSA dataset loads properly with required fields."""
        questions = load_all_questions()
        self.assertGreaterEqual(len(questions), 30, f"Expected at least 30 questions, found {len(questions)}.")
        
        first = questions[0]
        required_keys = [
            "id", "title", "topic", "difficulty", "description",
            "constraints", "examples", "expected_time_complexity",
            "expected_space_complexity", "function_name", "test_cases"
        ]
        for key in required_keys:
            self.assertIn(key, first, f"Missing required key '{key}' in dataset question.")

    def test_04_code_runner_passing_case(self):
        """Verify that correct Python solution passes all test cases."""
        code = """
def pair_target_sum(nums, target):
    seen = {}
    for i, n in enumerate(nums):
        diff = target - n
        if diff in seen:
            return [seen[diff], i]
        seen[n] = i
    return []
"""
        test_cases = [
            {"inputs": [[2, 7, 11, 15], 9], "expected": [0, 1]},
            {"inputs": [[3, 2, 4], 6], "expected": [1, 2]}
        ]
        res = run_code(code, "pair_target_sum", test_cases)
        self.assertTrue(res["success"])
        self.assertEqual(res["passed_tests"], 2)
        self.assertEqual(res["total_tests"], 2)
        self.assertIsNone(res["error_type"])

    def test_05_code_runner_failing_case(self):
        """Verify that incorrect Python solution reports failure."""
        code = """
def pair_target_sum(nums, target):
    return [0, 0]
"""
        test_cases = [
            {"inputs": [[2, 7, 11, 15], 9], "expected": [0, 1]}
        ]
        res = run_code(code, "pair_target_sum", test_cases)
        self.assertFalse(res["success"])
        self.assertEqual(res["passed_tests"], 0)

    def test_06_code_runner_security_rejection(self):
        """Verify that unauthorized module imports are intercepted by AST."""
        code = """
import os
def pair_target_sum(nums, target):
    return []
"""
        with self.assertRaises(SecurityValidationError):
            validate_code_ast(code)

        res = run_code(code, "pair_target_sum", [{"inputs": [], "expected": []}])
        self.assertFalse(res["success"])
        self.assertEqual(res["error_type"], "SecurityValidationError")

    def test_07_code_runner_timeout(self):
        """Verify that infinite loops are terminated by subprocess timeout."""
        code = """
def pair_target_sum(nums, target):
    while True:
        pass
"""
        res = run_code(code, "pair_target_sum", [{"inputs": [[1], 1], "expected": [1]}], timeout=1.0)
        self.assertFalse(res["success"])
        self.assertEqual(res["error_type"], "TimeoutError")

    def test_08_ast_complexity_inspection(self):
        """Verify AST inspector correctly counts loop depth and detects data structures."""
        code = """
def sample_algo(matrix):
    visited = set()
    output = []
    for row in matrix:
        for val in row:
            if val not in visited:
                visited.add(val)
                output.append(val)
    return output
"""
        metrics = inspect_code_ast(code)
        self.assertEqual(metrics["max_loop_depth"], 2)
        self.assertEqual(metrics["total_loops"], 2)
        self.assertFalse(metrics["has_recursion"])
        self.assertIn("set", metrics["detected_structures"])

    def test_09_question_generator_curated(self):
        """Verify question generator selects problem based on topic and difficulty."""
        q = generate_question(topic="Binary Search", difficulty="Easy")
        self.assertEqual(q["topic"], "Binary Search")
        self.assertEqual(q["difficulty"], "Easy")
        self.assertIn("interviewer_presentation", q)
        self.assertGreater(len(q["interviewer_presentation"]), 20)

if __name__ == "__main__":
    unittest.main()
