import random

questions_db = []

def add_questions(q):
    if q and isinstance(q, str):
        questions_db.append(q)

def get_question():
    if not questions_db:
        return None
    
    return random.choice(questions_db)
