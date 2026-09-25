import ast


# ============================================================
# AST COMPLEXITY ANALYZER
# ============================================================

class ComplexityVisitor(ast.NodeVisitor):

    def __init__(self):
        self.loop_depth = 0
        self.max_loop_depth = 0
        self.total_loops = 0
        self.recursion = False
        self.data_structures = set()

    def visit_For(self, node):
        self.total_loops += 1
        self.loop_depth += 1

        self.max_loop_depth = max(
            self.max_loop_depth,
            self.loop_depth
        )

        self.generic_visit(node)

        self.loop_depth -= 1

    def visit_While(self, node):
        self.total_loops += 1
        self.loop_depth += 1

        self.max_loop_depth = max(
            self.max_loop_depth,
            self.loop_depth
        )

        self.generic_visit(node)

        self.loop_depth -= 1

    def visit_Call(self, node):
        if isinstance(node.func, ast.Name):
            if node.func.id == "set":
                self.data_structures.add("set")

            elif node.func.id == "dict":
                self.data_structures.add("dict")

            elif node.func.id == "list":
                self.data_structures.add("list")

        self.generic_visit(node)

    def visit_FunctionDef(self, node):
        function_name = node.name

        for child in ast.walk(node):
            if isinstance(child, ast.Call):
                if (
                    isinstance(child.func, ast.Name)
                    and child.func.id == function_name
                ):
                    self.recursion = True

        self.generic_visit(node)


# ============================================================
# HEURISTIC COMPLEXITY ESTIMATION
# ============================================================

def estimate_complexity(tree):
    visitor = ComplexityVisitor()

    visitor.visit(tree)

    # --------------------------------------------------------
    # TIME COMPLEXITY
    # --------------------------------------------------------

    if visitor.recursion:

        if visitor.max_loop_depth > 0:
            time_complexity = "O(2^N) or higher"
            reasoning = (
                "The solution contains recursion combined "
                "with iterative operations."
            )
        else:
            time_complexity = "O(2^N)"
            reasoning = (
                "The solution contains recursive calls, "
                "suggesting exponential growth."
            )

    elif visitor.max_loop_depth == 0:

        time_complexity = "O(1)"
        reasoning = (
            "No loops or recursive calls were detected "
            "in the submitted solution."
        )

    elif visitor.max_loop_depth == 1:

        time_complexity = "O(N)"
        reasoning = (
            "A single level of iteration was detected."
        )

    elif visitor.max_loop_depth == 2:

        time_complexity = "O(N^2)"
        reasoning = (
            "Two nested levels of iteration were detected."
        )

    elif visitor.max_loop_depth == 3:

        time_complexity = "O(N^3)"
        reasoning = (
            "Three nested levels of iteration were detected."
        )

    else:

        time_complexity = f"O(N^{visitor.max_loop_depth})"
        reasoning = (
            f"{visitor.max_loop_depth} nested loop levels "
            "were detected."
        )

    # --------------------------------------------------------
    # SPACE COMPLEXITY
    # --------------------------------------------------------

    if visitor.data_structures:
        space_complexity = "O(N)"

        reasoning += (
            " Additional memory appears to be used through "
            "data structures such as "
            + ", ".join(sorted(visitor.data_structures))
            + "."
        )

    elif visitor.recursion:
        space_complexity = "O(N)"

        reasoning += (
            " Recursive calls may require additional "
            "call-stack memory."
        )

    else:
        space_complexity = "O(1)"

    # --------------------------------------------------------
    # OPTIMIZATION SUGGESTION
    # --------------------------------------------------------

    if visitor.max_loop_depth >= 2:

        optimization = (
            "Consider whether nested loops can be replaced "
            "with a hash map, set, sorting, or another "
            "more efficient data structure."
        )

    elif visitor.recursion:

        optimization = (
            "Consider whether the recursive approach can "
            "be optimized using memoization or an "
            "iterative solution."
        )

    elif time_complexity == "O(N)":

        optimization = (
            "The detected time complexity is linear. "
            "Check whether the problem requires any "
            "additional optimization."
        )

    else:

        optimization = (
            "The detected complexity is already relatively "
            "efficient for the analyzed structure."
        )

    return {
        "time_complexity": time_complexity,
        "space_complexity": space_complexity,
        "reasoning": reasoning,
        "optimization_suggestion": optimization,
        "loop_depth": visitor.max_loop_depth,
        "total_loops": visitor.total_loops,
        "recursion": visitor.recursion,
        "data_structures": list(visitor.data_structures),
        "method": "Static AST Analysis"
    }


# ============================================================
# PUBLIC FUNCTION
# ============================================================

def analyze_complexity(submitted_code):

    try:
        tree = ast.parse(submitted_code)

        result = estimate_complexity(tree)

        return result

    except SyntaxError as e:

        return {
            "time_complexity": "Unknown",
            "space_complexity": "Unknown",
            "reasoning": f"Unable to analyze code because of syntax error: {e}",
            "optimization_suggestion": "Fix the syntax errors first.",
            "method": "Static AST Analysis"
        }

    except Exception as e:

        return {
            "time_complexity": "Unknown",
            "space_complexity": "Unknown",
            "reasoning": f"Complexity analysis failed: {e}",
            "optimization_suggestion": "Review the submitted code.",
            "method": "Static AST Analysis"
        }