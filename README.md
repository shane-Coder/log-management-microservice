# Log Management Microservice

## 🚀 Overview
A scalable log ingestion and analytics system built using Django, Kafka, and MongoDB.  
Designed to mimic real-world observability pipelines like ELK and Datadog.

---

## 🏗 Architecture

Client → Django API → Kafka → Consumer → MongoDB → Analytics APIs

---

## ⚙️ Tech Stack

- Django REST Framework  
- Apache Kafka (KRaft mode)  
- MongoDB  
- Python  

---

## 🔥 Features

- Bulk log ingestion  
- Asynchronous processing via Kafka  
- MongoDB-based storage (flexible schema)  
- Search logs API  
- Scalable event-driven architecture  
- Analytics-ready structure  

---

## 📌 APIs

### Logs
- `POST /api/logs/` → Ingest logs (single/bulk)  
- `GET /api/logs/list/` → Fetch latest logs  
- `GET /api/logs/search/?q=` → Search logs  

### Analytics (WIP / Step 6)
- Errors per service  
- Logs per service  
- Log level distribution  
- Time-series metrics  

---

## ▶️ How to Run Locally

### 1. Start Kafka
```bash
cd kafka_2.13-4.2.0
bin/kafka-server-start.sh config/server.properties

2. Start Consumer
```bash
python core/event_stream/consumer.py

3. Start Django Server
```bash
python manage.py runserver

🧪 Example Log
```JSON
{
  "service_name": "auth-service",
  "level": "INFO",
  "message": "User login",
  "timestamp": "2026-03-18T18:10:00Z",
  "metadata": 
  {
    "user_id": 101
  }
}