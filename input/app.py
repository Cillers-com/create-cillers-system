import os
import json
from bottle import post, run, request

from confluent_kafka import Producer

PORT = int(os.getenv("APP_PORT", 8000))
KAFKA_BROKER = os.getenv("KAFKA_BROKER", 'localhost:9092')
KAFKA_TOPIC = os.getenv("KAFKA_TOPIC", 'mytopic')

if not KAFKA_BROKER:
    raise ValueError("KAFKA_BROKER is not set!")
if not KAFKA_TOPIC:
    raise ValueError("KAFKA_TOPIC is not set!")
print(f"Starting server on port {PORT}")
print(f"Kafka broker: {KAFKA_BROKER}")
print(f"Kafka topic: {KAFKA_TOPIC}")

producer = Producer({'bootstrap.servers': KAFKA_BROKER})

@post('/dummy-event')
def event():
    producer.produce('hook-dummy-event', value=json.dumps(request.json))
    producer.flush()
    return

run(host='0.0.0.0', port=PORT)
