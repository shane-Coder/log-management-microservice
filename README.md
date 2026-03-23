# Log Management Microservice

## 🚀 Overview

A scalable log ingestion and analytics system built using Django, Kafka, and MongoDB.
Designed to mimic real-world observability pipelines like ELK and Datadog.

---

## 🏗 Architecture

```
Client → Django API → Kafka → Consumer → MongoDB → Analytics APIs
```

---

## ⚙️ Tech Stack

* Django REST Framework
* Apache Kafka (KRaft mode)
* MongoDB
* Python

---

## 🔥 Features

* Bulk log ingestion
* Asynchronous processing via Kafka
* MongoDB-based storage (flexible schema)
* Search logs API
* Scalable event-driven architecture
* Analytics-ready structure

---

## 📌 APIs

### Logs

* `POST /api/logs/` → Ingest logs (single/bulk)
* `GET /api/logs/list/` → Fetch latest logs
* `GET /api/logs/search/?q=` → Search logs

### Analytics (Coming Next)

* Errors per service
* Logs per service
* Log level distribution
* Time-series metrics

---

## ▶️ How to Run Locally

### 1. Start Kafka

```bash
cd kafka_2.13-4.2.0

# (Run only first time)
bin/kafka-storage.sh random-uuid
bin/kafka-storage.sh format -t <UUID> -c config/server.properties

# Start Kafka
bin/kafka-server-start.sh config/server.properties
```

---

### 2. Start Consumer

```bash
python event_stream/consumer.py
```

---

### 3. Start Django Server

```bash
python manage.py runserver
```

---

## ⚙️ How It Works

1. Client sends logs to Django API
2. API publishes logs to Kafka topic
3. Consumer reads logs in batches
4. Logs are stored in MongoDB
5. Analytics APIs query MongoDB

---

## 🧪 Example Log

```json
{
  "service_name": "auth-service",
  "level": "INFO",
  "message": "User login",
  "timestamp": "2026-03-18T18:10:00Z",
  "metadata": {
    "user_id": 101
  }
}
```

---

## 📈 Scalability

* Kafka enables horizontal scaling via partitions
* Multiple consumers can process logs in parallel
* MongoDB supports flexible schema for log data

---

## 🚀 Future Improvements

* Alerting system (error thresholds)
* Grafana dashboards
* Log retention policies
* Docker & Kubernetes deployment

---

## 🚨 Alerting System

- Detects high error rates per service  
- Uses MongoDB aggregation with time-window filtering  
- Example: Trigger alert if errors exceed threshold in last 5 minutes  

---

## ⏱ Time Handling

All timestamps are stored in UTC using timezone-aware datetime for consistency across services.

---

{
  "alerts": [
    {
      "service": "payment-service",
      "error_count": 6
    }
  ]
}

---

- Real-time alerting (similar to Datadog / ELK)

---
## 📊 System Design Highlights

- Event-driven architecture using Kafka
- Scalable log ingestion pipeline
- MongoDB aggregation for analytics
- Alerting based on time-window queries
- TTL-based log retention

---
## 🧠 Design Decisions

- Kafka chosen over Celery for scalability
- MongoDB for flexible schema and aggregation
- UTC timestamps for consistency
- Batch processing for performance

## 👨‍💻 Author

Shivam
