from pymongo import MongoClient
from config import MONGO_URI
import random

client = MongoClient(MONGO_URI)
db = client["revision_bot"]

users = db["users"]
questions = db["questions"]

def save_user(user_id):
    users.update_one(
        {"user_id": user_id},
        {"$set": {"user_id": user_id}},
        upsert=True
    )

def add_question(user_id, q):
    questions.insert_one({
        "user_id": user_id,
        "q": q
    })

def get_question(user_id):
    qs = list(questions.find({"user_id": user_id}))
    if not qs:
        return None
    return random.choice(qs)["q"]
