import json
from pathlib import Path


QUESTIONS = [
    {
        "id": 9,
        "title": "Contains Duplicate",
        "topic": "Arrays",
        "difficulty": "Easy",
        "function_name": "contains_duplicate",
        "description": "Given a list of integers, return True if any value appears at least twice, otherwise return False.",
        "test_cases": [
            {"args": [[1, 2, 3, 1]], "expected": True},
            {"args": [[1, 2, 3, 4]], "expected": False},
            {"args": [[1, 1]], "expected": True}
        ],
        "expected_time": "O(n)",
        "expected_space": "O(n)",
        "tags": ["array", "hashset"]
    },
    {
        "id": 10,
        "title": "Best Time to Buy and Sell Stock",
        "topic": "Arrays",
        "difficulty": "Easy",
        "function_name": "max_profit",
        "description": "Given daily stock prices, find the maximum profit possible from buying on one day and selling on a later day.",
        "test_cases": [
            {"args": [[7, 1, 5, 3, 6, 4]], "expected": 5},
            {"args": [[7, 6, 4, 3, 1]], "expected": 0},
            {"args": [[2, 4, 1]], "expected": 2}
        ],
        "expected_time": "O(n)",
        "expected_space": "O(1)",
        "tags": ["array", "greedy"]
    },
    {
        "id": 11,
        "title": "Move Zeroes",
        "topic": "Arrays",
        "difficulty": "Easy",
        "function_name": "move_zeroes",
        "description": "Move all zeroes in an array to the end while maintaining the relative order of the non-zero elements. Return the modified array.",
        "test_cases": [
            {"args": [[0, 1, 0, 3, 12]], "expected": [1, 3, 12, 0, 0]},
            {"args": [[0]], "expected": [0]},
            {"args": [[1, 2, 3]], "expected": [1, 2, 3]}
        ],
        "expected_time": "O(n)",
        "expected_space": "O(1)",
        "tags": ["array", "two-pointers"]
    },
    {
        "id": 12,
        "title": "Valid Anagram",
        "topic": "Strings",
        "difficulty": "Easy",
        "function_name": "is_anagram",
        "description": "Given two strings, determine whether they are anagrams of each other.",
        "test_cases": [
            {"args": ["anagram", "nagaram"], "expected": True},
            {"args": ["rat", "car"], "expected": False},
            {"args": ["listen", "silent"], "expected": True}
        ],
        "expected_time": "O(n)",
        "expected_space": "O(n)",
        "tags": ["string", "hashmap"]
    },
    {
        "id": 13,
        "title": "Valid Palindrome",
        "topic": "Strings",
        "difficulty": "Easy",
        "function_name": "is_palindrome",
        "description": "Determine whether a string is a palindrome after converting uppercase letters to lowercase and ignoring non-alphanumeric characters.",
        "test_cases": [
            {"args": ["A man, a plan, a canal: Panama"], "expected": True},
            {"args": ["race a car"], "expected": False},
            {"args": [" "], "expected": True}
        ],
        "expected_time": "O(n)",
        "expected_space": "O(1)",
        "tags": ["string", "two-pointers"]
    },
    {
        "id": 14,
        "title": "Longest Common Prefix",
        "topic": "Strings",
        "difficulty": "Easy",
        "function_name": "longest_common_prefix",
        "description": "Find the longest common prefix shared by all strings in a list.",
        "test_cases": [
            {"args": [["flower", "flow", "flight"]], "expected": "fl"},
            {"args": [["dog", "racecar", "car"]], "expected": ""},
            {"args": [["interview", "internet", "internal"]], "expected": "inter"}
        ],
        "expected_time": "O(n*m)",
        "expected_space": "O(1)",
        "tags": ["string"]
    },
    {
        "id": 15,
        "title": "Search Insert Position",
        "topic": "Binary Search",
        "difficulty": "Easy",
        "function_name": "search_insert",
        "description": "Given a sorted array and a target value, return the index if found. Otherwise return the index where it should be inserted.",
        "test_cases": [
            {"args": [[1, 3, 5, 6], 5], "expected": 2},
            {"args": [[1, 3, 5, 6], 2], "expected": 1},
            {"args": [[1, 3, 5, 6], 7], "expected": 4}
        ],
        "expected_time": "O(log n)",
        "expected_space": "O(1)",
        "tags": ["binary-search"]
    },
    {
        "id": 16,
        "title": "Missing Number",
        "topic": "Arrays",
        "difficulty": "Easy",
        "function_name": "missing_number",
        "description": "Given an array containing n distinct numbers from 0 to n, return the only number missing.",
        "test_cases": [
            {"args": [[3, 0, 1]], "expected": 2},
            {"args": [[0, 1]], "expected": 2},
            {"args": [[9, 6, 4, 2, 3, 5, 7, 0, 1]], "expected": 8}
        ],
        "expected_time": "O(n)",
        "expected_space": "O(1)",
        "tags": ["array", "math"]
    },
    {
        "id": 17,
        "title": "Single Number",
        "topic": "Arrays",
        "difficulty": "Easy",
        "function_name": "single_number",
        "description": "Every element appears twice except one. Find the element that appears only once.",
        "test_cases": [
            {"args": [[2, 2, 1]], "expected": 1},
            {"args": [[4, 1, 2, 1, 2]], "expected": 4},
            {"args": [[1]], "expected": 1}
        ],
        "expected_time": "O(n)",
        "expected_space": "O(1)",
        "tags": ["array", "bit-manipulation"]
    },
    {
        "id": 18,
        "title": "Majority Element",
        "topic": "Arrays",
        "difficulty": "Easy",
        "function_name": "majority_element",
        "description": "Given an array, return the element that appears more than n/2 times.",
        "test_cases": [
            {"args": [[3, 2, 3]], "expected": 3},
            {"args": [[2, 2, 1, 1, 1, 2, 2]], "expected": 2},
            {"args": [[1]], "expected": 1}
        ],
        "expected_time": "O(n)",
        "expected_space": "O(1)",
        "tags": ["array", "boyer-moore"]
    },
    {
        "id": 19,
        "title": "Product of Array Except Self",
        "topic": "Arrays",
        "difficulty": "Medium",
        "function_name": "product_except_self",
        "description": "Return an array where each element is the product of all elements except the element at that index.",
        "test_cases": [
            {"args": [[1, 2, 3, 4]], "expected": [24, 12, 8, 6]},
            {"args": [[-1, 1, 0, -3, 3]], "expected": [0, 0, 9, 0, 0]},
            {"args": [[2, 3]], "expected": [3, 2]}
        ],
        "expected_time": "O(n)",
        "expected_space": "O(1)",
        "tags": ["array", "prefix-product"]
    },
    {
        "id": 20,
        "title": "Maximum Product Subarray",
        "topic": "Arrays",
        "difficulty": "Medium",
        "function_name": "max_product",
        "description": "Find the contiguous subarray with the largest product.",
        "test_cases": [
            {"args": [[2, 3, -2, 4]], "expected": 6},
            {"args": [[-2, 0, -1]], "expected": 0},
            {"args": [[-2, 3, -4]], "expected": 24}
        ],
        "expected_time": "O(n)",
        "expected_space": "O(1)",
        "tags": ["array", "dynamic-programming"]
    },
    {
        "id": 21,
        "title": "Climbing Stairs",
        "topic": "Dynamic Programming",
        "difficulty": "Easy",
        "function_name": "climb_stairs",
        "description": "You can climb either one or two steps at a time. Return the number of distinct ways to reach the top of n steps.",
        "test_cases": [
            {"args": [2], "expected": 2},
            {"args": [3], "expected": 3},
            {"args": [5], "expected": 8}
        ],
        "expected_time": "O(n)",
        "expected_space": "O(1)",
        "tags": ["dynamic-programming"]
    },
    {
        "id": 22,
        "title": "House Robber",
        "topic": "Dynamic Programming",
        "difficulty": "Medium",
        "function_name": "rob",
        "description": "Given money in houses along a street, maximize the amount stolen without robbing adjacent houses.",
        "test_cases": [
            {"args": [[1, 2, 3, 1]], "expected": 4},
            {"args": [[2, 7, 9, 3, 1]], "expected": 12},
            {"args": [[2, 1, 1, 2]], "expected": 4}
        ],
        "expected_time": "O(n)",
        "expected_space": "O(1)",
        "tags": ["dynamic-programming"]
    },
    {
        "id": 23,
        "title": "Coin Change",
        "topic": "Dynamic Programming",
        "difficulty": "Medium",
        "function_name": "coin_change",
        "description": "Given coin denominations and an amount, return the fewest number of coins needed to make that amount. Return -1 if impossible.",
        "test_cases": [
            {"args": [[1, 2, 5], 11], "expected": 3},
            {"args": [[2], 3], "expected": -1},
            {"args": [[1], 0], "expected": 0}
        ],
        "expected_time": "O(amount * coins)",
        "expected_space": "O(amount)",
        "tags": ["dynamic-programming", "coin-change"]
    },
    {
        "id": 24,
        "title": "Fibonacci Number",
        "topic": "Dynamic Programming",
        "difficulty": "Easy",
        "function_name": "fibonacci",
        "description": "Return the nth Fibonacci number.",
        "test_cases": [
            {"args": [2], "expected": 1},
            {"args": [5], "expected": 5},
            {"args": [10], "expected": 55}
        ],
        "expected_time": "O(n)",
        "expected_space": "O(1)",
        "tags": ["dynamic-programming", "recursion"]
    },
    {
        "id": 25,
        "title": "Length of Last Word",
        "topic": "Strings",
        "difficulty": "Easy",
        "function_name": "length_of_last_word",
        "description": "Given a string containing words and spaces, return the length of the last word.",
        "test_cases": [
            {"args": ["Hello World"], "expected": 5},
            {"args": ["   fly me   to   the moon  "], "expected": 4},
            {"args": ["luffy is still joyboy"], "expected": 6}
        ],
        "expected_time": "O(n)",
        "expected_space": "O(1)",
        "tags": ["string"]
    },
    {
        "id": 26,
        "title": "Reverse Words in a String",
        "topic": "Strings",
        "difficulty": "Medium",
        "function_name": "reverse_words",
        "description": "Reverse the order of words in a string and remove extra spaces.",
        "test_cases": [
            {"args": ["the sky is blue"], "expected": "blue is sky the"},
            {"args": ["  hello world  "], "expected": "world hello"},
            {"args": ["a good   example"], "expected": "example good a"}
        ],
        "expected_time": "O(n)",
        "expected_space": "O(n)",
        "tags": ["string"]
    },
    {
        "id": 27,
        "title": "First Unique Character",
        "topic": "Hashing",
        "difficulty": "Easy",
        "function_name": "first_unique_char",
        "description": "Return the index of the first non-repeating character in a string. Return -1 if none exists.",
        "test_cases": [
            {"args": ["leetcode"], "expected": 0},
            {"args": ["loveleetcode"], "expected": 2},
            {"args": ["aabb"], "expected": -1}
        ],
        "expected_time": "O(n)",
        "expected_space": "O(n)",
        "tags": ["string", "hashmap"]
    },
    {
        "id": 28,
        "title": "Group Anagrams",
        "topic": "Hashing",
        "difficulty": "Medium",
        "function_name": "group_anagrams",
        "description": "Group strings that are anagrams of each other. Return the groups as a list.",
        "test_cases": [
            {
                "args": [["eat", "tea", "tan", "ate", "nat", "bat"]],
                "expected": [
                    ["eat", "tea", "ate"],
                    ["tan", "nat"],
                    ["bat"]
                ]
            }
        ],
        "expected_time": "O(n*k)",
        "expected_space": "O(n*k)",
        "tags": ["hashmap", "string"]
    },
    {
        "id": 29,
        "title": "Top K Frequent Elements",
        "topic": "Hashing",
        "difficulty": "Medium",
        "function_name": "top_k_frequent",
        "description": "Return the k most frequent elements in an array.",
        "test_cases": [
            {"args": [[1, 1, 1, 2, 2, 3], 2], "expected": [1, 2]},
            {"args": [[1], 1], "expected": [1]},
            {"args": [[4, 4, 4, 5, 5, 6], 1], "expected": [4]}
        ],
        "expected_time": "O(n)",
        "expected_space": "O(n)",
        "tags": ["hashmap", "heap"]
    },
    {
        "id": 30,
        "title": "Three Sum",
        "topic": "Arrays",
        "difficulty": "Medium",
        "function_name": "three_sum",
        "description": "Find all unique triplets in an array that sum to zero.",
        "test_cases": [
            {
                "args": [[-1, 0, 1, 2, -1, -4]],
                "expected": [[-1, -1, 2], [-1, 0, 1]]
            },
            {"args": [[0, 1, 1]], "expected": []},
            {"args": [[0, 0, 0]], "expected": [[0, 0, 0]]}
        ],
        "expected_time": "O(n^2)",
        "expected_space": "O(1)",
        "tags": ["array", "two-pointers"]
    },
    {
        "id": 31,
        "title": "Merge Intervals",
        "topic": "Arrays",
        "difficulty": "Medium",
        "function_name": "merge_intervals",
        "description": "Merge all overlapping intervals and return the resulting non-overlapping intervals.",
        "test_cases": [
            {
                "args": [[[1, 3], [2, 6], [8, 10], [15, 18]]],
                "expected": [[1, 6], [8, 10], [15, 18]]
            },
            {
                "args": [[[1, 4], [4, 5]]],
                "expected": [[1, 5]]
            }
        ],
        "expected_time": "O(n log n)",
        "expected_space": "O(n)",
        "tags": ["array", "sorting"]
    },
    {
        "id": 32,
        "title": "Insert Interval",
        "topic": "Arrays",
        "difficulty": "Medium",
        "function_name": "insert_interval",
        "description": "Insert a new interval into a sorted list of non-overlapping intervals and merge if necessary.",
        "test_cases": [
            {
                "args": [[[1, 3], [6, 9]], [2, 5]],
                "expected": [[1, 5], [6, 9]]
            },
            {
                "args": [[], [5, 7]],
                "expected": [[5, 7]]
            }
        ],
        "expected_time": "O(n)",
        "expected_space": "O(n)",
        "tags": ["array", "intervals"]
    },
    {
        "id": 33,
        "title": "Matrix Transpose",
        "topic": "Matrix",
        "difficulty": "Easy",
        "function_name": "transpose",
        "description": "Return the transpose of a matrix.",
        "test_cases": [
            {
                "args": [[[1, 2, 3], [4, 5, 6]]],
                "expected": [[1, 4], [2, 5], [3, 6]]
            },
            {
                "args": [[[1, 2], [3, 4]]],
                "expected": [[1, 3], [2, 4]]
            }
        ],
        "expected_time": "O(m*n)",
        "expected_space": "O(m*n)",
        "tags": ["matrix"]
    },
    {
        "id": 34,
        "title": "Spiral Matrix",
        "topic": "Matrix",
        "difficulty": "Medium",
        "function_name": "spiral_order",
        "description": "Return all elements of a matrix in spiral order.",
        "test_cases": [
            {
                "args": [[[1, 2, 3], [4, 5, 6], [7, 8, 9]]],
                "expected": [1, 2, 3, 6, 9, 8, 7, 4, 5]
            },
            {
                "args": [[[1, 2, 3, 4]]],
                "expected": [1, 2, 3, 4]
            }
        ],
        "expected_time": "O(m*n)",
        "expected_space": "O(m*n)",
        "tags": ["matrix"]
    },
    {
        "id": 35,
        "title": "Rotate Array",
        "topic": "Arrays",
        "difficulty": "Medium",
        "function_name": "rotate_array",
        "description": "Rotate an array to the right by k positions and return the resulting array.",
        "test_cases": [
            {"args": [[1, 2, 3, 4, 5, 6, 7], 3], "expected": [5, 6, 7, 1, 2, 3, 4]},
            {"args": [[-1, -100, 3, 99], 2], "expected": [3, 99, -1, -100]},
            {"args": [[1, 2], 1], "expected": [2, 1]}
        ],
        "expected_time": "O(n)",
        "expected_space": "O(n)",
        "tags": ["array"]
    },
    {
        "id": 36,
        "title": "Intersection of Two Arrays",
        "topic": "Hashing",
        "difficulty": "Easy",
        "function_name": "intersection",
        "description": "Return the unique elements that appear in both arrays.",
        "test_cases": [
            {"args": [[1, 2, 2, 1], [2, 2]], "expected": [2]},
            {"args": [[4, 9, 5], [9, 4, 9, 8, 4]], "expected": [4, 9]},
            {"args": [[1, 2], [3, 4]], "expected": []}
        ],
        "expected_time": "O(n+m)",
        "expected_space": "O(n+m)",
        "tags": ["hashset", "array"]
    },
    {
        "id": 37,
        "title": "Count Vowels",
        "topic": "Strings",
        "difficulty": "Easy",
        "function_name": "count_vowels",
        "description": "Count the number of vowels in a string. Treat uppercase and lowercase vowels equally.",
        "test_cases": [
            {"args": ["hello"], "expected": 2},
            {"args": ["AEIOU"], "expected": 5},
            {"args": ["xyz"], "expected": 0}
        ],
        "expected_time": "O(n)",
        "expected_space": "O(1)",
        "tags": ["string"]
    },
    {
        "id": 38,
        "title": "Reverse Integer",
        "topic": "Math",
        "difficulty": "Medium",
        "function_name": "reverse_integer",
        "description": "Reverse the digits of an integer. Return 0 if the reversed value overflows the 32-bit signed integer range.",
        "test_cases": [
            {"args": [123], "expected": 321},
            {"args": [-123], "expected": -321},
            {"args": [120], "expected": 21}
        ],
        "expected_time": "O(log n)",
        "expected_space": "O(1)",
        "tags": ["math"]
    },
    {
        "id": 39,
        "title": "Palindrome Number",
        "topic": "Math",
        "difficulty": "Easy",
        "function_name": "is_palindrome_number",
        "description": "Determine whether an integer reads the same forward and backward.",
        "test_cases": [
            {"args": [121], "expected": True},
            {"args": [-121], "expected": False},
            {"args": [10], "expected": False}
        ],
        "expected_time": "O(log n)",
        "expected_space": "O(1)",
        "tags": ["math"]
    },
    {
        "id": 40,
        "title": "Power of Two",
        "topic": "Math",
        "difficulty": "Easy",
        "function_name": "is_power_of_two",
        "description": "Return True if n is a power of two, otherwise return False.",
        "test_cases": [
            {"args": [1], "expected": True},
            {"args": [16], "expected": True},
            {"args": [18], "expected": False},
            {"args": [0], "expected": False}
        ],
        "expected_time": "O(1)",
        "expected_space": "O(1)",
        "tags": ["math", "bit-manipulation"]
    },
]


# ============================================================
# ADD QUESTIONS TO DATASET
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
print(f"Dataset updated: {QUESTIONS_FILE}")