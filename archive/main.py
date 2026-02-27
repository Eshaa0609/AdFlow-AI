from fastapi import FastAPI, HTTPException
import psycopg2
from psycopg2.extras import RealDictCursor
import os
from dotenv import load_dotenv

load_dotenv() # Load variables from .env

app = FastAPI(title="AdFlow AI - Advanced Analytics API")

def get_db_connection():
    # Priority 1: Use a full URL string (Standard for Neon/Supabase)
    db_url = os.getenv("DATABASE_URL")
    if db_url:
        return psycopg2.connect(db_url, cursor_factory=RealDictCursor)
    
    # Priority 2: Fallback to individual variables (for your local setup)
    return psycopg2.connect(
        host=os.getenv("DB_HOST", "localhost"),
        database=os.getenv("DB_NAME", "ad_tech_db"),
        user=os.getenv("DB_USER", "postgres"),
        password=os.getenv("DB_PASSWORD"),
        cursor_factory=RealDictCursor
    )

@app.get("/")
def home():
    return {"message": "AdFlow AI Analytics Engine Online"}

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

@app.get("/analytics/summary")
def get_summary():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT 
                COUNT(*) as total_clicks,
                COUNT(*) FILTER (WHERE is_bot = TRUE) as bot_clicks,
                (COUNT(*) FILTER (WHERE is_bot = TRUE)::float / NULLIF(COUNT(*), 0) * 100) as bot_percentage
            FROM click_logs
        """)
        stats = cursor.fetchone()
        cursor.close()
        conn.close()
        return stats
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database connection failed: {str(e)}")