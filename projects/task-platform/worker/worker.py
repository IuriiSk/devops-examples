import redis
import json
import time
import os

redis_host = os.getenv("REDIS_HOST", "redis")
r = redis.Redis(host=redis_host, port=6379, decode_responses=True)

print("Worker started...")

while True:
    task = r.blpop("tasks", timeout=5)

    if task:
        _, payload = task
        data = json.loads(payload)

        print(f"Processing task: {data['name']}")
        time.sleep(2)
        print(f"Done: {data['name']}")