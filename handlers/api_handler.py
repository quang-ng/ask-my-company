import fastapi
import logging

logging.basicConfig(level=logging.INFO)

# handlers/api_handler.py
# Placeholder for API handler for personal data queries

import requests

from llama_index import SimpleLLM

def llm_answer_with_context(question: str, user_id: str) -> str:
    """
    Feeds question and answer into context and calls LLM to generate a response.
    """
    answer = handle_api(user_id)

    # Prepare context
    context = f"Question: {question}\nAnswer: {answer}"
    # Call LLM (using llama-index SimpleLLM for demonstration)
    llm = SimpleLLM()
    response = llm.complete(context)
    return response

def handle_api(user_id: str) -> dict:
    """
    Calls an external API to request user information by user_id.
    Returns a dictionary with user information or an error message.
    """
    # Example: Call an external API to get user info
    api_url = f"https://api.example.com/users/{user_id}"
    try:
        response = requests.get(api_url)
        response.raise_for_status()
        user_data = response.json()
        # Map the response to expected fields
        mapped_data = {
            "user_id": user_data.get("id", user_id),
            "name": user_data.get("name", ""),
            "email": user_data.get("email", ""),
            "role": user_data.get("role", ""),
            "status": user_data.get("status", "")
        }
        return mapped_data
    except requests.RequestException as e:
        logging.error(f"API request failed: {e}")
        return {"error": "Failed to fetch user data"}

