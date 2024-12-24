from flask import Flask, request, jsonify
from src.limiter import sliding_window_rate_limiter
from src.cache import timed_lru_cache
from prometheus_flask_exporter import PrometheusMetrics

        
app = Flask(__name__)
metrics = PrometheusMetrics(app)
metrics.info("app_info", "App Info, this can be anything you want", version="1.0.0")

# Test function with timed cache
@timed_lru_cache(maxsize=128, ttl=10)
def get_cached_data():
    return {"a": 1, "b": 5}


@app.route('/api/resource', methods=['GET'])
@sliding_window_rate_limiter
def protected_resource():
    mssg_json = get_cached_data()
    return jsonify({"message": mssg_json})

