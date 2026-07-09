from dotenv import load_dotenv

from openai import OpenAI

load_dotenv() 

client = OpenAI()

# Read file contents
with open("notes.txt", "r") as f:
    document = f.read()

# Get question from user
question = input("Ask a question: ")

# Send document + question to GPT

response = client.chat.completions.create(
    model="gpt-4o",    
    messages=[
        {"role": "user", "content": f"Document:\n{document}\n\nQuestion:\n{question}\n\nAnswer based only on the document."}
    ]    



)

print("\nAnswer:")

print(response.choices[0].message.content)
