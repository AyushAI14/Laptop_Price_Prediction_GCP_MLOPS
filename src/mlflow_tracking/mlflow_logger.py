import mlflow
import dagshub
from src.components.data_transformation import DataTransformation
from src.components.model_evaluation import ModelEvaluation
from src.components.model_pusher_mlflow import ModelPusher
from gcp.monitoring.logging_config import gcp_logger
from src.utils.logger import logger


dagshub.init(repo_owner='AyushAI14', repo_name='Laptop_Price_Prediction_GCP_MLOPS', mlflow=True)
mlflow.set_tracking_uri('https://dagshub.com/AyushAI14/Laptop_Price_Prediction_GCP_MLOPS.mlflow')
mlflow.set_experiment('Laptop_gcp')

tranformation = DataTransformation()
training = ModelPusher()
evaluation = ModelEvaluation()

def run_stage(stage_name, func):
    with mlflow.start_run(run_name=stage_name, nested=True):
        func()


def run_pipeline():
    with mlflow.start_run(run_name="pipeline_main"):
        run_stage("data_transformation", tranformation.eda)
        run_stage("model_training", training.model_training)
        run_stage("model_evaluation", evaluation.evaluation)


if __name__ == "__main__":
    logger.info("Mlflow Experiemnt Tracking Start")
    gcp_logger("Mlflow Experiemnt Tracking Start")
    run_pipeline()
    gcp_logger("Mlflow Experiemnt Tracking Sucessfully Executed")
    logger.info("Mlflow Experiemnt Tracking Sucessfully Executed")

