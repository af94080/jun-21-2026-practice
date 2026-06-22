from dotenv import load_dotenv

from openai import OpenAI

client = OpenAI()

# Read file contents
with open("notes.txt", "r") as f:
    document = f.read()

# Get question from user
question = input("Ask a question: ")

# Send document + question to GPT
response = client.responses.create(
    model="gpt-4.1",
    input=f"""
Document:

{document}

Question:
{question}

Answer based only on the document.
"""
)

print("\nAnswer:")
print(response.output_text)
