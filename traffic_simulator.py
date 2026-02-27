import psycopg2
import os
import random
import time
from datetime import datetime
from dotenv import load_dotenv
from psycopg2 import OperationalError

load_dotenv()

def get_db_connection():
    """Connects using DATABASE_URL or individual env vars."""
    while True:
        try:
            db_url = os.getenv("DATABASE_URL")
            if db_url:
                return psycopg2.connect(db_url)
            
            return psycopg2.connect(
                host=os.getenv("DB_HOST", "localhost"),
                database=os.getenv("DB_NAME"),
                user=os.getenv("DB_USER"),
                password=os.getenv("DB_PASSWORD")
            )
        except OperationalError:
            print("⏳ Database not ready yet, retrying in 2 seconds...")
            time.sleep(2)

def setup_database():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS click_logs (
            id SERIAL PRIMARY KEY,
            user_region VARCHAR(100),
            is_bot BOOLEAN,
            timestamp TIMESTAMP
        );
    """)
    conn.commit()
    cur.close()
    conn.close()

def simulate_traffic():
    print("🚀 Traffic Simulator Started. Writing to DB...")
    setup_database()
    conn = get_db_connection()
    cur = conn.cursor()
    
    try:
        while True:
            region = random.choice(['Mumbai', 'Delhi', 'Bangalore', 'Pune'])
            is_bot = random.random() < 0.25
            cur.execute(
                "INSERT INTO click_logs (user_region, is_bot, timestamp) VALUES (%s, %s, %s)",
                (region, is_bot, datetime.now())
            )
            conn.commit()
            print(f"✅ Injected: {region} | Bot: {is_bot}")
            time.sleep(3)
    except KeyboardInterrupt:
        print("\n🛑 Simulator Stopped.")
    finally:
        cur.close()
        conn.close()

if __name__ == "__main__":
    simulate_traffic()