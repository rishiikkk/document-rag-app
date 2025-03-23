import ollama

def generate_embedding(text):
    response = ollama.embeddings("llama3", text)
    return response["embedding"]
