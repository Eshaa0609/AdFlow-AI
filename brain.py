import os
from dotenv import load_dotenv
from google import genai  # The NEW stable import
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

# 1. Setup
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

# Initialize the NEW stable client
client = genai.Client(api_key=api_key)

# 2. Setup the "Librarian" (Vector DB)
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
vector_db = Chroma(persist_directory="./chroma_db", embedding_function=embeddings)

def ask_adflow(question):
    # Search for top 5 rules
    docs = vector_db.similarity_search(question, k=8)
    context = "\n".join([doc.page_content for doc in docs])
    
    # 3. Use the 2026 Standard Stable Model
    # gemini-2.5-flash is the current free-tier workhorse
    model_id = "gemini-2.5-flash" 
    
    prompt = f"""
    You are AdFlow AI, a Senior Marketing Strategy Consultant. 
    
    ### STYLE EXAMPLES:
    User: "What's the tone for ads?"
    Bad Answer: "The rule says be professional and use words like Success."
    Good Answer: "Based on our current strategic guidelines, we are maintaining an authoritative and sophisticated voice. Focus your messaging on 'Success' and 'Precision' to resonate with our HNI audience."

    ### YOUR TASK:
    Answer the User Query using the Brand Rules below. 
    - NEVER mention 'Rule 101' or say 'The rules say.'
    - Use a sophisticated, consultative tone.
    - If a calculation is needed (like budget %), do the math for the user.
    
    ### BRAND RULES:
    {context}
    
    ### USER QUERY:
    {question}
    
    ### CONSULTANT RESPONSE:
    """
    
    try:
        # The new SDK call
        response = client.models.generate_content(
            model=model_id,
            contents=prompt
        )
        return response.text
    except Exception as e:
        # If 2.5 is too new for your region, we try 2.0 as a backup
        try:
            response = client.models.generate_content(
                model="gemini-2.0-flash",
                contents=prompt
            )
            return response.text
        except:
            return f"❌ AI Brain Error: {str(e)}"

# --- TEST IT ---
if __name__ == "__main__":
    print("\n🚀 AdFlow AI Agent is ONLINE.")
    print("Type 'exit' or 'quit' to stop.")
    print("-" * 30)
    
    while True:
        user_input = input("\n👤 You: ")
        
        if user_input.lower() in ['exit', 'quit']:
            print("Goodbye! 👋")
            break
            
        print("\n🧠 AdFlow AI is thinking...")
        result = ask_adflow(user_input)
        print(f"🤖 AdFlow: {result}")
