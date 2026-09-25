import ast
import json
import subprocess
import sys
import tempfile
import time
from pathlib import Path


# ============================================================
# SAFETY VALIDATION
# ============================================================

class SafetyVisitor(ast.NodeVisitor):

    FORBIDDEN = {
        "import",
        "importfrom",
        "exec",
        "eval",
        "open",
        "compile",
        "__import__",
    }

    def __init__(self):
        self.errors = []

    def visit_Import(self, node):
        self.errors.append("Import statements are not allowed.")
        self.generic_visit(node)

    def visit_ImportFrom(self, node):
        self.errors.append("Import statements are not allowed.")
        self.generic_visit(node)

    def visit_Call(self, node):
        if isinstance(node.func, ast.Name):
            if node.func.id in self.FORBIDDEN:
                self.errors.append(
                    f"Use of '{node.func.id}' is not allowed."
                )

        self.generic_visit(node)

    def visit_Name(self, node):
        if node.id in {"exec", "eval", "open", "__import__"}:
            self.errors.append(
                f"Use of '{node.id}' is not allowed."
            )

        self.generic_visit(node)


def validate_code_ast(code):
    try:
        tree = ast.parse(code)

        visitor = SafetyVisitor()
        visitor.visit(tree)

        if visitor.errors:
            return False, visitor.errors

        return True, []

    except SyntaxError as e:
        return False, [f"Syntax error: {e}"]


# ============================================================
# TEST CASE NORMALIZATION
# ============================================================

def normalize_test_cases(test_cases):
    """
    Supports both formats:

    {
        "args": [[2, 7, 11, 15], 9],
        "expected": [0, 1]
    }

    and

    {
        "inputs": [[2, 7, 11, 15], 9],
        "expected": [0, 1]
    }
    """

    normalized = []

    for test_case in test_cases:

        if "inputs" in test_case:
            inputs = test_case["inputs"]

        elif "args" in test_case:
            inputs = test_case["args"]

        else:
            inputs = []

        normalized.append(
            {
                "inputs": inputs,
                "expected": test_case.get("expected"),
            }
        )

    return normalized


# ============================================================
# HARNESS GENERATION
# ============================================================

def generate_harness(
    submitted_code,
    test_cases,
    function_name,
    result_file,
):

    test_cases_json = json.dumps(test_cases)

    harness = f'''
import json
import traceback

RESULT_FILE = {result_file!r}

# ============================================================
# USER SUBMITTED CODE
# ============================================================

{submitted_code}

# ============================================================
# TEST CASES
# ============================================================

test_cases = json.loads({test_cases_json!r})

results = []
passed = 0

for index, test_case in enumerate(test_cases, start=1):

    inputs = test_case.get("inputs", [])
    expected = test_case.get("expected")

    try:

        function_to_call = {function_name!r}

        if function_to_call not in globals():
            raise NameError(
                f"Required function '{{function_to_call}}' "
                "was not found."
            )

        function = globals()[function_to_call]

        actual = function(*inputs)

        if actual == expected:

            status = "Passed"
            passed += 1

        else:

            status = "Failed"

        results.append(
            {{
                "test_case": index,
                "status": status,
                "input": inputs,
                "expected": expected,
                "actual": actual,
            }}
        )

    except Exception as e:

        results.append(
            {{
                "test_case": index,
                "status": "Error",
                "input": inputs,
                "expected": expected,
                "actual": None,
                "error": str(e),
            }}
        )

final_result = {{
    "passed": passed,
    "total": len(test_cases),
    "results": results,
    "error": None,
}}

try:

    with open(RESULT_FILE, "w", encoding="utf-8") as f:
        json.dump(final_result, f)

except Exception as e:

    print(
        "RESULT_WRITE_ERROR:",
        str(e)
    )
''' 

    return harness


# ============================================================
# RUN CODE
# ============================================================

def run_code(
    submitted_code,
    test_cases,
    function_name,
    timeout=5,
):

    # --------------------------------------------------------
    # Validate submitted code
    # --------------------------------------------------------

    is_valid, errors = validate_code_ast(
        submitted_code
    )

    if not is_valid:

        return {
            "passed": 0,
            "total": len(test_cases),
            "results": [],
            "error": "\n".join(errors),
            "execution_time": 0,
        }

    # --------------------------------------------------------
    # Normalize test cases
    # --------------------------------------------------------

    normalized_tests = normalize_test_cases(
        test_cases
    )

    # --------------------------------------------------------
    # Temporary files
    # --------------------------------------------------------

    temp_dir = tempfile.mkdtemp(
        prefix="coding_evaluator_"
    )

    script_path = Path(temp_dir) / "solution.py"
    result_path = Path(temp_dir) / "result.json"

    # --------------------------------------------------------
    # Generate harness
    # --------------------------------------------------------

    harness = generate_harness(
        submitted_code=submitted_code,
        test_cases=normalized_tests,
        function_name=function_name,
        result_file=str(result_path),
    )

    script_path.write_text(
        harness,
        encoding="utf-8",
    )

    # --------------------------------------------------------
    # Execute
    # --------------------------------------------------------

    start_time = time.time()

    try:

        process = subprocess.run(
            [
                sys.executable,
                str(script_path),
            ],
            capture_output=True,
            text=True,
            timeout=timeout,
        )

        execution_time = time.time() - start_time

    except subprocess.TimeoutExpired:

        return {
            "passed": 0,
            "total": len(test_cases),
            "results": [],
            "error": (
                f"Execution timed out after "
                f"{timeout} seconds."
            ),
            "execution_time": time.time() - start_time,
        }

    except Exception as e:

        return {
            "passed": 0,
            "total": len(test_cases),
            "results": [],
            "error": str(e),
            "execution_time": time.time() - start_time,
        }

    # --------------------------------------------------------
    # Read result file
    # --------------------------------------------------------

    if result_path.exists():

        try:

            with open(
                result_path,
                "r",
                encoding="utf-8",
            ) as f:

                result = json.load(f)

            result["execution_time"] = execution_time

            return result

        except Exception as e:

            return {
                "passed": 0,
                "total": len(test_cases),
                "results": [],
                "error": (
                    f"Could not read evaluator result: {e}"
                ),
                "execution_time": execution_time,
            }

    # --------------------------------------------------------
    # Handle execution errors
    # --------------------------------------------------------

    stderr = process.stderr.strip()

    stdout = process.stdout.strip()

    error_message = stderr or stdout

    if not error_message:
        error_message = "Unknown execution error."

    return {
        "passed": 0,
        "total": len(test_cases),
        "results": [],
        "error": error_message,
        "execution_time": execution_time,
    }


# ============================================================
# DIRECT TEST
# ============================================================

if __name__ == "__main__":

    code = """
def two_sum(nums, target):
    seen = {}

    for i, num in enumerate(nums):

        complement = target - num

        if complement in seen:
            return [seen[complement], i]

        seen[num] = i

    return []
"""

    tests = [
        {
            "args": [[2, 7, 11, 15], 9],
            "expected": [0, 1],
        },
        {
            "args": [[3, 2, 4], 6],
            "expected": [1, 2],
        },
        {
            "args": [[3, 3], 6],
            "expected": [0, 1],
        },
    ]

    print(
        run_code(
            code,
            tests,
            "two_sum",
        )
    )