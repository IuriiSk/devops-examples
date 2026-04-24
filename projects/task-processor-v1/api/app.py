from flask import Flask, jsonify
import psycopg2
import redis
import os
import time

app = Flask(__name__)

# ---------------- DB ----------------
def get_db():
    while True:
        try:
            conn = psycopg2.connect(
                host=os.getenv("POSTGRES_HOST", "db"),
                database=os.getenv("POSTGRES_DB", "tasks"),
                user=os.getenv("POSTGRES_USER", "postgres"),
                password=os.getenv("POSTGRES_PASSWORD", "postgres")
            )
            return conn
        except Exception as e:
            print("⏳ Waiting for DB...", e)
            time.sleep(2)

# ---------------- REDIS (FIXED: no global client) ----------------
def get_redis():
    while True:
        try:
            r = redis.Redis(
                host=os.getenv("REDIS_HOST", "redis"),
                port=6379,
                db=0,
                decode_responses=True
            )
            r.ping()
            return r
        except Exception as e:
            print("⏳ Waiting for Redis...", e)
            time.sleep(1)

# ---------------- INIT DB ----------------
def init_db():
    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id SERIAL PRIMARY KEY,
            status TEXT
        )
    """)

    conn.commit()
    cur.close()
    conn.close()

    print("✅ DB initialized")

init_db()

# ---------------- ROUTES ----------------
@app.route("/task", methods=["POST"])
def create_task():
    r = get_redis()   # 🔥 fresh connection per request

    conn = get_db()
    cur = conn.cursor()

    cur.execute(
        "INSERT INTO tasks (status) VALUES ('pending') RETURNING id"
    )
    task_id = cur.fetchone()[0]

    conn.commit()
    cur.close()
    conn.close()

    print("📦 TASK CREATED:", task_id)

    # 🔥 Redis push (guaranteed)
    r.lpush("tasks", str(task_id))

    print("📨 REDIS STATE:", r.lrange("tasks", 0, -1))

    return jsonify({"task_id": task_id})

@app.route("/task/<int:task_id>")
def get_task(task_id):
    conn = get_db()
    cur = conn.cursor()

    cur.execute(
        "SELECT status FROM tasks WHERE id=%s",
        (task_id,)
    )
    row = cur.fetchone()

    cur.close()
    conn.close()

    if row:
        return jsonify({
            "task_id": task_id,
            "status": row[0]
        })

    return jsonify({"error": "not found"}), 404

# ---------------- RUN ----------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000)