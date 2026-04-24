from flask import Flask, jsonify
import psycopg2
import redis

app = Flask(__name__)

# ---------- DB ----------
def get_db():
    return psycopg2.connect(
        host="db",
        database="tasks",
        user="postgres",
        password="postgres"
    )

# ---------- REDIS ----------
r = redis.Redis(host="redis", port=6379, decode_responses=True)

# ---------- INIT DB ----------
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

init_db()

# ---------- CREATE TASK ----------
@app.route("/task", methods=["POST"])
def create_task():
    conn = get_db()
    cur = conn.cursor()

    # создаём задачу
    cur.execute(
        "INSERT INTO tasks (status) VALUES ('pending') RETURNING id"
    )
    task_id = cur.fetchone()[0]

    conn.commit()
    cur.close()
    conn.close()

    # кладём в очередь Redis
    r.lpush("tasks", task_id)

    return jsonify({"task_id": task_id, "status": "pending"})

# ---------- GET TASK ----------
@app.route("/task/<int:task_id>")
def get_task(task_id):
    conn = get_db()
    cur = conn.cursor()

    cur.execute("SELECT status FROM tasks WHERE id=%s", (task_id,))
    row = cur.fetchone()

    cur.close()
    conn.close()

    if not row:
        return jsonify({"error": "not found"}), 404

    return jsonify({"task_id": task_id, "status": row[0]})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000)