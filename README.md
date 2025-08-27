# FastAPI LangGraph RAG/API Router Project

## Overview
This project implements a FastAPI backend with the following flow:

1. **User submits question** via API.
2. **FastAPI** endpoint receives it and sends the query to **LangGraph Router**.
3. **LangGraph Router** decides the intent:
    - **RAG Handler** (policy/benefit queries) → Uses **LlamaIndex** for retrieval from **MongoDB vector store**.
    - **API Handler** (personal data queries) → Calls internal API directly.
    - **Human Escalation** → Sends ticket/alert to support staff.
4. **Conversation history** is stored/retrieved from **MongoDB** for context in each turn.

## Structure
- `main.py`: FastAPI entrypoint
- `router/`: LangGraph router logic
- `handlers/`: RAG, API, and Human Escalation handlers
- `db/`: MongoDB integration and conversation history

## Setup
- Python 3.10+
- FastAPI
- LlamaIndex
- MongoDB (vector store)
- [Optional] LangGraph, Pydantic, Uvicorn

## Usage
1. Install dependencies: `pip install -r requirements.txt`
2. Run server: `uvicorn main:app --reload`

---
This is a scaffold. Replace placeholders and add implementation as needed.
