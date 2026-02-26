import os
from dotenv import load_dotenv
from google import genai
from tools_sql import get_bot_stats_by_region
from brain import ask_adflow # We're reusing your RAG brain!

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def adflow_agent(user_query):
    print(f"🕵️ Agent Reasoning: Analyzing query -> '{user_query}'")
    
    # 1. Decision Logic: Does the user want LIVE data?
    if "mumbai" in user_query.lower() or "bot rate" in user_query.lower():
        print("🔍 Agent Action: Fetching live SQL data...")
        stats = get_bot_stats_by_region("Mumbai")
        
        # 2. Reasoning: Get the rules to compare with the data
        print("📚 Agent Action: Consulting RAG for thresholds...")
        rules = ask_adflow("What is the mandatory pause threshold for bot rates?")
        
        # 3. Final Synthesis (The 'Strategist' part)
        prompt = f"""
        You are AdFlow, a high-level Marketing Strategist. 
        
        CONTEXT:
        Live Data: {stats}
        Brand Policy: {rules}
        
        TONE & STYLE:
        - Be direct and calm. 
        - Avoid all labels like "EXECUTIVE RESPONSE" or "Recommendation:".
        - Use simple, professional language.
        - If the bot rate is over 20%, lead with the need to pause.
        
        QUESTION: {user_query}
        """
        
        # Switch to the stable 2026 model path
        response = client.models.generate_content(
            model="gemini-2.5-flash", 
            contents=prompt
        )
        return response.text
    
    else:
        # Fallback to standard RAG for general questions
        return ask_adflow(user_query)

if __name__ == "__main__":
    print("\n🚀 Agent is ready.")
    query = "What is the current status of the Mumbai campaign? Should we keep it running?"
    print(f"\n🤖 Agent Verdict:\n{adflow_agent(query)}")