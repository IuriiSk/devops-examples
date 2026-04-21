#!/usr/bin/env python3
"""
Flask приложение с Prometheus метриками, Redis кэшем и MySQL
Для демонстрации навыков DevOps
"""

import os
import time
from functools import wraps

from flask import Flask, jsonify, request
from prometheus_flask_exporter import PrometheusMetrics
import redis
import pymysql
from pymysql.cursors import DictCursor

# Инициализация приложения
app = Flask(__name__)

# Prometheus метрики
metrics = PrometheusMetrics(app)
metrics.info('app_info', 'Application info', version='1.0.0')

# Кастомная метрика
REQUEST_COUNT = metrics.counter(
    'http_requests_total', 'Total HTTP requests',
    labels={'method': lambda: request.method, 'endpoint': lambda: request.endpoint}
)

# Подключение к Redis (из переменных окружения)
redis_client = redis.Redis(
    host=os.getenv('REDIS_HOST', 'localhost'),
    port=int(os.getenv('REDIS_PORT', 6379)),
    decode_responses=True
)

# Подключение к MySQL
def get_db_connection():
    return pymysql.connect(
        host=os.getenv('DB_HOST', 'localhost'),
        user=os.getenv('DB_USER', 'root'),
        password=os.getenv('DB_PASSWORD', ''),
        database=os.getenv('DB_NAME', 'flask_db'),
        cursorclass=DictCursor
    )

# Декоратор для кэширования в Redis
def cache(ttl=60):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            cache_key = f"{func.__name__}:{request.path}"
            cached = redis_client.get(cache_key)
            if cached:
                return jsonify({"source": "redis", "data": eval(cached)})
            
            result = func(*args, **kwargs)
            redis_client.setex(cache_key, ttl, str(result.get_json()))
            return result
        return wrapper
    return decorator

# Декоратор для измерения времени выполнения
def measure_time(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        duration = time.time() - start
        metrics.histogram('request_duration_seconds', 'Request duration').observe(duration)
        return result
    return wrapper

# Health check для Kubernetes
@app.route('/health')
@measure_time
def health():
    checks = {
        "status": "healthy",
        "redis": False,
        "mysql": False
    }
    
    # Проверка Redis
    try:
        redis_client.ping()
        checks["redis"] = True
    except:
        pass
    
    # Проверка MySQL
    try:
        conn = get_db_connection()
        conn.close()
        checks["mysql"] = True
    except:
        pass
    
    status_code = 200 if all([checks["redis"], checks["mysql"]]) else 503
    return jsonify(checks), status_code

# Readiness probe для Kubernetes
@app.route('/ready')
def ready():
    return jsonify({"status": "ready"}), 200

# API endpoint с кэшированием
@app.route('/api/users')
@REQUEST_COUNT
@measure_time
@cache(ttl=30)
def get_users():
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT id, name, email FROM users LIMIT 100")
            users = cursor.fetchall()
        return jsonify({"source": "database", "data": users})
    finally:
        conn.close()

# API endpoint с записью в БД
@app.route('/api/users', methods=['POST'])
@REQUEST_COUNT
@measure_time
def create_user():
    data = request.get_json()
    
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                "INSERT INTO users (name, email) VALUES (%s, %s)",
                (data['name'], data['email'])
            )
            conn.commit()
            
            # Инвалидируем кэш
            redis_client.delete("get_users:/api/users")
            
        return jsonify({"status": "created", "id": cursor.lastrowid}), 201
    finally:
        conn.close()

# Metrics endpoint для Prometheus
@app.route('/metrics')
def metrics_endpoint():
    return metrics.export_metrics()

# Root endpoint
@app.route('/')
def index():
    return jsonify({
        "service": "Flask DevOps Demo",
        "version": "1.0.0",
        "endpoints": [
            "/health - Health check",
            "/ready - Readiness probe",
            "/metrics - Prometheus metrics",
            "/api/users - GET (cached) / POST"
        ]
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)