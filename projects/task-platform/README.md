# Task Platform

A small event-driven task processing platform built for a DevOps portfolio.

## Overview

This project demonstrates a minimal asynchronous architecture:

- API service accepts tasks via HTTP
- Redis acts as a message queue
- Worker consumes queued tasks asynchronously
- PostgreSQL stores task state transitions

Task lifecycle:

queued → processing → done

---

## Architecture

text Client   |   v API (Flask)   |   +--> PostgreSQL   |   v Redis queue   |   v Worker   |   v PostgreSQL 

---

## Tech Stack

- Flask
- Redis
- PostgreSQL
- Docker
- GitHub

---

## Project Structure

text task-platform/ ├── api/ │   ├── app.py │   ├── requirements.txt │   └── Dockerfile ├── worker/ │   ├── worker.py │   ├── requirements.txt │   └── Dockerfile ├── init.sql ├── docker-compose.yml └── README.md 

---

## Run Locally

bash docker compose up --build 

Check service health:

bash docker compose ps 

---

## API Usage

### Create task

bash curl -X POST http://localhost:5001/tasks \   -H "Content-Type: application/json" \   -d '{"name":"portfolio task"}' 

Example response:

json {   "status": "queued",   "task": {     "id": 1,     "name": "portfolio task"   } } 

---

### List tasks

bash curl http://localhost:5001/tasks 

Example response:

json [   {     "id": 1,     "name": "portfolio task",     "status": "done"   } ] 

---

## Health Endpoint

bash curl http://localhost:5001/health 

---

## Production-Oriented Features

This project includes several practical DevOps-oriented elements:

- containerized services
- asynchronous background processing
- database-backed task state tracking
- health checks for service readiness
- restart policies for resiliency
- clean multi-service local orchestration

---

## Next Improvements

Planned next steps:

- add CI with GitHub Actions
- add tests
- add metrics with Prometheus
- package deployment with Helm
- deploy to Kubernetes

---

## Why This Project

The goal of this project is to demonstrate practical DevOps skills beyond a simple CRUD application:

- service decomposition
- inter-service communication
- message queues
- observability readiness
- deployment readiness