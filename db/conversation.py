import logging
from pymongo import MongoClient
import os
from datetime import datetime

MONGO_URI = os.getenv("MONGO_URI", "mongodb://root:example@localhost:27017/")
DB_NAME = os.getenv("MONGO_DB_NAME", "askmycompany")
COLLECTION_NAME = "conversations"

client = MongoClient(MONGO_URI)
db = client[DB_NAME]
collection = db[COLLECTION_NAME]

def store_history(user_id, question, response, intent):
    logging.info(f"Storing history for user_id={user_id}")
    """
    Store a conversation turn in MongoDB.
    """
    doc = {
        "user_id": user_id,
        "question": question,
        "response": response,
        "intent": intent,
        "timestamp": datetime.now()
    }
    collection.insert_one(doc)

def get_history(user_id, max_messages=20):
    logging.info(f"Getting history for user_id={user_id} with max_messages={max_messages}")
    """
    Retrieve up to max_messages conversation history for a user from MongoDB.
    Returns a list of dicts sorted by timestamp descending (most recent first).
    """
    cursor = collection.find({"user_id": user_id}).sort("timestamp", -1).limit(max_messages)
    return list(cursor)
        