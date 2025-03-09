import json
import os


import kafka
from dotenv import load_dotenv


load_dotenv()
KAFKA_BROKER_URL = os.getenv("KAFKA_BROKER_URL", "localhost:29092")
KAFKA_TOPIC = os.getenv("KAFKA_TOPIC", "user_actions")

def get_message():
    consumer = kafka.KafkaConsumer(
        bootstrap_servers=KAFKA_BROKER_URL,
        topic=KAFKA_TOPIC,
        value_deserializer=lambda value: json.loads(value.decode('utf-8')),
        auto_offset_reset='earliest',
        enable_auto_commit=True)

    print("Kafka Consumer listening message....")
    data = []
    for message in consumer:
        print(message)
        data.append(message.value)
    return data
