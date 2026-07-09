from dotenv import load_dotenv
from openai import OpenAI
import pdfplumber
import numpy as np

load_dotenv()

client = OpenAI()

PATH="/Users/arulfrancis/Downloads/LA_v_Callas_supreme_court.pdf"
# downloaded from https://www.supremecourt.gov/opinions/25pdf/24-109_21o3.pdf
def load_pdf(path):
    pages = []
    with pdfplumber.open(path) as pdf:
        for page in pdf.pages:
            pages.append(page.extract_text() or "")
    return "\n".join(pages) 

document = load_pdf(PATH)

# 1. step 1 : chunking 

def chunk_text(text, chunk_size=500):
    """Split text into chunks of `chunk_size` characters."""
    chunks = []
    for i in range(0, len(text), chunk_size):
        chunk = text[i:i+chunk_size]
        chunks.append(chunk)
    return chunks

chunks = chunk_text(document)
print(f"Document split into {len(chunks)} chunks")
print("First chunk preview:", chunks[0][:100])

# step 2 : embedding

def get_embedding(text):
    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=text
    )
    return response.data[0].embedding

# Embed every chunk
chunk_embeddings = [get_embedding(chunk) for chunk in chunks]
print(f"Got {len(chunk_embeddings)} embeddings")
print(f"Each embedding has {len(chunk_embeddings[0])} numbers")

# 3. Step 3 : similarity search 

import numpy as np

def cosine_similarity(a, b):
    a = np.array(a)
    b = np.array(b)
    dot_product = np.dot(a, b)
    norm_a = np.linalg.norm(a)
    norm_b = np.linalg.norm(b)
    return dot_product / (norm_a * norm_b)

def find_best_chunk(question, chunks, chunk_embeddings):
    question_embedding = get_embedding(question)
    similarities = [cosine_similarity(question_embedding, emb) for emb in chunk_embeddings]
    best_index = np.argmax(similarities)   # index of the highest similarity score
    return chunks[best_index]

# step 4 : generation

def answer_question(question, chunks, chunk_embeddings):
    best_chunk = find_best_chunk(question, chunks, chunk_embeddings)

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "user", "content": f"Context:\n{best_chunk}\n\nQuestion:\n{question}\n\nAnswer based only on the context."}
        ]
    )
    return response.choices[0].message.content

question = input("Ask a question: ")
print("\nAnswer:")
print(answer_question(question, chunks, chunk_embeddings))