import json

from fastapi import APIRouter

from app_statistic.repository.statistic_repository import StatisticsRepository
from app_statistic.schemas.schema import EventSchema
from app_statistic.service.statistic_service import StatisticService
from db.database import SessionLocal

# from kafka import KafkaConsumer
#
# KAFKA_BROKER_URL = '127.0.0.1:29092'
# KAFKA_TOPIC = 'user_actions'
#
# consumer = KafkaConsumer(KAFKA_TOPIC,
#                          bootstrap_servers=KAFKA_BROKER_URL,
#                          value_deserializer=lambda value: json.loads(value.decode('utf-8')),
#                          group_id='statistics_group')
#
#
# def read_message():
#     for message in consumer:
#         print(message)

router = APIRouter(prefix="/statistic", tags=["statistic"])
db = SessionLocal()
repository = StatisticsRepository(db)
service = StatisticService(repository)

@router.get("/get-all-statistics")
def get_all_statistics() -> list[EventSchema]:
    return service.get_all()

@router.get("/{username}")
def get_by_username_statistic(username: str):
    pass



