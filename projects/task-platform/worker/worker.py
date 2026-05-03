import redis
import psycopg2
import json
import time
import os


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


r = redis.Redis(
    host=os.getenv("REDIS_HOST", "redis"),
    port=6379,
    decode_responses=True,
)

db = connect_db()

print("Worker started...")

while True:
    task = r.blpop("tasks", timeout=5)

    if task:
        _, payload = task
        data = json.loads(payload)

        task_id = data["id"]

        with db.cursor() as cur:
            cur.execute(
                "UPDATE tasks SET status=%s WHERE id=%s",
                ("processing", task_id),
            )
            db.commit()

        print(f"Processing task: {data['name']}")
        time.sleep(2)

        with db.cursor() as cur:
            cur.execute(
                "UPDATE tasks SET status=%s WHERE id=%s",
                ("done", task_id),
            )
            db.commit()

        print(f"Done: {data['name']}")