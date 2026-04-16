import g4f

def generate_qa(content):
    try:
        prompt = f"""
        You are a teacher.

        Create 5 revision questions with answers from the content below.

        Keep it simple and exam-focused.

        Content:
        {content[:3000]}

        Format:
        Q1:
        A1:
        """

        response = g4f.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            timeout=30
        )

        return response

    except Exception as e:
        print("AI ERROR:", e)
        return None
