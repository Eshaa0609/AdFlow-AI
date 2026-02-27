# agent.py
import os
from dotenv import load_dotenv
from google import genai
from data_provider import get_campaign_metrics # Using your new dynamic provider
from brain import ask_adflow
from audit_logger import log_event

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def adflow_agent(user_query):
    # 1. Audit Trail: Log the incoming query
    log_event("USER_QUERY", user_query)
    
    # 2. Reasoning: Decision Logic
    log_event("AGENT_THOUGHT", "Analyzing query for SQL tool necessity vs RAG fallback")
    
    # Dynamic Data Source Selection (Set in Streamlit Secrets!)
    data_source = os.getenv("DATA_SOURCE", "sql") 
    
    if "mumbai" in user_query.lower() or "bot rate" in user_query.lower():
        # SQL Path via Data Provider
        log_event("AGENT_ACTION", f"Triggering {data_source} tool for Mumbai health check")
        
        stats = get_campaign_metrics("Mumbai", source_type=data_source)
        log_event("TOOL_OUTPUT", f"Live data fetched: {stats}")
        
        # RAG Path
        log_event("AGENT_ACTION", "Consulting RAG brain for policy compliance")
        rules = ask_adflow("What is the mandatory pause threshold for bot rates?")
        log_event("RAG_OUTPUT", "Policy thresholds retrieved")
        
        # 3. Final Synthesis (Restoring your specific prompt instructions)
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
        
        log_event("AGENT_THOUGHT", "Synthesizing response with live data and policy")
        
        response = client.models.generate_content(
            model="gemini-2.5-flash", 
            contents=prompt
        )
        
        # 4. Audit Trail: Log the final verdict
        log_event("FINAL_RESPONSE", response.text)
        return response.text
    
    else:
        # Fallback RAG Path
        log_event("AGENT_ACTION", "No SQL trigger detected; using standard RAG")
        fallback_response = ask_adflow(user_query)
        log_event("FINAL_RESPONSE", fallback_response)
        return fallback_response

if __name__ == "__main__":
    print("\n🚀 Agent is ready with Audit Logging enabled.")
    query = "What is the current status of the Mumbai campaign?"
    print(f"\n🤖 Agent Verdict:\n{adflow_agent(query)}")