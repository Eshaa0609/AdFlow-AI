from fastapi import FastAPI, HTTPException
import psycopg2
from psycopg2.extras import RealDictCursor

app = FastAPI(title="AdFlow AI - Advanced Analytics API")

# DB Connection Helper
def get_db_connection():
    return psycopg2.connect(
        host="localhost",
        database="ad_tech_db",
        user="postgres",
        password="Eshaa@123",
        cursor_factory=RealDictCursor
    )

@app.get("/")
def home():
    return {"message": "AdFlow AI Analytics Engine Online"}

# 1. Advanced Search (Filter by Brand + Region + Bot Status)
@app.get("/filter-clicks")
def filter_clicks(brand: str = None, region: str = None, is_bot: bool = None):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    query = "SELECT * FROM click_logs WHERE 1=1"
    params = []
    
    if brand:
        query += " AND campaign_name ILIKE %s"
        params.append(f"%{brand}%")
    if region:
        # Changed '=' to 'ILIKE' to ignore capital letters
        query += " AND user_region ILIKE %s"
        params.append(f"{region}")
    if is_bot is not None:
        query += " AND is_bot = %s"
        params.append(is_bot)
    
    query += " LIMIT 50"
    cursor.execute(query, tuple(params))
    results = cursor.fetchall()
    
    cursor.close()
    conn.close()
    return {"count": len(results), "results": results}

# 2. Summary Stats (The "Brain" for the Agent)
@app.get("/analytics/summary")
def get_summary():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT 
                COUNT(*) as total_clicks,
                COUNT(*) FILTER (WHERE is_bot = TRUE) as bot_clicks,
                (COUNT(*) FILTER (WHERE is_bot = TRUE)::float / COUNT(*) * 100) as bot_percentage
            FROM click_logs
        """)
        stats = cursor.fetchone()
        
        cursor.close()
        conn.close()
        return stats
    except Exception as e:
        # This sends a clean 500 error instead of crashing the server
        raise HTTPException(status_code=500, detail=f"Database connection failed: {str(e)}")