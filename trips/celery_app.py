from core.config import celery, ssl_settings, settings
import requests
from datetime import timedelta

celery_app = celery

celery_app.conf.update(
    broker_use_ssl=ssl_settings,
    redis_backend_use_ssl=ssl_settings,
    task_serializer='json',
    result_serializer='json',
    accept_content=['json'],
    enable_utc=True, 
    timezone='Europe/Moscow',  
    broker_connection_retry_on_startup=True,
    task_acks_late=True,
    task_reject_on_worker_lost=True,
)

@celery_app.task(
    name='get_api_info',
    bind=True,
    max_retries=5,
    default_retry_delay=10
)

def get_api_info(self):
    try: 
        response = requests.get(f'{settings.BASE_URL}/trips/read')
        response.raise_for_status()
        return response.status_code
    except requests.RequestException as exc:
        self.retry(exc=exc)
    except Exception as e:
        raise e
    
celery_app.conf.beat_schedule = {
    'get_api_info': {
        'task': 'celery_app.get_api_info',
        'schedule': timedelta(minutes=1)
    }
}