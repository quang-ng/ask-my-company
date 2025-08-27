import os
import pymongo
import numpy as np
from llama_index.llms.gemini import Gemini
from llama_index.embeddings.gemini import GeminiEmbedding

# MongoDB setup
client = pymongo.MongoClient('mongodb://localhost:27017/')
db = client['rag_db']
collection = db['documents']

# Load models
gemini_api_key = os.getenv('GEMINI_API_KEY')
llm = Gemini(model="gemini-pro-vision-lite", api_key=gemini_api_key)
embed_model = GeminiEmbedding()

def retrieve_relevant_docs(query, top_k=3):
    # Embed the user query
    query_embedding = embed_model.embed(query)
    # Fetch all document embeddings from MongoDB
    docs = list(collection.find({}, {'embedding': 1, 'content': 1, 'summary': 1, 'filename': 1}))
    # Compute similarity (cosine) between query and each doc
    def cosine_similarity(a, b):
        a = np.array(a)
        b = np.array(b)
        return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))
    scored_docs = []
    for doc in docs:
        score = cosine_similarity(query_embedding, doc['embedding'])
        scored_docs.append((score, doc))
    # Sort by score and select top_k
    scored_docs.sort(reverse=True, key=lambda x: x[0])
    top_docs = [doc for _, doc in scored_docs[:top_k]]
    return top_docs

def generate_answer(query, conversation_history=None, top_k=3):
    # Retrieve relevant docs
    relevant_docs = retrieve_relevant_docs(query, top_k=top_k)
    # Prepare context for LLM
    context = "\n\n".join([doc['summary'] for doc in relevant_docs])
    if conversation_history:
        context = f"Lịch sử hội thoại:\n{conversation_history}\n\n{context}"
    prompt = f"Trả lời câu hỏi sau dựa trên tài liệu công ty và lịch sử hội thoại nếu có:\nCâu hỏi: {query}\n\n{context}"
    # Generate answer
    answer = llm.complete(prompt)
    return answer
# handlers/rag_handler.py
# Placeholder for RAG handler using LlamaIndex and MongoDB

import logging
from llama_index.core import SimpleDirectoryReader
from llama_index.vector_stores.mongodb import MongoDBAtlasVectorSearch
from pymongo import MongoClient

MONGO_URI = "mongodb://localhost:27017"
DB_NAME = "rag_db"
COLLECTION_NAME = "embeddings"

def handle_rag(question, history_conversation):
    logging.info(f"Handling RAG request: {question}")
