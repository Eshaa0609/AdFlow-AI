import os
from langchain_community.document_loaders import TextLoader
from langchain_chroma import Chroma 
from langchain_huggingface import HuggingFaceEmbeddings
# This is the smarter splitter we need
from langchain_text_splitters import RecursiveCharacterTextSplitter

# 1. Load the Knowledge
if not os.path.exists("./data/rules.txt"):
    print("❌ Error: data/rules.txt not found! Create the file first.")
else:
    # We clear the old database so the new chunking logic takes effect
    if os.path.exists("./chroma_db"):
        import shutil
        shutil.rmtree("./chroma_db")
        
    loader = TextLoader("./data/rules.txt")
    documents = loader.load()

    # 2. Split text into chunks
    # Now using Recursive splitter to respect your bullet points
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=300,           # Optimized for single rules
        chunk_overlap=50,         # Keeps context between slices
        separators=["\n- ", "\n", " ", ""] # Priorities: Bullet points, then lines
    )
    docs = text_splitter.split_documents(documents)

    # 3. Create Embeddings (Local & Free)
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

    # 4. Store in Vector Database (ChromaDB)
    vectorstore = Chroma.from_documents(
        documents=docs, 
        embedding=embeddings,
        persist_directory="./chroma_db"
    )

    print(f"✅ Knowledge Base Created with {len(docs)} precise chunks!")