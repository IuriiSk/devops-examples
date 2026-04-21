# DevOps Examples 🚀

Практический DevOps-портфолио репозиторий с реальными инфраструктурными проектами, контейнеризацией и CI/CD.

---

## 📌 О проекте

Этот репозиторий демонстрирует практические DevOps-навыки:

- контейнеризация приложений (Docker)
- multi-container архитектура
- Kubernetes манифесты (GKE-ready)
- Helm charts
- мониторинг и логирование
- автоматизация инфраструктуры
- CI/CD пайплайны (GitHub Actions)

[Docker](chatgpt://generic-entity?number=0)  
[Kubernetes](chatgpt://generic-entity?number=1)  
[GitHub Actions](chatgpt://generic-entity?number=2)  

---

## 📁 Структура проекта

### 📦 examples/
Практические backend и full-stack проекты:

- **todo-devops**  
  Flask + PostgreSQL + Nginx + Docker Compose  
  👉 полноценный DevOps стек:
  - backend (Flask)
  - database (PostgreSQL)
  - reverse proxy (Nginx)
  - persistent storage
  - healthcheck endpoint

- **todo-project (Node.js)**  
  Node.js + Express + Docker пример

- **docker-site**  
  frontend + backend + nginx + docker-compose

- **python-app**  
  минимальный Flask API пример

- **docker-compose-app**  
  Python + PostgreSQL приложение

[Flask](chatgpt://generic-entity?number=3)  
[PostgreSQL](chatgpt://generic-entity?number=4)  
[Nginx](chatgpt://generic-entity?number=5)  

---

### ☸️ k8s/
Kubernetes манифесты:
- Deployments
- Services
- Ingress
- GKE-ready конфигурации

---

### 📦 helm/
Helm charts для:
- Django приложений
- Node.js сервисов
- параметризованные Kubernetes деплои

---

### 📊 prometheus/
Monitoring stack:
- Prometheus
- Grafana dashboards
- Loki logging
- alerting rules

---

### ⚙️ scripts/
Infrastructure automation:
- создание cloud ресурсов (Droplet / GKE)
- бэкапы в object storage
- provisioning scripts
- DevOps automation utilities

---

## ⚙️ CI/CD

Проект включает GitHub Actions CI pipeline:

### CI выполняет:
- сборку Docker образа
- запуск контейнера
- smoke test (`/health` endpoint)

Запускается автоматически:
- при push в `main`
- при pull request

[GitHub Actions](chatgpt://generic-entity?number=6)  

---

## 🧰 Технологический стек

- Kubernetes (GKE)
- Docker / Docker Compose
- Helm
- Ansible
- GitHub Actions (CI/CD)
- Prometheus / Grafana / Loki
- PostgreSQL / MySQL / MongoDB / Redis
- Python / Node.js / Next.js
- Nginx Ingress

---

## 🎯 Цель проекта

Этот репозиторий создан для практики DevOps навыков:

- построение production-like инфраструктуры
- контейнеризация и оркестрация приложений
- CI/CD pipelines
- infrastructure as code (IaC)
- monitoring & logging (observability)

---

## 🚀 Запуск примеров

Пример запуска Docker проектов:

```bash
docker compose up --build