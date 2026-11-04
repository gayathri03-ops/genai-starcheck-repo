import httpx

request = {
    "messages": [
        {
            "role": "user",
            "content": "Explain what a vector database is in simple terms.",
        }
    ],
    "model": "gemini-3.5-flash",
}

with httpx.stream(
    "POST",
    "http://localhost:8000/chat",
    json=request,
    timeout=None,
) as response:
    response.raise_for_status()
    for line in response.iter_lines():
        if line:
            print(line)
