import random
from kafka import KafkaProducer
import json
import time
from datetime import datetime

services = ["auth-service", "payment-service", "order-service", "product-service"]
levels = ["INFO", "INFO", "INFO", "WARNING", "ERROR"]

messages = {
    "INFO": [
        "Request completed successfully",
        "User login successful",
        "Order processed successfully",
        "Product data retrieved"
    ],
    "WARNING": [
        "High response time detected",
        "Database connection is slow"
    ],
    "ERROR": [
        "Database connection failed",
        "Payment processing failed",
        "Internal server error"
    ]
}

producer = KafkaProducer(
    bootstrap_servers="localhost:9092",
    value_serializer=lambda v: json.dumps(v).encode("utf-8")
)

while True:
    level = random.choice(levels)

    log = {
        "timestamp": datetime.now().isoformat(),
        "service": random.choice(services),
        "level": level,
        "response_time": random.randint(100, 5000),
        "status_code": random.choice([200, 200, 200, 400, 500]),
        "message": random.choice(messages[level])
    }

    producer.send("application-logs", log)
    producer.flush()

    print("Sent to Kafka:", log)

    time.sleep(2)