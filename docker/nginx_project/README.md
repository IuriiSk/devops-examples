# Multi-Layer Nginx Reverse Proxy Chain

DevOps тестовый проект, демонстрирующий:

- многоуровневую архитектуру reverse proxy (Nginx)
- передачу и формирование цепочки `X-Forwarded-For`
- защиту от подделки заголовков (spoofing)
- Docker Compose оркестрацию сервисов
- статическую Docker-сеть с фиксированными IP
- backend на Flask + Gunicorn
- healthcheck-и и зависимости сервисов
- production-style hardening контейнеров

---

# Архитектура

```text
Пользователь
   ↓
nginx1 (edge proxy)
   ↓
nginx2
   ↓
nginx3
   ↓
Flask + Gunicorn приложение

Цель проекта

Реализовать доверенную цепочку проксирования, где:

* приложение получает реальный IP клиента
* приложение видит всю цепочку прокси
* нельзя подменить IP через X-Forwarded-For
* только доверенные nginx добавляют себя в цепочку

Поддерживаемые сценарии

пользователь -> nginx1 -> приложение
пользователь -> nginx2 -> приложение
пользователь -> nginx3 -> приложение
пользователь -> nginx1 -> nginx2 -> nginx3 -> приложение

Приложение получает:

* IP клиента
* всю цепочку прокси

Приложение НЕ получает:

* поддельный X-Forwarded-For от пользователя

Стек технологий

* Docker
* Docker Compose
* Nginx
* Flask
* Gunicorn
* Alpine Linux

Структура проекта

.
├── app/
│   ├── app.py
│   └── Dockerfile
├── nginx1/
│   └── nginx.conf
├── nginx2/
│   └── nginx.conf
├── nginx3/
│   └── nginx.conf
├── logs/
│   ├── nginx1/
│   ├── nginx2/
│   └── nginx3/
├── docker-compose.yml
├── .dockerignore
└── README.md

Запуск и тесты

# =========================
# RUN PROJECT
# =========================

docker compose up -d --build

docker compose ps


# =========================
# HEALTH CHECK
# =========================

curl localhost:8081/health


# =========================
# SINGLE PROXY TESTS
# =========================

curl localhost:8081
curl localhost:8082
curl localhost:8083


# =========================
# FULL PROXY CHAIN TEST
# =========================

curl localhost:8081/chain | jq


# =========================
# SPOOFING TEST
# =========================

curl -H "X-Forwarded-For: 1.1.1.1" localhost:8081/chain | jq


# =========================
# NETWORK CHECK
# =========================

docker network inspect nginx_project_proxy_net


# =========================
# LOGS (REAL TIME)
# =========================

tail -f logs/nginx1/access.log
tail -f logs/nginx2/access.log
tail -f logs/nginx3/access.log


# =========================
# NGINX CONFIG CHECK
# =========================

docker exec -it nginx1 nginx -t
docker exec -it nginx2 nginx -t
docker exec -it nginx3 nginx -t


# =========================
# CLEAN UP
# =========================

docker compose down