MODEL = "llama-3.3-70b-versatile"


def make_client():
    from groq import Groq

    return Groq()


def ask_groq(question, client=None):
    if not question.strip():
        raise ValueError("Question must not be empty")
    if client is None:
        client = make_client()
    result = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": question}],
        max_tokens=1024,
    )
    return result.choices[0].message.content
