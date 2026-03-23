# Log Management Microservice

## 🚀 Overview
A log ingestion and analytics microservice built using Django, Kafka, and MongoDB.  
This project simulates a real-world observability pipeline similar to ELK or Datadog.

---

## 🏗 Architecture

Client → Django API → Kafka → Consumer → MongoDB → APIs

---

## ⚙️ Tech Stack

- Django REST Framework
- Apache Kafka
- MongoDB
- Docker (optional)
- Python

---

## 🔥 Features

- Log ingestion (single & bulk)
- Asynchronous processing using Kafka
- MongoDB storage (flexible schema)
- Log search API
- Basic alerting (error threshold)
- Simple analytics (stats API)

---

## 📌 APIs

### Logs
- POST /api/logs
- GET /api/logs/list
- GET /api/logs/search?q=

### Alerts
- GET /api/alerts

### Stats
- GET /api/stats

---

## Run with Docker

Start all services:

```

docker-compose up --build

```

Access:
- API: http://127.0.0.1:8000
- MongoDB: mongodb://localhost:27018

---

## ▶️ Run Locally (Manual Setup)

### 1. Start Kafka

```bash

cd kafka_2.13-4.2.0

# Run only first time

bin/kafka-storage.sh random-uuid
bin/kafka-storage.sh format -t <UUID> -c config/server.properties

bin/kafka-server-start.sh config/server.properties

```

### 2. Start Consumer

```bash

python event_stream/consumer.py

```

### 3. Start Django

```bash

python manage.py runserver

```

---

## 🧪 Example Log

```json

{
  "service_name": "auth-service",
  "level": "ERROR",
  "message": "Invalid credentials",
  "timestamp": "2026-03-18T18:10:00Z",
  "metadata": {
    "user_id": 101
  }
}

```

---

## ⚙️ How It Works

1. Logs are sent to Django API  
2. API pushes logs to Kafka  
3. Consumer reads logs in batches  
4. Logs are stored in MongoDB  
5. APIs fetch logs and analytics  

---

## 🧠 Notes

- Timestamps are stored in UTC  
- MongoDB is used for flexible log schema  
- Kafka enables scalable log processing  

---

## 👨‍💻 Author

Shivam  
LinkedIn: https://www.linkedin.com/in/programmer-shivam/  
GitHub: https://github.com/shane-Coder

---
