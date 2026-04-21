# DevOps Examples 🚀

Практический DevOps-портфолио репозиторий с инфраструктурой, CI/CD подходами и контейнеризированными приложениями.

---

## 📌 О проекте

Этот репозиторий содержит реальные DevOps-практики:

- контейнеризация приложений
- Kubernetes манифесты
- Helm charts
- мониторинг и логирование
- автоматизация инфраструктуры
- backend примеры (Node.js / Python)

---

## 📁 Структура

### 📦 examples/
Практические приложения и Docker-проекты:

- **todo-devops**  
  Flask + PostgreSQL + Nginx + Docker Compose  
  👉 полноценный multi-container стек

- **todo-project (Node.js)**  
  Node.js + Express + Docker пример

- **docker-site**  
  frontend/backend + nginx + docker-compose

- **python-app**  
  минимальный Flask backend

- **docker-compose-app**  
  Python + PostgreSQL пример

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
- параметризованные deployment’ы

---

### 📊 prometheus/
Мониторинг и observability:
- Prometheus
- Grafana dashboards
- Loki logging
- алерты

---

### ⚙️ scripts/
Infrastructure automation scripts:
- создание Droplet (DigitalOcean)
- бэкапы в DO Spaces
- деплой GKE cluster
- utility scripts

---

## 🧰 Технологический стек

- Kubernetes (GKE)
- Docker / Docker Compose
- Helm
- Ansible
- Jenkins CI/CD
- Prometheus / Grafana / Loki
- PostgreSQL / MySQL / MongoDB / Redis
- Python / Node.js / Next.js
- Nginx Ingress

---

## 🎯 Цель проекта

Этот репозиторий создан для практики DevOps навыков:

- построение production-like инфраструктуры
- работа с контейнерами и оркестрацией
- CI/CD pipelines
- observability (monitoring + logging)
- infrastructure as code

---

## 🚀 Запуск примеров

Пример (docker проекты):

```bash
docker compose up --build