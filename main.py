from fastapi import FastAPI, UploadFile, File, HTTPException, Query
from db import create_db_connection, create_table
from utils import generate_embedding
import asyncio

app = FastAPI()

# Create database table on startup
@app.on_event("startup")
async def startup_event():
    await create_table()

# Document Ingestion API
@app.post("/upload/")
async def upload_document(file: UploadFile = File(...)):
    content = await file.read()
    text = content.decode("utf-8")

    # Generate Embedding
    embedding = generate_embedding(text)

    # Store in DB
    conn = await create_db_connection()
    await conn.execute(
        "INSERT INTO documents (filename, content, embedding) VALUES ($1, $2, $3)",
        file.filename, text, embedding
    )
    await conn.close()

    return {"message": "Document uploaded and stored successfully"}

# Q&A API
@app.post("/qa/")
async def ask_question(question: str):
    conn = await create_db_connection()

    # Retrieve embeddings and documents
    rows = await conn.fetch("SELECT content, embedding FROM documents")
    await conn.close()

    # Use Ollama to find relevant documents using embeddings
    relevant_docs = []
    for row in rows:
        response = ollama.chat("llama3", messages=[{"role": "user", "content": question}])
        relevant_docs.append({"content": row["content"], "response": response['message']})

    return {"answers": relevant_docs}

# Document Selection API
@app.post("/select_docs/")
async def select_documents(docs: list = Query(...)):
    conn = await create_db_connection()
    selected_docs = await conn.fetch("SELECT * FROM documents WHERE filename = ANY($1)", docs)
    await conn.close()
    return {"selected_documents": selected_docs}
