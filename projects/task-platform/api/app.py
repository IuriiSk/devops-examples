from flask import Flask, request, jsonify
import redis
import psycopg2
import json
import os
import time

app = Flask(__name__)

redis_host = os.getenv("REDIS_HOST", "redis")


def connect_db():
    for _ in range(10):
        try:
            return psycopg2.connect(
                host=os.getenv("POSTGRES_HOST", "postgres"),
                dbname=os.getenv("POSTGRES_DB", "tasks"),
                user=os.getenv("POSTGRES_USER", "tasks"),
                password=os.getenv("POSTGRES_PASSWORD", "tasks"),
            )
        except psycopg2.OperationalError:
            time.sleep(2)

    raise RuntimeError("Could not connect to postgres")


db = connect_db()

r = redis.Redis(host=redis_host, port=6379, decode_responses=True)


@app.route("/health")
def health():
    return {"status": "ok"}


@app.route("/tasks", methods=["POST"])
def create_task():
    payload = request.get_json()
    name = payload.get("name")

    with db.cursor() as cur:
        cur.execute(
            "INSERT INTO tasks (name, status) VALUES (%s, %s) RETURNING id",
            (name, "queued"),
        )
        task_id = cur.fetchone()[0]
        db.commit()

    task = {
        "id": task_id,
        "name": name,
    }

    r.rpush("tasks", json.dumps(task))

    return jsonify({
        "status": "queued",
        "task": task,
    }), 202


@app.route("/tasks", methods=["GET"])
def list_tasks():
    with db.cursor() as cur:
        cur.execute("SELECT id, name, status FROM tasks ORDER BY id")
        rows = cur.fetchall()

    return jsonify([
        {
            "id": row[0],
            "name": row[1],
            "status": row[2],
        }
        for row in rows
    ])


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)