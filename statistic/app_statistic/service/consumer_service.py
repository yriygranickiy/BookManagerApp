import json
import os
import uuid
from datetime import datetime

import kafka
from dotenv import load_dotenv

from app_statistic.models.statistic_models import StatisticModel
from app_statistic.repository.statistic_repository import StatisticRepository
from app_statistic.service.statistic_service import StatisticService
from db.database import get_db, SessionLocal

db = SessionLocal()
repository = StatisticRepository(db)
service = StatisticService(repository)

load_dotenv()
KAFKA_BROKER_URL = os.getenv("KAFKA_BROKER_URL", "localhost:29092")
KAFKA_TOPIC = os.getenv("KAFKA_TOPIC", 'user_actions')

def get_message():
    consumer = kafka.KafkaConsumer(
        KAFKA_TOPIC,
        bootstrap_servers=KAFKA_BROKER_URL,
        auto_offset_reset='earliest',
        value_deserializer=lambda m: json.loads(m.decode('utf-8')),
        enable_auto_commit=False,
        group_id='statistic-consumer-group'
    )

    print("Kafka Consumer listening message....")

    try:
        while True:
            message_pack = consumer.poll(timeout_ms=5000)
            if not message_pack:
                continue
            for messages in message_pack.values():
                for message in messages:
                    print(f"Received message: {message.value}")
                    data = message.value
                    book_instance_id = data.get("id")
                    username = data.get("username")
                    status = data.get("status")
                    time = data.get("time")
                    statistic = StatisticModel(book_instance_id=book_instance_id,
                                       username=username,
                                       status=status,
                                       time_updated=datetime.fromtimestamp(time))
                    service.create(statistic)
            consumer.commit()
    except KeyboardInterrupt:
        print("Keyboard interrupt received, shutting down...")
    finally:
        consumer.close()
