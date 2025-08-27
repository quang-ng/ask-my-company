import os
from langchain_google_genai import ChatGoogleGenerativeAI


class GeminiIntentNode():
    """LangGraph Node for Gemini LLM intent detection."""
    def run(self, question):
        api_key = os.getenv("GEMINI_API_KEY")
        prompt = (
            "Classify the user's question into one of the following intents: "
            "'rag' (for policy/benefit/knowledge questions), "
            "'api' (for personal/account-specific questions), "
            "'human_escalation' (if the question cannot be answered by the system).\n"
            f"Question: {question}\nIntent: "
        )
        try:
            llm = ChatGoogleGenerativeAI(api_key=api_key, model="gemini-pro")
            response = llm.invoke(prompt)
            intent = response.content.strip().lower()
            if intent not in {"rag", "api", "human_escalation"}:
                intent = "human_escalation"
            return intent
        except Exception:
            return "human_escalation"

intent_node = GeminiIntentNode()

def route_query(question, history, user_id):
    # Use LangGraph Gemini node for intent detection
    intent = intent_node.run(question)
    if intent == "rag":
        from handlers.rag_handler import handle_rag
        return handle_rag(question, history), "rag"
    elif intent == "api":
        from handlers.api_handler import handle_api
        return handle_api(question, user_id), "api"
    else:
        from handlers.human_handler import escalate_to_human
        return escalate_to_human(question, user_id), "human_escalation"
    