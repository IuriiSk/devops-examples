from flask import Flask, request, jsonify
import redis
import json
import os

app = Flask(__name__)

redis_host = os.getenv("REDIS_HOST", "redis")
r = redis.Redis(host=redis_host, port=6379, decode_responses=True)


@app.route("/health")
def health():
    return {"status": "ok"}


@app.route("/tasks", methods=["POST"])
def create_task():
    payload = request.get_json()

    task = {
        "name": payload.get("name")
    }

    r.rpush("tasks", json.dumps(task))

    return jsonify({
        "status": "queued",
        "task": task
    }), 202


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)