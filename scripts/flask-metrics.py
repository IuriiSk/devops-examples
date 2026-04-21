from flask import Flask
from prometheus_flask_exporter import PrometheusMetrics
import redis
import pymongo

app = Flask(__name__)
metrics = PrometheusMetrics(app)

redis_client = redis.Redis(host='redis-service', port=6379)
mongo_client = pymongo.MongoClient('mongodb://mongo-service:27017')

@app.route('/api/health')
def health():
    return {"status": "ok"}

@app.route('/api/data')
@metrics.counter('api_requests_total', 'Number of requests')
def get_data():
    cache = redis_client.get('key')
    if cache:
        return {"source": "redis", "data": cache}
    
    data = mongo_client.db.collection.find_one()
    redis_client.setex('key', 60, str(data))
    return {"source": "db", "data": data}