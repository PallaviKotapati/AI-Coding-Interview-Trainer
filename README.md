# AI Coding Interview Trainer

An intelligent, interactive coding interview preparation platform designed to help students and software engineering aspirants practice Data Structures and Algorithms (DSA) through personalized AI-driven guidance, automated code evaluation, and asymptotic complexity analysis.

---

## Project Description

The AI Coding Interview Trainer simulates realistic technical interview rounds. Instead of passive problem solving, the system serves as an interactive mock interviewer that provides progressive hints, evaluates Python solution submissions against comprehensive test cases, analyzes time and space complexity, and offers actionable feedback based on canonical DSA patterns.

---

## Planned Technologies

- **Programming Language:** Python 3.12
- **Web User Interface:** Gradio
- **Local Large Language Model:** Mistral 7B (served locally via Ollama)
- **Vector Database:** ChromaDB (embedded, local persistent storage)
- **Embeddings:** Sentence-Transformers (`all-MiniLM-L6-v2`)
- **Code Evaluation & Security:** Python `subprocess` sandbox with AST (`ast` module) code inspection
- **Dataset:** Curated DSA Sheet based on Striver's A2Z DSA Course

---

## Planned Features

1. **Curated DSA Question Bank:** Canonical problems categorized by topic (Arrays, Two Pointers, Strings, Linked Lists, Trees, Graphs, DP).
2. **AI Question Generation:** Synthesizes new problem variations grounded in curated patterns with automated reference-solution pre-flight validation.
3. **Interactive Code Editor & Test Runner:** Monaco-style editor with real-time test execution against public and hidden test cases.
4. **Progressive 3-Tier Hints:** Conceptual nudges $\rightarrow$ Algorithmic steps $\rightarrow$ Code skeletons without spoiling the solution.
5. **Hybrid Complexity Analysis:** Combines static AST parsing with LLM reasoning to derive precise Big-O time and space complexity.
6. **Personalized Mock Interview Feedback:** Multi-factor critique covering correctness, asymptotic efficiency, code style, and interview hiring recommendations.
7. **Offline RAG Architecture:** Fully private, zero API-cost retrieval-augmented generation running entirely on local hardware.

---

## Current Development Status

## Current Development Status

- **Phase 1 (Completed):** Development environment setup using Python 3.12 virtual environment, dependency management, and project base structure.
- **Phase 2 (Completed):** DSA dataset compilation and RAG retrieval setup using ChromaDB and sentence-transformer embeddings.
- **Phase 3 (Completed):** Code evaluation sandbox and AST-based time and space complexity analyzer.
- **Phase 4 (Completed):** Local LLM integration with Mistral via Ollama for AI-generated interview feedback.
- **Phase 5 (Completed):** Gradio web interface assembly and end-to-end testing of question generation, code evaluation, complexity analysis, and RAG-based feedback.
