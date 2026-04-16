from pymongo import MongoClient
from config import MONGO_URI
from datetime import datetime, timedelta
import random

client = MongoClient(MONGO_URI)
db = client["revision_bot"]

users = db["users"]
questions = db["questions"]
memory = db["memory"]

def add_user(user_id):
    users.update_one({"user_id": user_id}, {"$set": {"user_id": user_id}}, upsert=True)

# ---------- MEMORY ----------
def save_memory(user_id, text):
    memory.update_one(
        {"user_id": user_id},
        {"$push": {"messages": text}},
        upsert=True
    )

def get_memory(user_id):
    data = memory.find_one({"user_id": user_id})
    if not data:
        return ""
    return "\n".join(data["messages"][-10:])

# ---------- QUESTIONS ----------
def add_questions(user_id, qa_list):
    for qa in qa_list:
        questions.insert_one({
            "user_id": user_id,
            "text": qa,
            "used_count": 0,
            "next_review": datetime.now()
        })

def get_revision(user_id):
    now = datetime.now()
    qs = list(questions.find({
        "user_id": user_id,
        "next_review": {"$lte": now}
    }))

    random.shuffle(qs)
    return qs[:5]

def update_question(q):
    level = q["used_count"]

    if level == 0:
        days = 1
    elif level == 1:
        days = 3
    elif level == 2:
        days = 7
    else:
        days = 15

    questions.update_one(
        {"_id": q["_id"]},
        {
            "$inc": {"used_count": 1},
            "$set": {"next_review": datetime.now() + timedelta(days=days)}
        }
    )
