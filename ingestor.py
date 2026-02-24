import psycopg2
import csv

def migrate_csv_to_db():
    # 1. Connection Details
    # Replace 'your_password_here' with your real pgAdmin password
    conn_params = {
        "host": "localhost",
        "database": "ad_tech_db",
        "user": "postgres",
        "password": "Eshaa@123" 
    }

    try:
        # 2. Connect to the "Vault"
        print("Connecting to PostgreSQL...")
        conn = psycopg2.connect(**conn_params)
        cursor = conn.cursor()

        # 3. Open the CSV file we generated earlier
        with open('ad_clicks_dataset.csv', 'r') as f:
            reader = csv.reader(f)
            next(reader)  # Skip the header row
            
            print("Uploading data to the 'click_logs' table...")
            for row in reader:
                # SQL command to insert data
                cursor.execute(
                    "INSERT INTO click_logs (ad_id, campaign_name, source_url, user_region, device_type, click_duration_ms, is_bot) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                    row
                )
        
        # 4. Save (Commit) the changes
        conn.commit()
        print(f"Success! 10,000 rows have been moved to the vault.")

    except Exception as e:
        print(f"Error during ingestion: {e}")
    
    finally:
        if conn:
            cursor.close()
            conn.close()

if __name__ == "__main__":
    migrate_csv_to_db()