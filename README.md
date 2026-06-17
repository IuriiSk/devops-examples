# DevOps Examples 🚀

Практический DevOps-портфолио репозиторий с реальными инфраструктурными проектами, контейнеризацией, автоматизацией развертывания (IaC) и CI/CD пайплайнами.


---

## 📌 О проекте

Этот репозиторий демонстрирует комплексные практические DevOps-навыки и содержит готовые к использованию production-like конфигурации:

- **Автоматизация конфигурации (IaC):** Сценарии Ansible для оркестрации и деплоя стеков на чистые серверы.
- **Контейнеризация и оркестрация:** Docker, Docker Compose, Kubernetes манифесты (GKE-ready) и Helm-чарты.
- **Сетевой инжиниринг:** Многоуровневое проксирование, балансировка трафика, защита от спуфинга и логирование.
- **Observability:** Стек мониторинга и сбора логов (Prometheus, Grafana, Loki).
- **Непрерывная интеграция:** Автоматические GitHub Actions CI пайплайны.

---

## 📁 Структура проекта

### ⚙️ ansible/
Инфраструктурная автоматизация и управление конфигурациями:
* **laravel-ansible** 🆕  
  Автоматическое развертывание полного стека Laravel + Nginx + MySQL + phpMyAdmin на чистом сервере Debian 11 с помощью Ansible и Docker.
  - **Особенности:** Полная идемпотентность, автоматический запуск миграций бэкенда только после прохождения MySQL Docker-healthcheck (`mysqladmin ping`), решение проблемы Race Condition при старте, автоматическое выставление прав `www-data` на директории `storage` и `cache`.

### 📦 examples/
Практические backend, full-stack и инфраструктурные проекты:

* **nginx-proxy-chain (Multi-Layer Nginx Reverse Proxy Chain)** 🆕  
  Высокотехнологичный тестовый проект, демонстрирующий многоуровневую архитектуру reverse proxy для безопасной передачи IP-адресов клиентов сквозь request chain.
  - **Архитектура:** `Пользователь` ➔ `nginx1 (edge)` ➔ `nginx2` ➔ `nginx3` ➔ `Flask + Gunicorn`
  - **Цель:** Построение доверенной цепочки проксирования, защита от подделки заголовков (HTTP Spoofing), корректное формирование `X-Forwarded-For` и изоляция контейнеров в статической Docker-сети с фиксированными IP.

* **todo-devops** Стек Flask + PostgreSQL + Nginx + Docker Compose с persistent storage и healthcheck-валидацией.

* **todo-project** — Node.js + Express приложение в Docker.
* **docker-site** — Связка Frontend + Backend + Nginx через Docker Compose.
* **python-app** — Минималистичный Flask API пример контейнеризации.

---

### ☸️ k8s/ & 📦 helm/
Оркестрация контейнеров промышленного уровня:
* **k8s/** — Манифесты (Deployments, Services, Ingress), адаптированные для быстрого деплоя в Google Kubernetes Engine (GKE).
* **helm/** — Параметризованные Helm-чарты для гибкого деплоя Django и Node.js приложений в различных окружениях (dev/stage/prod).

---

### 📊 prometheus/ & ⚙️ scripts/
* **prometheus/** — Стек мониторинга: Prometheus, Grafana Dashboards, сбор логов через Loki и настроенные правила алертинга.
* **scripts/** — Скрипты автоматизации: создание облачной инфраструктуры (DigitalOcean Droplets / GKE), утилиты бэкапа в S3-совместимые Object Storage.

---

## 🛠 Технологический стек

* **Оркестрация:** Kubernetes (GKE), Docker / Docker Compose, Helm
* **Автоматизация (IaC):** Ansible
* **CI/CD:** GitHub Actions
* **Веб-серверы / Прокси:** Nginx (Reverse Proxy, Ingress)
* **Базы данных:** PostgreSQL, MySQL 8.0, MongoDB, Redis
* **Мониторинг:** Prometheus, Grafana, Loki
* **Языки / Фреймворки:** Python (Flask, Django), PHP (Laravel), Node.js (Express), Next.js

---

## 🚀 Инструкции по запуску ключевых проектов

### 1. Стек Laravel (Ansible + Docker)
Проект находится в директории `ansible/laravel-ansible`.

1. Откройте `inventory.ini` и укажите параметры вашего сервера:
```ini
[servers]
laravel-vm ansible_host=YOUR_SERVER_IP ansible_port=2222

[servers:vars]
ansible_user=YOUR_SSH_USER
ansible_ssh_private_key_file=~/.ssh/YOUR_PRIVATE_KEY

1.	Запустите автоматический деплой:

ansible-playbook -i inventory.ini playbook.yml -K

Интерфейсы доступны по HTTP напрямую по IP сервера: / — Laravel (200 OK), /pma/ — phpMyAdmin (User: db, Pass: dbpassword).
2. Multi-Layer Nginx Reverse Proxy Chain
Проект находится в директории docked/nginx_project.

# 1. Запуск многоуровневого стека проксирования
docker compose up -d --build

# 2. Проверка статуса контейнеров и их Healthcheck
docker compose ps

# 3. Тест полной цепочки проксирования (Получение реального IP и пути)
curl localhost:8081/chain | jq

# 4. Тест защиты от подмены IP (Spoofing Test)
# Внедренный заголовок 1.1.1.1 будет проигнорирован/обработан согласно правилам безопасности
curl -H "X-Forwarded-For: 1.1.1.1" localhost:8081/chain | jq

# 5. Просмотр логов цепочки в реальном времени
tail -f logs/nginx1/access.log logs/nginx2/access.log logs/nginx3/access.log

# 6. Очистка окружения
docker compose down


⚙️ CI/CD Пайплайн
В репозиторий интегрированы пайплайны GitHub Actions, которые автоматически запускаются при каждом push в ветку main или создании pull request.
Пайплайн выполняет:
	1.	Линтинг конфигурационных файлов.
	2.	Тестовую сборку Docker-образов целевых сервисов.
	3.	Запуск изолированного тест-окружения.
	4.	Проведение Smoke-тестов (валидация /health эндпоинтов).