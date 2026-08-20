from fastapi import FastAPI
import psycopg2
from psycopg2.extras import RealDictCursor

app = FastAPI(title="Log Anomaly Detection API")

def get_db_connection():
    return psycopg2.connect(
        host="localhost",
        port=5432,
        database="logs_db",
        user="postgres",
        password="postgres",
        cursor_factory=RealDictCursor
    )


@app.get("/")
def home():
    return {
        "message": "Log Anomaly Detection API is running"
    }


@app.get("/logs")
def get_logs():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT *
        FROM logs
        ORDER BY id DESC
        LIMIT 100
        """
    )

    logs = cursor.fetchall()

    cursor.close()
    conn.close()

    return logs


@app.get("/anomalies")
def get_anomalies():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT *
        FROM logs
        WHERE is_anomaly = TRUE
        ORDER BY id DESC
        LIMIT 100
        """
    )

    anomalies = cursor.fetchall()

    cursor.close()
    conn.close()

    return anomalies


@app.get("/stats")
def get_stats():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) AS total_logs FROM logs")
    total_logs = cursor.fetchone()["total_logs"]

    cursor.execute(
        """
        SELECT COUNT(*) AS total_anomalies
        FROM logs
        WHERE is_anomaly = TRUE
        """
    )
    total_anomalies = cursor.fetchone()["total_anomalies"]

    cursor.execute(
        """
        SELECT AVG(response_time) AS average_response_time
        FROM logs
        """
    )
    average_response_time = cursor.fetchone()["average_response_time"]

    cursor.close()
    conn.close()

    return {
        "total_logs": total_logs,
        "total_anomalies": total_anomalies,
        "average_response_time": (
            float(average_response_time)
            if average_response_time is not None
            else 0
        )
    }