from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse
import uvicorn
from src.utils.gcp_utils import download_blob
from src.utils.logger import logger
from src.constants import *
from src.entity.config_entity import *
import joblib as jb
import os
from contextlib import asynccontextmanager

model = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    global model
    os.makedirs(ModelTrainingConfig.model_training_artifacts_dir, exist_ok=True)
    
    logger.info("Downloading model...")
    download_blob(GCP_BUCKET_NAME, MODEL_PATH, ModelTrainingConfig.model_training_file_path)
    
    model = jb.load(ModelTrainingConfig.model_training_file_path)
    yield

app = FastAPI(lifespan=lifespan)

@app.get("/healthy")
def status():
    return {"status": "Healthy"}

@app.get("/", response_class=HTMLResponse)
def home():
    return "<h1>Still in development, Use Swagger UI for Endpoints</h1>"

@app.post("/predict")
def predict(
    company: str = Form(...),
    type_name: str = Form(...),
    cpu_company: str = Form(...),
    cpu_frequency_ghz: float = Form(...),
    ram_gb: int = Form(...),
    gpu_company: str = Form(...),
    operating_system: str = Form(...),
    gpu_tier: str = Form(...),        
    cpu_tier: str = Form(...),       
    is_premium: int = Form(...),    
    ssd_gb: int = Form(...),
    hdd_gb: int = Form(...),
    flash_storage_gb: int = Form(...)
):
    features = [[
        company, type_name, cpu_company, cpu_frequency_ghz, ram_gb,
        gpu_company, operating_system, gpu_tier, cpu_tier,
        is_premium, ssd_gb, hdd_gb, flash_storage_gb
    ]]

    prediction = model.predict(features)
    return {"Laptop Price is approx": prediction.tolist()}

# if __name__ == "__main__":
#     uvicorn.run(host="0.0.0.0",port=5000,app=app)