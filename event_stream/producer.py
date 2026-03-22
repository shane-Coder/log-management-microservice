from confluent_kafka import Producer
import json
from datetime import datetime

producer=Producer({"bootstrap.servers":"localhost:9092"})

def serialize(obj):
    if isinstance(obj,datetime):
        return obj.isoformat()
    return obj

def send_logs(logs):
    for log in logs:
        producer.produce(
            "logs",
            json.dumps(log,default=serialize).encode("utf-8")
        )
    producer.flush()