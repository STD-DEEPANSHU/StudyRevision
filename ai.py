import g4f

# -------- Q&A GENERATOR --------
def generate_qa(content):
    prompt = f"""
    You are a medical teacher.

    Generate 5 important questions.

    Rules:
    - English + Hindi answer
    - Add example
    - Exam focused

    Content:
    {content}

    Format:
    Q:
    EN:
    HI:
    EX:
    """

    try:
        res = g4f.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}]
        )
        return parse_qa(res)
    except:
        return []

def parse_qa(text):
    blocks = text.split("Q:")
    result = []

    for b in blocks:
        if "EN:" in b:
            result.append("Q:" + b.strip())

    return result


# -------- CHATBOT --------
def ask_ai(memory, question):
    prompt = f"""
    You are a medical AI tutor.

    User past context:
    {memory}

    Answer question below in:
    - English
    - Hindi
    - Example

    Question:
    {question}
    """

    try:
        return g4f.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}]
        )
    except:
        return "⚠️ AI error"
