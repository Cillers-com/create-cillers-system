from kafka import KafkaProducer
import json

def create_event(topic: str, event: dict):
    producer = KafkaProducer(bootstrap_servers=['redpanda:9092'],
                             value_serializer=lambda v: json.dumps(v).encode('utf-8'))
    producer.send(topic, event)
    producer.flush()
