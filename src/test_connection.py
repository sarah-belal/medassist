import anthropic

client = anthropic.Anthropic()

response = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=256,
    messages=[
        {"role": "user", "content": "What is ibuprofen used for? Reply in one sentence."}
    ]
)

print(response.content[0].text)

