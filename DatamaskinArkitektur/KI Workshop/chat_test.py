from ollama import chat

tall = input("Skriv inn et tall: ")

prompt = f"Hva er {tall} + 637284?"

#prompt = "Heisan, hvordan har du det i dag?"

message = [
    {
        "role": "user",
        "content": prompt,
           },
]

response = chat(model="qwen3:8b", messages=message)

print(response.message.content)