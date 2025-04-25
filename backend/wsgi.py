from flask import Flask,jsonify,request,render_template
from flask_cors import CORS
import psycopg2
import os
import requests
app = Flask(__name__)
CORS(app)
# Load environment variables
DB_HOST = os.getenv("DB_HOST", "postgres-database-databases")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "admin")
DB_USER = os.getenv("DB_USER", "admin")
DB_PASSWORD = os.getenv("DB_PASSWORD", "Arghya1712")

@app.route('/')
def hello():
    return "Hello, World!"

@app.route('/callback')
def callbackend():
    return requests.get('http://data-health-check:5000',timeout=10).text

@app.route('/connect_database')
def connect_database():
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

@app.route("/query", methods=["POST"])
def query():
    conn = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        )
    print("✅ Connected to PostgreSQL!")
    sql = request.json.get("query")
    try:
        with conn.cursor() as cur:
            cur.execute(sql)
            if cur.description:  # SELECT statement
                columns = [desc[0] for desc in cur.description]
                rows = cur.fetchall()
                return jsonify({"columns": columns, "rows": rows})
            else:
                conn.commit()
                return jsonify({"columns": [], "rows": [["Query executed successfully"]]})
    except Exception as e:
        return jsonify({"error": str(e)}), 400   
    
@app.route("/ui", methods=["GET"])
def ui():
    return render_template("index.html")
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
