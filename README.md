# 🌌 Codeforces AI Analyst

An advanced desktop tool with a sophisticated web interface, designed to fetch, analyze, and compare competitive programming solutions from Codeforces using the power of the Gemini API.

This application provides a seamless, beautiful, and robust environment for deep-diving into algorithmic strategies and code quality.

---

## ✨ Features

*   **Modular & Professional Architecture:** The application is built with a clean, separated architecture (`ui`, `scraping`, `ai`, `config`) for maximum maintainability and scalability.
*   **Dynamic AI Analysis:** Fetches top solutions for any Codeforces problem and uses the Gemini API to provide in-depth analysis on intuition, complexity, and code structure.
*   **Dual Analysis Modes:**
    *   **One by One:** An interactive dashboard to view individual solution analyses and compare them.
    *   **All Together:** A comprehensive mode to generate a single, unified report on all fetched solutions.
*   **Intelligent & Dynamic UI:** A custom-built, production-quality UI with a dynamic "deep space" theme, animated elements, and a flawless user experience, including an auto-collapsing sidebar for an unobstructed view.
*   **Interactive Chat:** Engage in a contextual conversation with the AI about any specific solution or the final comparative analysis.
*   **Tunable AI Prompts:** The sidebar contains an advanced section allowing you to modify the exact prompts sent to the AI, giving you complete control over the style and focus of the analysis.

---

## ⚠️ Critical Prerequisite: Desktop Environment

This application uses the `pyautogui` library to perform its web scraping, which means it **physically controls the mouse and keyboard** of the machine it is running on.

> **This tool cannot be deployed on standard headless cloud platforms (like Streamlit Community Cloud, Heroku, Vercel, etc.).**
>
> It **must** be run on a machine with a graphical user interface (GUI) and a desktop environment (e.g., Windows, macOS, or a Linux distribution with a desktop).

---

## 🚀 Setup and Installation

Follow these steps to run the application on your local machine.

1.  **Clone the Repository:**
    ```bash
    git clone https://github.com/YOUR_USERNAME/YOUR_REPOSITORY_NAME.git
    cd YOUR_REPOSITORY_NAME
    ```

2.  **Create and Activate a Virtual Environment:**
    ```bash
    # For Windows
    python -m venv .venv
    .venv\Scripts\activate

    # For macOS/Linux
    python3 -m venv .venv
    source .venv/bin/activate
    ```

3.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Create Your Environment File:**
    *   In the root of the project folder, create a file named `.env`.
    *   Add your Gemini API key to this file. The file should contain only this line:
        ```
        GEMINI_API_KEY="AIzaSy...your...key"
        ```

5.  **Run the Application:**
    ```bash
    streamlit run main_app.py
    ```
    The application will open in your web browser. Otherwise you may also use the launch_streamlit.vbs, to use the one click launch.

---

## 🏛️ Project Architecture

The application is designed with a clean, separated architecture for professional-grade maintainability:

*   `main_app.py`: The main entry point that orchestrates all modules and manages the application state.
*   `ui_components.py`: Renders all UI elements, including the sidebar, results area, and all custom CSS.
*   `scraping_logic.py`: Contains all the `pyautogui` logic for browser automation and web scraping.
*   `gemini_integration.py`: Handles all communication with the Google Gemini API, including analysis and chat.
*   `config.py`: Stores all application constants, default settings, and AI prompt templates.
