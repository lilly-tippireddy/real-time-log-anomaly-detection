import json
import psycopg2
from kafka import KafkaConsumer

consumer = KafkaConsumer(
    "application-logs",
    bootstrap_servers="localhost:9092",
    auto_offset_reset="earliest",
    enable_auto_commit=True,
    group_id="log-anomaly-consumer",
    value_deserializer=lambda x: json.loads(x.decode("utf-8"))
)

conn = psycopg2.connect(
    host="localhost",
    port=5432,
    database="logs_db",
    user="postgres",
    password="postgres"
)

cursor = conn.cursor()

print("Waiting for logs...")

for message in consumer:
    log = message.value

    is_anomaly = False
    reasons = []

    if log["response_time"] > 3000:
        is_anomaly = True
        reasons.append("High response time")

    if log["status_code"] >= 500:
        is_anomaly = True
        reasons.append("Server error")

    if log["level"] == "ERROR":
        is_anomaly = True
        reasons.append("Error log")

    anomaly_reason = ", ".join(reasons) if reasons else None

    cursor.execute(
        """
        INSERT INTO logs (
            timestamp,
            service,
            level,
            response_time,
            status_code,
            message,
            is_anomaly,
            anomaly_reason
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """,
        (
            log["timestamp"],
            log["service"],
            log["level"],
            log["response_time"],
            log["status_code"],
            log["message"],
            is_anomaly,
            anomaly_reason
        )
    )

    conn.commit()

    if is_anomaly:
        print("ANOMALY DETECTED")
        print("Log:", log)
        print("Reason:", anomaly_reason)
        print("-" * 60)
    else:
        print("Normal:", log)

    print("Saved to PostgreSQL")