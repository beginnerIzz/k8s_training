import os
import psycopg2
from flask import Flask, jsonify

# Initialize Flask app
app = Flask(__name__)

# Load environment variables
DB_HOST = os.getenv("DB_HOST", "my_postgres")
DB_PORT = int(os.getenv("DB_PORT", "5432"))
DB_NAME = os.getenv("DB_NAME", "postgres")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASS = os.getenv("DB_PASS", "mystrongpassword")

# Function to connect to PostgreSQL
def get_db_connection():
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASS
        )
        print("✅ Connected to PostgreSQL!")
        return conn
    except Exception as e:
        print("❌ Database connection failed:", e)
        return None

#homepage
@app.route('/', methods=['GET'])
def home():
    return "Welcome to the Flask API!", 200

# Route to fetch users from PostgreSQL
@app.route('/users', methods=['GET'])
def get_users():
    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "❌ Database connection failed"}), 500
    
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users;")  # Ensure "users" is your actual table name
        rows = cursor.fetchall()  # Fetch all rows
        column_names = [desc[0] for desc in cursor.description]  # Get column names

        # Convert to list of dictionaries
        data = [dict(zip(column_names, row)) for row in rows]

        cursor.close()
        conn.close()
        return jsonify(data), 200  # Return data as JSON
    except Exception as e:
        return jsonify({"error": f"❌ Failed to fetch users: {e}"}), 500

# Run Flask app on port 5001
if __name__ == '__main__':
    print("🚀 Starting Flask app on port 5000...")
    app.run(host='0.0.0.0', port=5000, debug=True)

