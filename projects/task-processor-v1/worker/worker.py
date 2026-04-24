import redis
import psycopg2
import os
import time

r = redis.Redis(
    host=os.getenv("REDIS_HOST", "redis"),
    port=6379,
    db=int(os.getenv("REDIS_DB", 0)),  # 🔥 FIX
    decode_responses=True
)

def get_db():
    while True:
        try:
            return psycopg2.connect(
                host=os.getenv("POSTGRES_HOST", "db"),
                database=os.getenv("POSTGRES_DB", "tasks"),
                user=os.getenv("POSTGRES_USER", "postgres"),
                password=os.getenv("POSTGRES_PASSWORD", "postgres")
            )
        except:
            print("Waiting DB...")
            time.sleep(2)

print("Worker started")

while True:
    _, task_id = r.brpop("tasks")

    print("Processing:", task_id)
    time.sleep(2)

    conn = get_db()
    cur = conn.cursor()

    cur.execute(
        "UPDATE tasks SET status='done' WHERE id=%s",
        (task_id,)
    )

    conn.commit()
    cur.close()
    conn.close()

    print("Done:", task_id)