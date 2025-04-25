from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
import psycopg2
import os
import requests
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
logger = logging.getLogger(__name__)

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
    logger.info("Received request: /")
    return "Hello, World!"


@app.route('/callback')
def callbackend():
    logger.info("Received request: /callback")
    try:
        response = requests.get('http://data-health-check:5000', timeout=10)
        logger.info("Callback response received")
        return response.text
    except Exception as e:
        logger.error(f"Callback request failed: {e}")
        return f"Error: {str(e)}", 500


@app.route('/connect_database')
def connect_database():
    logger.info("Received request: /connect_database")
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        )
        logger.info("✅ Connected to PostgreSQL")

        with conn.cursor() as cur:
            cur.execute("SELECT version();")
            version = cur.fetchone()
            logger.info(f"PostgreSQL version: {version}")

        conn.close()
        return "✅ Connected to PostgreSQL!"
    except Exception as e:
        logger.error(f"❌ Could not connect to PostgreSQL: {e}")
        return f"❌ Could not connect to PostgreSQL: {e}", 500


@app.route("/query", methods=["POST"])
def query():
    logger.info("Received request: /query")
    sql = request.json.get("query")
    logger.info(f"Executing SQL query: {sql}")

    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        )
        logger.info("✅ Connected to PostgreSQL for query")

        with conn.cursor() as cur:
            cur.execute(sql)

            if cur.description:  # SELECT-like
                columns = [desc[0] for desc in cur.description]
                rows = cur.fetchall()
                logger.info("✅ Query executed and results fetched")
                return jsonify({"columns": columns, "rows": rows})
            else:  # INSERT/UPDATE/DDL
                conn.commit()
                logger.info("✅ Query executed with no result set")
                return jsonify({"columns": [], "rows": [["Query executed successfully"]]})

    except Exception as e:
        logger.error(f"❌ Query failed: {e}")
        return jsonify({"error": str(e)}), 400
    finally:
        if 'conn' in locals():
            conn.close()


@app.route("/ui", methods=["GET"])
def ui():
    logger.info("Serving UI at /ui")
    return render_template("index.html")


if __name__ == '__main__':
    logger.info("🚀 Starting Flask server on port 8080")
    app.run(host='0.0.0.0', port=8080)
