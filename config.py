# config.py

DEFAULT_SLEEP = 6

ANALYSIS_MODES = ["One by One", "All Together"]

LANGUAGE_OPTIONS = [
    "Any language", "GNU C11", "C++17 (GCC 7-32)", "C++20 (GCC 13-64)", "C++23 (GCC 14-64, msys2)",
    "C# 8", "C# 10", "C# 13", "Mono C#", "D", "F# 9", "Go", "Haskell", "Java 21", "Java 8", "Kotlin 1.7",
    "Kotlin 1.9", "OCaml", "Delphi", "FPC", "PascalABC.NET", "Perl", "PHP", "Python 2", "Python 3",
    "PyPy 2", "PyPy 3", "PyPy 3-64", "Ruby 3", "Rust 2021", "Scala", "JavaScript", "Node.js"
]

LANGUAGE_SYNTAX = {
    "Python 3": "python", "Python 2": "python", "PyPy 2": "python", "PyPy 3": "python", "PyPy 3-64": "python",
    "C++17 (GCC 7-32)": "cpp", "C++20 (GCC 13-64)": "cpp", "C++23 (GCC 14-64, msys2)": "cpp",
    "Java 8": "java", "Java 21": "java", "C# 8": "csharp", "C# 10": "csharp", "C# 13": "csharp",
    "Go": "go", "JavaScript": "javascript", "Node.js": "javascript", "PHP": "php", "Rust 2021": "rust"
}

DEFAULT_SINGLE_SOLUTION_PROMPT = """As an expert competitive programming coach, analyze the following solution for the given problem.

**Problem Statement:**
---
{problem_statement}
---

**Programming Language:** {language}

**Code Solution:**
---
{code}```
Please provide a clear and concise explanation covering the following points:
Code Explanation: A step-by-step breakdown of what the code does.
Intuition: The core logic or insight behind this approach. Why does it work?
Time Complexity: Analyze the Big O time complexity.
Space Complexity: Analyze the Big O space complexity.
Format your response using Markdown."""
DEFAULT_COMPARISON_PROMPT = """As an expert competitive programming coach, compare and contrast the following solutions for the given problem.
Problem Statement:
{problem_statement}
Code Solutions to Compare:
{solutions}
Please perform a comparative analysis:
Summarize Approaches: Briefly describe the different algorithms or strategies used in each solution.
Compare Efficiency: Discuss the time and space complexity of each approach. Are there significant differences?
Readability and Style: Comment on the coding style, clarity, and elegance of each solution.
Final Verdict: Declare which solution you believe is the "best" overall and provide a clear justification for your choice, considering a balance of efficiency, readability, and cleverness.
Format your response using Markdown."""
DEFAULT_ALL_TOGETHER_PROMPT = """As an expert competitive programming coach, analyze the following problem and its accompanying solutions in a single comprehensive report.
Problem Statement:
{problem_statement}
Code Solutions to Analyze:
{solutions}
For your report, please perform the following steps:
Individual Analysis: For each solution provided, create a separate section. In each section, explain the code, its core intuition, and its time and space complexity.
Comparative Analysis: After analyzing all solutions individually, provide a final summary. Compare the different approaches, discuss their efficiency and style, and declare which solution you believe is the "best" overall, justifying your choice.
Format the entire response using Markdown."""