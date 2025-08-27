import os
from llama_index.llms.gemini import Gemini
from llama_index.embeddings.gemini import GeminiEmbedding
from llama_index.core import VectorStoreIndex, StorageContext
from llama_index.vector_stores.mongodb import MongoDBAtlasVectorSearch

# MongoDB and LlamaIndex setup
mongo_uri = 'mongodb://localhost:27017/'
db_name = 'rag_db'
collection_name = 'documents'

vector_store = MongoDBAtlasVectorSearch(
    mongo_uri=mongo_uri,
    db_name=db_name,
    collection_name=collection_name
)
storage_context = StorageContext.from_defaults(vector_store=vector_store)

# Load models
gemini_api_key = os.getenv('GEMINI_API_KEY')
llm = Gemini(model="gemini-pro-vision-lite", api_key=gemini_api_key)
embed_model = GeminiEmbedding()
index = VectorStoreIndex.from_vector_store(
    storage_context=storage_context,
    embed_model=embed_model
)

def retrieve_relevant_docs(query: str, top_k: int = 3) -> list:
    """
    Semantically search for relevant documents using LlamaIndex.
    Returns a list of dicts with content, summary, and filename.
    """
    results = index.query(query, similarity_top_k=top_k)
    return [
        {
            'content': result.node.get_content(),
            'summary': result.node.metadata.get('summary', ''),
            'filename': result.node.metadata.get('filename', '')
        }
        for result in results
    ]

def generate_answer(query: str, conversation_history: str = None, top_k: int = 3) -> str:
    """
    Generate an answer to the query using relevant company documents and conversation history.
    """
    relevant_docs = retrieve_relevant_docs(query, top_k=top_k)
    summaries = [doc['summary'] for doc in relevant_docs if doc['summary']]
    context = "\n\n".join(summaries)
    if conversation_history:
        context = f"Lịch sử hội thoại:\n{conversation_history}\n\n{context}" if context else f"Lịch sử hội thoại:\n{conversation_history}"
    prompt = (
        "Trả lời câu hỏi sau dựa trên tài liệu công ty và lịch sử hội thoại nếu có:\n"
        f"Câu hỏi: {query}\n\n{context}"
    )
    return llm.complete(prompt)


