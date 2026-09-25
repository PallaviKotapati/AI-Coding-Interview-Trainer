import json
from pathlib import Path


QUESTIONS = [

    # ========================================================
    # ARRAYS
    # ========================================================

    {
        "id": 41,
        "title": "Maximum Sum Circular Subarray",
        "topic": "Arrays",
        "difficulty": "Hard",
        "function_name": "max_subarray_circular",
        "description": "Given a circular integer array, find the maximum possible sum of a non-empty subarray.",
        "test_cases": [
            {"args": [[1, -2, 3, -2]], "expected": 3},
            {"args": [[5, -3, 5]], "expected": 10},
            {"args": [[-3, -2, -3]], "expected": -2}
        ],
        "expected_time": "O(n)",
        "expected_space": "O(1)",
        "tags": ["array", "kadane", "dynamic-programming"]
    },

    {
        "id": 42,
        "title": "Jump Game",
        "topic": "Arrays",
        "difficulty": "Medium",
        "function_name": "can_jump",
        "description": "Given an array where each element represents the maximum jump length from that position, determine whether you can reach the last index.",
        "test_cases": [
            {"args": [[2, 3, 1, 1, 4]], "expected": True},
            {"args": [[3, 2, 1, 0, 4]], "expected": False},
            {"args": [[0]], "expected": True}
        ],
        "expected_time": "O(n)",
        "expected_space": "O(1)",
        "tags": ["array", "greedy"]
    },

    {
        "id": 43,
        "title": "Jump Game II",
        "topic": "Arrays",
        "difficulty": "Medium",
        "function_name": "min_jumps",
        "description": "Return the minimum number of jumps required to reach the last index.",
        "test_cases": [
            {"args": [[2, 3, 1, 1, 4]], "expected": 2},
            {"args": [[2, 3, 0, 1, 4]], "expected": 2},
            {"args": [[1, 2, 1, 1, 1]], "expected": 3}
        ],
        "expected_time": "O(n)",
        "expected_space": "O(1)",
        "tags": ["array", "greedy"]
    },

    {
        "id": 44,
        "title": "Container With Most Water",
        "topic": "Arrays",
        "difficulty": "Medium",
        "function_name": "max_area",
        "description": "Given heights of vertical lines, find two lines that together contain the most water.",
        "test_cases": [
            {"args": [[1, 8, 6, 2, 5, 4, 8, 3, 7]], "expected": 49},
            {"args": [[1, 1]], "expected": 1},
            {"args": [[4, 3, 2, 1, 4]], "expected": 16}
        ],
        "expected_time": "O(n)",
        "expected_space": "O(1)",
        "tags": ["array", "two-pointers"]
    },

    {
        "id": 45,
        "title": "Trapping Rain Water",
        "topic": "Arrays",
        "difficulty": "Hard",
        "function_name": "trap_rain_water",
        "description": "Given an array representing elevation heights, calculate how much rainwater can be trapped.",
        "test_cases": [
            {"args": [[0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1]], "expected": 6},
            {"args": [[4, 2, 0, 3, 2, 5]], "expected": 9},
            {"args": [[1, 2, 3, 4]], "expected": 0}
        ],
        "expected_time": "O(n)",
        "expected_space": "O(1)",
        "tags": ["array", "two-pointers"]
    },

    # ========================================================
    # STRINGS
    # ========================================================

    {
        "id": 46,
        "title": "Longest Substring Without Repeating Characters",
        "topic": "Strings",
        "difficulty": "Medium",
        "function_name": "longest_unique_substring",
        "description": "Find the length of the longest substring without repeating characters.",
        "test_cases": [
            {"args": ["abcabcbb"], "expected": 3},
            {"args": ["bbbbb"], "expected": 1},
            {"args": ["pwwkew"], "expected": 3}
        ],
        "expected_time": "O(n)",
        "expected_space": "O(n)",
        "tags": ["string", "sliding-window"]
    },

    {
        "id": 47,
        "title": "Longest Palindromic Substring",
        "topic": "Strings",
        "difficulty": "Medium",
        "function_name": "longest_palindrome",
        "description": "Return the longest palindromic substring in a given string.",
        "test_cases": [
            {"args": ["babad"], "expected": "bab"},
            {"args": ["cbbd"], "expected": "bb"},
            {"args": ["a"], "expected": "a"}
        ],
        "expected_time": "O(n^2)",
        "expected_space": "O(1)",
        "tags": ["string", "dynamic-programming"]
    },

    {
        "id": 48,
        "title": "Minimum Window Substring",
        "topic": "Strings",
        "difficulty": "Hard",
        "function_name": "min_window",
        "description": "Find the smallest substring of s that contains all characters of t.",
        "test_cases": [
            {"args": ["ADOBECODEBANC", "ABC"], "expected": "BANC"},
            {"args": ["a", "a"], "expected": "a"},
            {"args": ["a", "aa"], "expected": ""}
        ],
        "expected_time": "O(n)",
        "expected_space": "O(n)",
        "tags": ["string", "sliding-window", "hashmap"]
    },

    {
        "id": 49,
        "title": "String Compression",
        "topic": "Strings",
        "difficulty": "Medium",
        "function_name": "compress_string",
        "description": "Compress consecutive repeated characters using the character followed by its count.",
        "test_cases": [
            {"args": ["aabcccccaaa"], "expected": "a2b1c5a3"},
            {"args": ["abc"], "expected": "a1b1c1"},
            {"args": ["aaaa"], "expected": "a4"}
        ],
        "expected_time": "O(n)",
        "expected_space": "O(n)",
        "tags": ["string"]
    },

    {
        "id": 50,
        "title": "Edit Distance",
        "topic": "Strings",
        "difficulty": "Hard",
        "function_name": "edit_distance",
        "description": "Return the minimum number of insertions, deletions, and replacements needed to convert one string into another.",
        "test_cases": [
            {"args": ["horse", "ros"], "expected": 3},
            {"args": ["intention", "execution"], "expected": 5},
            {"args": ["", "abc"], "expected": 3}
        ],
        "expected_time": "O(m*n)",
        "expected_space": "O(m*n)",
        "tags": ["string", "dynamic-programming"]
    },

    # ========================================================
    # BINARY SEARCH
    # ========================================================

    {
        "id": 51,
        "title": "Search in Rotated Sorted Array",
        "topic": "Binary Search",
        "difficulty": "Medium",
        "function_name": "search_rotated",
        "description": "Search for a target in a rotated sorted array and return its index, or -1 if not found.",
        "test_cases": [
            {"args": [[4, 5, 6, 7, 0, 1, 2], 0], "expected": 4},
            {"args": [[4, 5, 6, 7, 0, 1, 2], 3], "expected": -1},
            {"args": [[1], 0], "expected": -1}
        ],
        "expected_time": "O(log n)",
        "expected_space": "O(1)",
        "tags": ["binary-search"]
    },

    {
        "id": 52,
        "title": "Find Minimum in Rotated Sorted Array",
        "topic": "Binary Search",
        "difficulty": "Medium",
        "function_name": "find_min",
        "description": "Find the minimum element in a rotated sorted array.",
        "test_cases": [
            {"args": [[3, 4, 5, 1, 2]], "expected": 1},
            {"args": [[4, 5, 6, 7, 0, 1, 2]], "expected": 0},
            {"args": [[11, 13, 15, 17]], "expected": 11}
        ],
        "expected_time": "O(log n)",
        "expected_space": "O(1)",
        "tags": ["binary-search"]
    },

    {
        "id": 53,
        "title": "Median of Two Sorted Arrays",
        "topic": "Binary Search",
        "difficulty": "Hard",
        "function_name": "find_median_sorted_arrays",
        "description": "Find the median of two sorted arrays.",
        "test_cases": [
            {"args": [[1, 3], [2]], "expected": 2.0},
            {"args": [[1, 2], [3, 4]], "expected": 2.5},
            {"args": [[0, 0], [0, 0]], "expected": 0.0}
        ],
        "expected_time": "O(log(min(m,n)))",
        "expected_space": "O(1)",
        "tags": ["binary-search", "array"]
    },

    # ========================================================
    # STACK
    # ========================================================

    {
        "id": 54,
        "title": "Daily Temperatures",
        "topic": "Stack",
        "difficulty": "Medium",
        "function_name": "daily_temperatures",
        "description": "For each day, return how many days you must wait until a warmer temperature.",
        "test_cases": [
            {
                "args": [[73, 74, 75, 71, 69, 72, 76, 73]],
                "expected": [1, 1, 4, 2, 1, 1, 0, 0]
            },
            {
                "args": [[30, 40, 50, 60]],
                "expected": [1, 1, 1, 0]
            }
        ],
        "expected_time": "O(n)",
        "expected_space": "O(n)",
        "tags": ["stack", "monotonic-stack"]
    },

    {
        "id": 55,
        "title": "Evaluate Reverse Polish Notation",
        "topic": "Stack",
        "difficulty": "Medium",
        "function_name": "eval_rpn",
        "description": "Evaluate an arithmetic expression written in Reverse Polish Notation.",
        "test_cases": [
            {"args": [["2", "1", "+", "3", "*"]], "expected": 9},
            {"args": [["4", "13", "5", "/", "+"]], "expected": 6},
            {"args": [["10", "6", "9", "3", "+", "-11", "*", "/", "*", "17", "+", "5", "+"]], "expected": 22}
        ],
        "expected_time": "O(n)",
        "expected_space": "O(n)",
        "tags": ["stack"]
    },

    {
        "id": 56,
        "title": "Largest Rectangle in Histogram",
        "topic": "Stack",
        "difficulty": "Hard",
        "function_name": "largest_rectangle",
        "description": "Given bar heights in a histogram, find the largest rectangular area.",
        "test_cases": [
            {"args": [[2, 1, 5, 6, 2, 3]], "expected": 10},
            {"args": [[2, 4]], "expected": 4},
            {"args": [[1, 1, 1]], "expected": 3}
        ],
        "expected_time": "O(n)",
        "expected_space": "O(n)",
        "tags": ["stack", "monotonic-stack"]
    },

    # ========================================================
    # LINKED LIST
    # ========================================================

    {
        "id": 57,
        "title": "Reverse Linked List",
        "topic": "Linked Lists",
        "difficulty": "Easy",
        "function_name": "reverse_list",
        "description": "Reverse a singly linked list represented as a Python list and return the reversed list.",
        "test_cases": [
            {"args": [[1, 2, 3, 4, 5]], "expected": [5, 4, 3, 2, 1]},
            {"args": [[1, 2]], "expected": [2, 1]},
            {"args": [[]], "expected": []}
        ],
        "expected_time": "O(n)",
        "expected_space": "O(1)",
        "tags": ["linked-list"]
    },

    {
        "id": 58,
        "title": "Middle of Linked List",
        "topic": "Linked Lists",
        "difficulty": "Easy",
        "function_name": "middle_node",
        "description": "Return the middle element of a list. For an even-length list, return the second middle element.",
        "test_cases": [
            {"args": [[1, 2, 3, 4, 5]], "expected": 3},
            {"args": [[1, 2, 3, 4, 5, 6]], "expected": 4},
            {"args": [[1]], "expected": 1}
        ],
        "expected_time": "O(n)",
        "expected_space": "O(1)",
        "tags": ["linked-list", "two-pointers"]
    },

    {
        "id": 59,
        "title": "Detect Cycle",
        "topic": "Linked Lists",
        "difficulty": "Medium",
        "function_name": "has_cycle",
        "description": "Given a list and a cycle entry index, determine whether the linked list contains a cycle.",
        "test_cases": [
            {"args": [[3, 2, 0, -4], 1], "expected": True},
            {"args": [[1, 2], 0], "expected": True},
            {"args": [[1], -1], "expected": False}
        ],
        "expected_time": "O(n)",
        "expected_space": "O(1)",
        "tags": ["linked-list", "two-pointers"]
    },

    # ========================================================
    # GREEDY
    # ========================================================

    {
        "id": 60,
        "title": "Assign Cookies",
        "topic": "Greedy",
        "difficulty": "Easy",
        "function_name": "assign_cookies",
        "description": "Given children's greed factors and cookie sizes, maximize the number of children who can be satisfied.",
        "test_cases": [
            {"args": [[1, 2, 3], [1, 1]], "expected": 1},
            {"args": [[1, 2], [1, 2, 3]], "expected": 2},
            {"args": [[10], [1, 2, 3]], "expected": 0}
        ],
        "expected_time": "O(n log n)",
        "expected_space": "O(1)",
        "tags": ["greedy", "sorting"]
    },

    {
        "id": 61,
        "title": "Lemonade Change",
        "topic": "Greedy",
        "difficulty": "Easy",
        "function_name": "lemonade_change",
        "description": "Determine whether you can provide correct change to every customer in sequence when lemonade costs $5.",
        "test_cases": [
            {"args": [[5, 5, 5, 10, 20]], "expected": True},
            {"args": [[5, 5, 10, 10, 20]], "expected": False},
            {"args": [[5, 5, 5, 5, 10, 5, 10, 10, 10, 20]], "expected": True}
        ],
        "expected_time": "O(n)",
        "expected_space": "O(1)",
        "tags": ["greedy"]
    },

    {
        "id": 62,
        "title": "Gas Station",
        "topic": "Greedy",
        "difficulty": "Medium",
        "function_name": "can_complete_circuit",
        "description": "Given gas available and gas cost between stations, return the starting station index that allows completing the circuit, or -1.",
        "test_cases": [
            {"args": [[1, 2, 3, 4, 5], [3, 4, 5, 1, 2]], "expected": 3},
            {"args": [[2, 3, 4], [3, 4, 3]], "expected": -1},
            {"args": [[5], [4]], "expected": 0}
        ],
        "expected_time": "O(n)",
        "expected_space": "O(1)",
        "tags": ["greedy"]
    },

    # ========================================================
    # DYNAMIC PROGRAMMING
    # ========================================================

    {
        "id": 63,
        "title": "Longest Increasing Subsequence",
        "topic": "Dynamic Programming",
        "difficulty": "Medium",
        "function_name": "lis_length",
        "description": "Return the length of the longest strictly increasing subsequence.",
        "test_cases": [
            {"args": [[10, 9, 2, 5, 3, 7, 101, 18]], "expected": 4},
            {"args": [[0, 1, 0, 3, 2, 3]], "expected": 4},
            {"args": [[7, 7, 7, 7]], "expected": 1}
        ],
        "expected_time": "O(n^2)",
        "expected_space": "O(n)",
        "tags": ["dynamic-programming"]
    },

    {
        "id": 64,
        "title": "0/1 Knapsack",
        "topic": "Dynamic Programming",
        "difficulty": "Hard",
        "function_name": "knapsack",
        "description": "Given item weights, values, and a capacity, return the maximum value that can be carried without exceeding the capacity.",
        "test_cases": [
            {"args": [[1, 3, 4, 5], [1, 4, 5, 7], 7], "expected": 9},
            {"args": [[2, 3, 4], [4, 5, 6], 5], "expected": 9},
            {"args": [[1, 2], [1, 2], 0], "expected": 0}
        ],
        "expected_time": "O(n*capacity)",
        "expected_space": "O(capacity)",
        "tags": ["dynamic-programming", "knapsack"]
    },

    {
        "id": 65,
        "title": "Partition Equal Subset Sum",
        "topic": "Dynamic Programming",
        "difficulty": "Medium",
        "function_name": "can_partition",
        "description": "Determine whether an array can be partitioned into two subsets with equal sum.",
        "test_cases": [
            {"args": [[1, 5, 11, 5]], "expected": True},
            {"args": [[1, 2, 3, 5]], "expected": False},
            {"args": [[2, 2, 2, 2]], "expected": True}
        ],
        "expected_time": "O(n*sum)",
        "expected_space": "O(sum)",
        "tags": ["dynamic-programming"]
    },

    # ========================================================
    # TREES
    # ========================================================

    {
        "id": 66,
        "title": "Maximum Depth of Binary Tree",
        "topic": "Trees",
        "difficulty": "Easy",
        "function_name": "max_depth",
        "description": "Given a binary tree represented as a nested list [value, left, right], return its maximum depth.",
        "test_cases": [
            {"args": [[3, [9, None, None], [20, [15, None, None], [7, None, None]]]], "expected": 3},
            {"args": [[1, None, [2, None, None]]], "expected": 2},
            {"args": [None], "expected": 0}
        ],
        "expected_time": "O(n)",
        "expected_space": "O(h)",
        "tags": ["tree", "recursion"]
    },

    {
        "id": 67,
        "title": "Binary Tree Level Order Traversal",
        "topic": "Trees",
        "difficulty": "Medium",
        "function_name": "level_order",
        "description": "Return the level-order traversal of a binary tree represented as a nested structure.",
        "test_cases": [
            {
                "args": [[3, [9, None, None], [20, [15, None, None], [7, None, None]]]],
                "expected": [[3], [9, 20], [15, 7]]
            }
        ],
        "expected_time": "O(n)",
        "expected_space": "O(n)",
        "tags": ["tree", "bfs"]
    },

    {
        "id": 68,
        "title": "Validate Binary Search Tree",
        "topic": "Trees",
        "difficulty": "Medium",
        "function_name": "is_valid_bst",
        "description": "Determine whether a binary tree satisfies the binary search tree property.",
        "test_cases": [
            {"args": [[2, [1, None, None], [3, None, None]]], "expected": True},
            {"args": [[5, [1, None, None], [4, [3, None, None], [6, None, None]]]], "expected": False},
            {"args": [[1, None, None]], "expected": True}
        ],
        "expected_time": "O(n)",
        "expected_space": "O(h)",
        "tags": ["tree", "dfs"]
    },

    # ========================================================
    # GRAPHS
    # ========================================================

    {
        "id": 69,
        "title": "Number of Islands",
        "topic": "Graphs",
        "difficulty": "Medium",
        "function_name": "num_islands",
        "description": "Given a grid of 1s and 0s, count the number of connected groups of 1s.",
        "test_cases": [
            {
                "args": [[
                    ["1", "1", "0", "0"],
                    ["1", "0", "0", "1"],
                    ["0", "0", "1", "1"]
                ]],
                "expected": 3
            },
            {
                "args": [[
                    ["1", "1"],
                    ["1", "1"]
                ]],
                "expected": 1
            },
            {
                "args": [["0"]],
                "expected": 0
            }
        ],
        "expected_time": "O(m*n)",
        "expected_space": "O(m*n)",
        "tags": ["graph", "bfs", "dfs"]
    },

    {
        "id": 70,
        "title": "Course Schedule",
        "topic": "Graphs",
        "difficulty": "Medium",
        "function_name": "can_finish",
        "description": "Given the number of courses and prerequisite pairs, determine whether all courses can be completed.",
        "test_cases": [
            {"args": [2, [[1, 0]]], "expected": True},
            {"args": [2, [[1, 0], [0, 1]]], "expected": False},
            {"args": [3, [[1, 0], [2, 1]]], "expected": True}
        ],
        "expected_time": "O(V+E)",
        "expected_space": "O(V+E)",
        "tags": ["graph", "topological-sort"]
    }
]


# ============================================================
# UPDATE DATASET
# ============================================================

BASE_DIR = Path(__file__).resolve().parent
QUESTIONS_FILE = BASE_DIR / "dsa_questions.json"

with open(QUESTIONS_FILE, "r", encoding="utf-8") as f:
    existing_questions = json.load(f)

existing_ids = {
    question["id"]
    for question in existing_questions
}

new_questions = [
    question
    for question in QUESTIONS
    if question["id"] not in existing_ids
]

updated_questions = existing_questions + new_questions

with open(
    QUESTIONS_FILE,
    "w",
    encoding="utf-8",
) as f:
    json.dump(
        updated_questions,
        f,
        indent=2,
        ensure_ascii=False,
    )

print(f"Existing questions: {len(existing_questions)}")
print(f"Questions added: {len(new_questions)}")
print(f"Total questions: {len(updated_questions)}")