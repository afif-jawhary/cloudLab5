from flask import Flask
import redis
import psycopg2

app = Flask(__name__)

# Connect to Redis
r = redis.Redis(host="redis", port=6379)

# Connect to PostgreSQL
conn = psycopg2.connect(
    host="postgres",
    database="flask_db",
    user="flask_user",
    password="flask_password"
)
cur = conn.cursor()

# Create a table if it doesn't exist
cur.execute("""
    CREATE TABLE IF NOT EXISTS visits (
        id SERIAL PRIMARY KEY,
        count INTEGER NOT NULL
    )
""")
conn.commit()

@app.route("/")
def home():
    # Increment the Redis counter
    count = r.incr("hits")

    # Insert or update the count in PostgreSQL
    cur.execute("INSERT INTO visits (count) VALUES (%s) RETURNING id", (count,))
    conn.commit()
    
    return f"This page has been visited {count} times."

if __name__ == "__main__":
    app.run(host="0.0.0.0")
