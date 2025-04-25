from flask import Flask
import psycopg2
import os
import requests
app = Flask(__name__)

@app.route('/')
def hello():
    return "Hello, World!"

@app.route('/callback')
def callbackend():
    return requests.get('http://0.0.0.0:5000',timeout=10).text

@app.route('/connect_database')
def connect_database():
    DB_HOST = os.getenv("DB_HOST", "postgres-database-databases")
    DB_PORT = os.getenv("DB_PORT", "5432")
    DB_NAME = os.getenv("DB_NAME", "admin")
    DB_USER = os.getenv("DB_USER", "admin")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "Arghya1712")

    try:
        # Connect to the PostgreSQL server
        conn = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        )

        print("✅ Connected to PostgreSQL!")
        text= "✅ Connected to PostgreSQL!"
        # Run a simple query
        with conn.cursor() as cur:
            cur.execute("SELECT version();")
            version = cur.fetchone()
            print("PostgreSQL version:", version)

        conn.close()

    except Exception as e:
        print("❌ Could not connect to PostgreSQL:", e)
        text=  "❌ Could not connect to PostgreSQL: "+str(e)
    return text
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
