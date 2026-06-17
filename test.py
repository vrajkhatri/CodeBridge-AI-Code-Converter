from ollama import chat

response = chat(
    model='deepseek-coder',
    messages=[
        {
            'role': 'user',
            'content': 'Convert Python to PHP: print("Hello World")'
        }
    ]
)

print(response['message']['content'])