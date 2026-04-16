import g4f

def generate_qa(content):
    prompt = f"""
    Generate SSC/UPSC level questions and answers.

    Focus:
    - Important facts
    - Concept clarity
    - Exam pattern

    Content:
    {content[:3000]}

    Format:
    Q:
    A:
    """

    try:
        return g4f.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            timeout=30
        )
    except:
        return None
