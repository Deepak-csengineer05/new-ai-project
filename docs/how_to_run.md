# How to Run SkillGenome

## Prerequisites
- **Python 3.8+** installed on your system.
- A **Google Gemini API Key**.

### How to get a Gemini API Key:
1.  Go to [Google AI Studio](https://aistudio.google.com/).
2.  Sign in with your Google account.
3.  Click on the **"Get API key"** button (usually on the top left).
4.  Click **"Create API key"** (you can create it in a new project).
5.  Copy the generated key string (it starts with `AIza...`).

## Installation

1.  **Clone or Download** the project repository.
2.  **Navigate** to the project directory in your terminal:
    ```bash
    cd "e:\App development\new ai project"
    ```
3.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

## Running the Application

1.  Run the Streamlit app:
    ```bash
    streamlit run app.py
    ```
2.  A browser window should automatically open at `http://localhost:8501`.

## Usage Guide

1.  **Enter API Key**: In the sidebar, paste your Google Gemini API Key.
2.  **Generate Graph**: Enter a target role (e.g., "Machine Learning Engineer") and click "Generate Graph".
3.  **Explore**:
    - The graph visualization will appear in the main area.
    - **Click on a node** to see details in the sidebar (description, resources).
4.  **Take Quiz**:
    - Select a node.
    - Click "Take Quiz" in the sidebar.
    - Answer the questions and submit.
    - If you pass, the node turns **Green** (Completed).
    - If you fail, you'll get feedback on what to review.

## Troubleshooting
- **Graph not showing?** Ensure `streamlit-agraph` is installed correctly.
- **API Errors?** Check your internet connection and API key validity.
