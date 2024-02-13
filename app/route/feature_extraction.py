from fastapi import APIRouter, File, UploadFile, Form, Depends
from celery.result import AsyncResult
import time

from app.celery.celery_task import extract_task_data
from app.celery.celery_utils import get_task_info
from app.schema.input_patient import Input_patient

# router
extraction_route = APIRouter(prefix='/feature-extraction', tags=['feature-extraction'], responses={404: {"description": "Not found"}})

@extraction_route.get("/{task_id}")
async def get_task_status(task_id: str) -> dict:
    """
    Return the status of the submitted Task
    """
    return get_task_info(task_id)

@extraction_route.post("/")
async def extract_image(data: Input_patient = Depends(Input_patient.as_form)):

    # Extract data , countdown=2
    task = extract_task_data.apply_async(args=[data.hn, data.path_file, data.mpi_test_id], countdown=10)

    # Check staus task 
    task_result = AsyncResult(task.id)

    return {"task_id": task.id, "task_status": task_result.status} 
