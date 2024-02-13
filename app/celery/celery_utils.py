from celery  import current_app as current_celery_app
from celery.result import AsyncResult
from celery import Celery
from kombu import Queue
import os

def create_celery():
    celery_app =  Celery(__name__)
    celery_app.conf.broker_url = "amqp://guest:guest@rabbitmq:5672/"
    celery_app.conf.result_backend = "rpc://"
    celery_app.conf.update(task_track_started=True)
    celery_app.conf.update(result_expires=600)
    celery_app.conf.update(result_extended=True)
    celery_app.conf.update(result_persistent=True) 
    celery_app.conf.update(worker_send_task_events=False)
    celery_app.conf.update(worker_prefetch_multiplier=1)
    celery_app.conf.update(worker_concurrency=1)
    celery_app.conf.update(task_acks_late=True)
    # celery_app.conf.update(task_acks_on_failure_or_timeout=True)
    # celery_app.conf.update(task_reject_on_worker_lost=True)
    #celery_app.conf.task_queues = [Queue("extract_data")] task_soft_time_limit

def get_task_info(task_id):
    """
    return task info for the given task_id
    """
    task_result = AsyncResult(task_id)
    print("task_result :", task_result)
    
    result = {
        "task_id": task_id,
        "task_status": task_result.status,
        "task_result": task_result.result
    }
    return result