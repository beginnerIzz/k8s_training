import os
import psycopg2
from flask import Flask, jsonify
from prometheus_flask_exporter import PrometheusMetrics
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST, REGISTRY

# Initialize Flask app
app = Flask(__name__)

# Initialize Prometheus metrics
metrics = PrometheusMetrics(app)
metrics.info('app_info', 'Application info', version='1.0.0')

# Define custom metrics
db_connection_failures = metrics.counter(
    'db_connection_failures', 'Number of database connection failures'
)

# Load environment variables
DB_HOST = os.getenv("DB_HOST", "postgres")
DB_PORT = int(os.getenv("DB_PORT", "5432"))
DB_NAME = os.getenv("DB_NAME", "my_postgres")
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
        print(f"❌ Database connection failed: {e}")
        db_connection_failures.inc()  # Increment counter on failure
        return None

# Homepage
@app.route('/', methods=['GET'])
@metrics.counter('home_endpoint_requests', 'Number of requests to homepage')
def home():
    return "Welcome to the Flask API!", 200

# Route to fetch users from PostgreSQL
@app.route('/users', methods=['GET'])
@metrics.counter('users_endpoint_requests', 'Number of requests to users endpoint')
@metrics.summary('users_endpoint_latency', 'Latency of users endpoint')
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

# Debugging Prometheus metrics
@app.route('/debug-metrics')
def debug_metrics():
    """List registered Prometheus metric names"""
    metric_names = [metric.name for metric in REGISTRY.collect()]
    return jsonify({"metrics": metric_names})

# Expose Prometheus metrics correctly
@app.route('/metrics')
def metrics():
    """Expose Prometheus metrics"""
    return generate_latest(), 200, {'Content-Type': CONTENT_TYPE_LATEST}

# Run Flask app on port 5000
if __name__ == '__main__':
    print("🚀 Starting Flask app on port 5000...")
    app.run(host='0.0.0.0', port=5000, debug=True)