import redis
import psycopg2
import time

# ---------- REDIS ----------
r = redis.Redis(
    host="redis",
    port=6379,
    decode_responses=True
)

# ---------- DB ----------
def get_db():
    return psycopg2.connect(
        host="db",
        database="tasks",
        user="postgres",
        password="postgres"
    )

print("🚀 Worker started")

while True:
    task = r.brpop("tasks")  # блокирующее ожидание

    if task:
        task_id = task[1]
        print(f"⚙️ Processing task {task_id}")

        time.sleep(2)  # имитация работы

        conn = get_db()
        cur = conn.cursor()

        cur.execute(
            "UPDATE tasks SET status='done' WHERE id=%s",
            (task_id,)
        )

        conn.commit()
        cur.close()
        conn.close()

        print(f"✅ Done task {task_id}")