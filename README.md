# 🤖 Ollama Streamlit Chatbot

A simple but powerful Streamlit chatbot interface for running local LLMs with Ollama.

![Demo GIF of the chatbot in action] (You can record a short GIF of your screen to show it off!)

## ✨ Features

* **Real-time Streaming:** See the model's response as it's being generated.
* **Model Selection:** Easily switch between any of your installed Ollama models.
* **Conversation History:** Each model has its own persistent chat history. (However, there's no feature to save history, so it will be deleted when the program is terminated)
* **"Thought Process" Viewer:** For models that use `<think>` tags (e.g., qwen3:4b-q4_K_M), their reasoning is neatly hidden in a collapsible expander.

## ⚙️ Prerequisites

Before you begin, ensure you have the following installed:
* [Python 3.8+](https://www.python.org/downloads/) - I used python 3.11.2
* [Ollama](https://ollama.com/) and at least one model pulled (e.g., `ollama run llama3`). I have used `[llama3:latest](https://ollama.com/library/llama3.2:latest)` and `[qwen3:4b-q4_K_M](https://ollama.com/library/qwen3:4b)`

## 🚀 Installation & Setup

1.  **Clone the repository:**
    ```bash
    git clone [your-github-repo-url]
    cd [your-project-folder]
    ```

2.  **Create and activate a virtual environment (recommended):**
    ```bash
    python -m venv .venv
    # On Windows
    .venv\Scripts\activate
    # On macOS/Linux
    source .venv/bin/activate
    ```

3.  **Install the required packages:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Ensure that Ollama is running in the background, and at least one model is pulled.**

5.  **Run the Streamlit app:**
    ```bash
    streamlit run app.py
    ```
