from pymongo import MongoClient
from config import MONGO_URI
import random

client = MongoClient(MONGO_URI)
db = client["revision_bot"]

users = db["users"]
questions = db["questions"]

def add_user(user_id):
    users.update_one({"user_id": user_id}, {"$set": {"user_id": user_id}}, upsert=True)

def add_question(user_id, q):
    questions.insert_one({
        "user_id": user_id,
        "q": q,
        "used": False
    })

def get_questions(user_id):
    new_q = list(questions.find({"user_id": user_id, "used": False}))
    old_q = list(questions.find({"user_id": user_id, "used": True}))

    result = []

    if new_q:
        result += random.sample(new_q, min(3, len(new_q)))
    if old_q:
        result += random.sample(old_q, min(2, len(old_q)))

    return result
