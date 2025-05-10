from celery import Celery

from app.config import settings


BROKER_URL = (f'redis://:{settings.REDIS_PASSWORD}@'
              f'{settings.REDIS_HOST}:{settings.REDIS_PORT}')

celery_app = Celery(
    'tasks',
    broker=BROKER_URL,
    include=["app.tasks.tasks"],
)
