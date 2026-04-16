import random

questions_db = []

def add_questions(q):
    questions_db.append(q)

def get_question():
    if not questions_db:
        return "No questions yet"
    return random.choice(questions_db)
