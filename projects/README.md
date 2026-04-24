# Task Processor v1

## Архитектура

API → Postgres (source of truth)
API → Redis (queue)
Worker → Redis → Postgres update

## Запуск

```bash
docker compose up --build