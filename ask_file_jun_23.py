from dotenv import load_dotenv

from openai import OpenAI

load_dotenv() 

client = OpenAI()

# Read file contents
with open("notes.txt", "r") as f:
    document = f.read()


# Initialize using a system message

messages = [
    {
        "role": "system",
        "content": f"Answer questions based only on this document:\n\n{document}"
    }
]


# Start the continuous loop

while True:
    # 1. get the question from the user
    question = input("Ask a question or type quit: ")

    # 2. check if user wants to exit from the loop
    if question.lower() in ["exit", "quit"]:
        print("Goodbye!")
        break

    # 3. skip empty inputs
    if not question.strip():
        continue

    # 4. append this user question to the history
    messages.append(
        {
            "role": "user",
            "content": question
        }
    )

    # 5. send the entire hist and get resp
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=messages
    )  

    #6. save the assistant's response
    answer = response.choices[0].message.content

    print("\nAnswer:")
    print(answer)

    messages.append(
        {
            "role": "assistant",
            "content": answer
        }
    ) 


