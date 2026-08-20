# Real-Time Log Anomaly Detection System

A real-time backend monitoring system that generates application logs, streams them through Apache Kafka, detects anomalies, stores processed logs in PostgreSQL, and exposes monitoring data through FastAPI REST endpoints.

## Tech Stack

- Python
- Apache Kafka
- PostgreSQL
- FastAPI
- Docker
- Docker Compose

## Architecture

Log Generator → Apache Kafka → Log Consumer → Anomaly Detection → PostgreSQL → FastAPI

## Features

- Generates simulated application logs in real time
- Streams logs through Apache Kafka
- Detects anomalies based on:
  - High response time
  - HTTP 500 server errors
  - ERROR-level logs
- Stores logs and anomaly information in PostgreSQL
- Provides REST APIs for logs, anomalies, and system statistics
- Includes interactive Swagger API documentation

## API Endpoints

- `GET /` — API health check
- `GET /logs` — Retrieve processed logs
- `GET /anomalies` — Retrieve detected anomalies
- `GET /stats` — View monitoring statistics
- `GET /docs` — Swagger API documentation

## Run Locally

Start Kafka and PostgreSQL:

```bash
docker compose up -d
