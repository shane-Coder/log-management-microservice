import os
import sys
import django
import json
from datetime import datetime, timezone
from confluent_kafka import Consumer

import time
last_flush = time.time()
FLUSH_INTERVAL = 5  # seconds

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJECT_ROOT = os.path.dirname(BASE_DIR)
sys.path.append(PROJECT_ROOT)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from logs.models import LogEntry

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
        print(f"Consumed: {log['service_name']} - {log['level']} - {log['timestamp']}")
        batch.append(
            LogEntry(
                service_name=log["service_name"],
                level=log["level"],
                message=log["message"],
                timestamp=datetime.fromisoformat(log["timestamp"]),
                metadata=log.get("metadata",{}),
                created_at=datetime.now(timezone.utc)
            )
        )
        print("Saving log:", log)
        if len(batch) >= BATCH_SIZE or time.time() - last_flush > FLUSH_INTERVAL:
            if batch:
                LogEntry.objects.insert(batch)
                batch.clear()
                last_flush = time.time()

except KeyboardInterrupt:
    pass

finally:
    if batch:
        LogEntry.objects.insert(batch)
    consumer.close()