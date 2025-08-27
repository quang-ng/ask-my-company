# handlers/human_handler.py
# Placeholder for human escalation handler

import logging

def escalate_to_human(question, user_id):
    import requests
    import os
    logging.info(f"Escalating query for user {user_id} with question: {question}")
    api_url = os.getenv("HUMAN_MGMT_API_URL", "https://human-mgmt.example.com/api/escalate")
    payload = {
        "question": question,
        "user_id": user_id
    }
    try:
        response = requests.post(api_url, json=payload, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        logging.error(f"Failed to escalate to human: {e}")
        return {"error": str(e)}
