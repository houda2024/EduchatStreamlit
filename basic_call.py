import os

from groq import Groq

client = Groq(
    api_key=os.environ.get("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"),
)

chat_completion = client.chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": "tell a joke ",
        }
    ],
    model="llama3-8b-8192",
)

print(chat_completion.choices[0].message.content)