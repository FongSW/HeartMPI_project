from fastapi import FastAPI
import uvicorn as uvicorn
import subprocess

#import router
from app.route.base_inference import base_inference_route
# from app.route.airflow_inference import airflow_inference_route
from app.route.feature_extraction import extraction_route
from app.celery.celery_utils import create_celery

# import utility functon (set model)
from app.utility_function.query_ml_model import query_ml_acc
from app.utility_function.qualitative.predict_qualitative import set_quali_model, load_qualitative_model_v2

def create_app() -> FastAPI:
    current_app = FastAPI(title="Web Heart-mibi")
    current_app.celery_app = create_celery()
    current_app.include_router(base_inference_route)
    # current_app.include_router(airflow_inference_route)
    current_app.include_router(extraction_route)

    # root api
    @current_app.get("/")
    async def root():
        return {'msg':'This API from project AI_assistant_heart_mibi'}
    
    # restart api
    @current_app.get("/restrat")
    async def restart_api():

        # restart
        subprocess.run(["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8001"])
        print(">>>>> Restrart FastAPI")
        return {'msg': 'Restarting API was complete'}
    
    # Register the startup event handler
    @current_app.on_event("startup")
    async def on_start_function():

        # query ml model accuracy and set values on start
        query_ml_acc()
        
        print("-" * 25, "Load model on start")
        
        # loaded once qualitative models and burn
        set_quali_model(*load_qualitative_model_v2())
        
    return current_app

# Fast-API
app = create_app()
celery = app.celery_app


# # main.py

# from router.py import set_model

# model = <bla bla>

# set_model(model)


# ----------------------
# # router.py

# stored_model = None

# def set_model(model):
#     stored_model = model

# use(stored_model)