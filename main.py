from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from router.langgraph_router import route_query
from db.conversation import store_history, get_history

app = FastAPI()

# Allow frontend to call the API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For development, allow all. Restrict in production.
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ChatRequest(BaseModel):
    message: str

class QueryRequest(BaseModel):
    user_id: str
    question: str

class ChatResponse(BaseModel):
    response: str
    intent: str


@app.post("/api/chat", response_model=ChatResponse)
async def chat_endpoint(request: QueryRequest):
    # Retrieve conversation history
    history = get_history(request.user_id)
    # Route query
    response, intent = route_query(request.question, history, request.user_id)
    # Store conversation turn
    store_history(request.user_id, request.question, response, intent)

    print({"response": response, "intent": intent})
    return ChatResponse(response=response, intent=intent)
