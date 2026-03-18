import os
import sys
import django
import json
from datetime import datetime
from confluent_kafka import Consumer

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJECT_ROOT = os.path.dirname(BASE_DIR)
sys.path.append(PROJECT_ROOT)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.config.settings')
django.setup()

from core.logs.models import LogEntry

consumer = Consumer({
    "bootstrap.servers":"localhost:9092",
    "group.id":"log-consumers",
    "auto.offset.reset":"earliest"
})

consumer.subscribe(["logs"])

batch = []
BATCH_SIZE = 100

print("Consumer started...")

try:
    while True:
        msg = consumer.poll(1.0)
        
        if msg is None:
            continue
        if msg.error():
            print(msg.error())
            continue

        log = json.loads(msg.value().decode("utf-8"))
        print(f"Consumed: {log['service_name']} - {log['level']}")
        batch.append(
            LogEntry(
                service_name=log["service_name"],
                level=log["level"],
                message=log["message"],
                timestamp=datetime.fromisoformat(log["timestamp"]),
                metadata=log.get("metadata",{}),
                created_at=datetime.now()
            )
        )

        if len(batch) >= BATCH_SIZE:
            LogEntry.objects.insert(batch)
            batch.clear()

except KeyboardInterrupt:
    pass

finally:
    if batch:
        LogEntry.objects.insert(batch)
    consumer.close()