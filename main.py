from fastapi import FastAPI
import psycopg2
from psycopg2.extras import RealDictCursor # This makes the data look like a clean dictionary

app = FastAPI(title="AdFlow AI API")

# Database Connection Helper
def get_db_connection():
    return psycopg2.connect(
        host="localhost",
        database="ad_tech_db",
        user="postgres",
        password="Eshaa@123", # Your Vault Password
        cursor_factory=RealDictCursor # Crucial: This formats the SQL rows into JSON automatically!
    )

@app.get("/")
def home():
    return {"message": "AdFlow AI API is Online"}

# NEW: The "Eyes" for your Agent
@app.get("/recent-clicks")
def get_recent_clicks():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Query the top 10 most recent logs
    cursor.execute("SELECT * FROM click_logs ORDER BY log_id DESC LIMIT 10")
    logs = cursor.fetchall()
    
    cursor.close()
    conn.close()
    return {"data": logs}

# NEW: Search for a specific brand's clicks
@app.get("/search-brand")
def search_brand(brand_name: str):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Using 'ILIKE' for case-insensitive search and % for partial matches
    query = "SELECT * FROM click_logs WHERE campaign_name ILIKE %s LIMIT 20"
    cursor.execute(query, (f"%{brand_name}%",))
    results = cursor.fetchall()
    
    cursor.close()
    conn.close()
    return {"brand": brand_name, "count": len(results), "data": results}