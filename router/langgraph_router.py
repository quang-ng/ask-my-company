import os
from handlers.rag_handler import generate_answer
from handlers.api_handler import handle_api
from handlers.human_handler import escalate_to_human
from langchain_google_genai import ChatGoogleGenerativeAI


class GeminiIntentNode:
    """LangGraph Node for Gemini LLM intent detection."""

    def run(self, question):
        api_key = os.getenv("GEMINI_API_KEY")
        prompt = (
            "Phân loại câu hỏi của người dùng vào một trong các ý định sau: "
            "'rag' (cho các câu hỏi về chính sách, phúc lợi, kiến thức), "
            "'api' (cho các câu hỏi cá nhân hoặc liên quan đến tài khoản), "
            "'human_escalation' (nếu hệ thống không thể trả lời câu hỏi này).\n"
            f"Câu hỏi: {question}\nÝ định: "
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
        return generate_answer(question, history), "rag"
    elif intent == "api":
        return handle_api(question, user_id), "api"
    else:
        return escalate_to_human(question, user_id), "human_escalation"
