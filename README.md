# SaaS Product Documentation Support Bot 🤖

A Streamlit-based chatbot that uses LangChain and OpenAI to answer questions about your SaaS product documentation.

## Features

- PDF-based document Q&A with citations (file name and page)
- Chat history support
- Streamlit UI
- Support ticket creation mock (Jira integration)
- Uses LangChain + OpenAI under the hood

## Getting Started

1. Clone the repo and install requirements:

```bash
pip install -r requirements.txt
```

2. Set your OpenAI API key in a `.env` file:

```env
OPENAI_API_KEY=your_openai_key_here
```

3. Put your PDF docs in the `data/` folder.

4. Run the app:

```bash
streamlit run src/app.py
```

## Folder Structure

- `data/`: place your PDF documentation here
- `src/`: main code files
- `requirements.txt`: dependencies
- `README.md`: this file

## Mock Jira Ticket

When the bot can't find a confident answer, it will offer to create a support ticket with mock Jira integration (prints to console).

---

## Example result images
![Example 1](Screenshot%202025-07-30%20at%2000.20.56.png)
![Example 2](Screenshot%202025-07-30%20at%2000.26.48.png)
![Example 3](Screenshot%202025-07-30%20at%2000.28.11.png)
![Example 4](Screenshot%202025-07-30%20at%2000.30.53.png)
![Example 5](Screenshot%202025-07-30%20at%2000.34.54.png)
![Example 6](Screenshot%202025-07-30%20at%2000.34.57.png)