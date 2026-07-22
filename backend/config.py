import os
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
DB_NAME = os.getenv("DB_NAME", "resume_analyzer_db")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")

class InMemoryCollection:
    """Fallback in-memory mock collection if MongoDB server is unavailable."""
    def __init__(self, name):
        self.name = name
        self.data = []

    def insert_one(self, document):
        doc = dict(document)
        if "_id" not in doc:
            doc["_id"] = str(len(self.data) + 1)
        self.data.append(doc)
        return type("InsertResult", (), {"inserted_id": doc["_id"]})()

    def find_one(self, query):
        for doc in self.data:
            match = True
            for k, v in query.items():
                if doc.get(k) != v:
                    match = False
                    break
            if match:
                return doc
        return None

    def find(self, query=None, limit=100):
        query = query or {}
        results = []
        for doc in self.data:
            match = True
            for k, v in query.items():
                if doc.get(k) != v:
                    match = False
                    break
            if match:
                results.append(doc)
        return results[:limit]

# Database Connection with Fallback
try:
    client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=2000)
    # Ping database to confirm live connection
    client.admin.command('ping')
    db = client[DB_NAME]
    users_collection = db["users"]
    resume_collection = db["resume_analysis"]
    print("Successfully connected to MongoDB.")
except Exception as e:
    print(f"MongoDB connection offline ({e}). Using in-memory store fallback for zero-downtime execution.")
    users_collection = InMemoryCollection("users")
    resume_collection = InMemoryCollection("resume_analysis")