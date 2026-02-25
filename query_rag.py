import os
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

# 1. Setup the Brain (Must match rag_engine.py)
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
vector_db = Chroma(persist_directory="./chroma_db", embedding_function=embeddings)

# 2. Ask a Question
query = "Tell me about the target audience and customers" # Change this to test!

# 3. Search the Database
docs = vector_db.similarity_search(query, k=2)

# 4. Show the Results
print("\n🔍 AI is searching your rules...")
print("-" * 30)
if docs:
    for i, doc in enumerate(docs):
        print(f"Result {i+1}:\n{doc.page_content}\n")
else:
    print("❌ No matching rules found.")