from flask import Flask, jsonify, request
from flask_cors import CORS
import psycopg2
from kafka import KafkaProducer, KafkaConsumer
import threading
import logging
import time
from psycopg2 import OperationalError
from kafka.errors import KafkaError
from kafka.admin import KafkaAdminClient, NewTopic

app = Flask(__name__)
CORS(app)

logging.basicConfig(level=logging.INFO)

def create_connection():
    attempts = 5
    while attempts > 0:
        try:
            conn = psycopg2.connect(
                host="database",
                port=5432,
                user="postgres",
                password="postgres",
                dbname="appdb"
            )
            logging.info("Successfully connected to the database.")
            return conn
        except OperationalError as e:
            logging.error(f"Database connection failed: {e}")
            attempts -= 1
            time.sleep(5)
    raise Exception("Failed to connect to the database after multiple attempts.")

conn = create_connection()

producer = KafkaProducer(bootstrap_servers='kafka:9092')

def create_kafka_topic():
    admin_client = KafkaAdminClient(
        bootstrap_servers='kafka:9092',
        client_id='backend'
    )
    topic_list = [NewTopic(name="my-topic", num_partitions=1, replication_factor=1)]
    try:
        admin_client.create_topics(new_topics=topic_list, validate_only=False)
        logging.info("Kafka topic 'my-topic' created successfully.")
    except Exception as e:
        logging.warning(f"Kafka topic 'my-topic' may already exist: {e}")

create_kafka_topic()

@app.route('/api/data', methods=['GET'])
def get_data():
    """Zwraca dane z bazy danych"""
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM sample_table;")
        rows = cursor.fetchall()
        logging.info("Successfully fetched data from the database.")
        return jsonify([{"id": row[0], "data": row[1]} for row in rows])
    except Exception as e:
        logging.error(f"Database error: {e}")
        conn.rollback()
        return jsonify({"error": "Failed to fetch data from the database."}), 500

@app.route('/api/send', methods=['POST'])
def send_message():
    """Wysyła wiadomość do Kafka"""
    try:
        data = request.json
        message = data.get("message", "default message")
        future = producer.send('my-topic', value=message.encode('utf-8'))
        future.get(timeout=10)
        logging.info(f"Message sent to Kafka: {message}")
        return jsonify({"status": "Message sent to Kafka!"})
    except KafkaError as e:
        logging.error(f"Kafka send error: {e}")
        return jsonify({"error": "Failed to send message to Kafka."}), 500
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        return jsonify({"error": str(e)}), 500

def save_kafka_messages():
    consumer = KafkaConsumer(
        'my-topic',
        bootstrap_servers='kafka:9092',
        auto_offset_reset='earliest',
        enable_auto_commit=True,
        group_id='database-consumer'  
    )
    for message in consumer:
        try:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO sample_table (data) VALUES (%s)", (message.value.decode('utf-8'),))
            conn.commit()
            logging.info(f"Saved message to database: {message.value.decode('utf-8')}")
        except Exception as e:
            logging.error(f"Error saving message to database: {e}")

threading.Thread(target=save_kafka_messages, daemon=True).start()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
