# 🧠 PageBrain: Turn any URL into an interactive Q&A bot.

PageBrain is an interactive Retrieval-Augmented Generation (RAG) application built with Streamlit and LangChain. It allows users to paste any URL, extract its content, and have an AI-powered conversation directly with the text of that webpage.

## ✨ Features

* **Dynamic URL Input:** Scrape and process any accessible webpage on the fly.
* **In-Memory Vector Store:** Uses ChromaDB entirely in-memory, making it fast and deployment-friendly (no filesystem errors!).
* **Open Source Embeddings:** Leverages HuggingFace embeddings for efficient text vectorization.
* **OpenRouter LLM Integration:** Powered by the `nvidia/nemotron-3-ultra-550b-a55b:free` model (can be swapped for any other model supported by OpenRouter).
* **Interactive UI:** Clean chat interface built natively with Streamlit.

## 🛠️ Tech Stack

* **Frontend/UI:** [Streamlit](https://streamlit.io/)
* **Orchestration:** [LangChain](https://www.langchain.com/)
* **Vector Database:** [ChromaDB](https://www.trychroma.com/) (In-memory)
* **Embeddings:** HuggingFace (`sentence-transformers`)
* **LLM Provider:** OpenRouter

## 🚀 Local Setup & Installation

### 1. Clone the repository
```bash
git clone https://github.com/yourusername/pagebrain.git
cd pagebrain
```

### 2. Create a virtual environment (Recommended)
```bash
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

### 3. Install dependencies
Ensure your `requirements.txt` includes all necessary packages, then run:
```bash
pip install -r requirements.txt
```

### 4. Set up environment variables
Create a `.env` file in the root directory of your project and add your OpenRouter API key:
```env
OPENROUTER_API_KEY=your_api_key_here
```

### 5. Run the application
```bash
streamlit run app.py
```

## ☁️ Deployment (Streamlit Community Cloud)

This app is perfectly suited for Streamlit Community Cloud since it doesn't require persistent local storage.

1. Push your code (including `app.py` and `requirements.txt`) to a GitHub repository. **Do not upload your `.env` file.**
2. Log into [Streamlit Community Cloud](https://share.streamlit.io/).
3. Click **Create app** and connect your repository.
4. Before clicking Deploy, go to **Advanced settings** and add your API key into the Secrets manager:
   ```toml
   OPENROUTER_API_KEY = "your_api_key_here"
   ```
5. Click **Deploy**!

## ⚠️ Notes

* Some websites block automated scrapers (like `UnstructuredURLLoader`). If the app fails to read a page, it may be due to bot-protection on that specific site.