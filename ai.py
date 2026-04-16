import g4f

def generate_qa(content):
    prompt = f"""
    Create 5 revision questions with answers from this:

    {content[:3000]}

    Format:
    Q1:
    A1:
    """

    response = g4f.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )

    return response
