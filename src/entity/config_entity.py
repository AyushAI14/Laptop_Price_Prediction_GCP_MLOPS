from dataclasses import dataclass
import os
from src.constants import *


@dataclass
class DataIngestionConfig:
        data_ingestion_artifacts_dir: str = os.path.join(
            ARTIFACTS_DIR, DATA_INGESTION_ARTIFACTS_DIR
        )
        gcp_data_file_path: str = os.path.join(
            data_ingestion_artifacts_dir, GCP_DATA_FILE_NAME
        )
        gcp_bucket_name: str = GCP_BUCKET_NAME
        gcp_bucket_uri: str = GCP_BUCKET_URI
        gcp_bucket_blob: str = GCP_BLOB_NAME

@dataclass
class DataTransformationConfig:
    data_transformation_artifacts_dir: str = os.path.join(
        ARTIFACTS_DIR, DATA_TRANSFORMATION_ARTIFACTS_DIR
    )
    transformes_data_file_path: str = os.path.join(
        data_transformation_artifacts_dir, PROCESS_DATA_FILE_NAME
    )
    eda_store_path: str = os.path.join(
        data_transformation_artifacts_dir, EDA
    )
    gcp_bucket_blob_processed: str = GCP_PROCESSED_BLOB_NAME

@dataclass
class ModelTrainingConfig:
        model_training_artifacts_dir: str = os.path.join(
            ARTIFACTS_DIR, MODEL_TRAINING_ARTIFACTS_DIR
        )
        model_training_file_path: str = os.path.join(
            model_training_artifacts_dir, MODEL_PATH
        )
        train_data = os.path.join(model_training_artifacts_dir,TRAIN_DF)
        test_data = os.path.join(model_training_artifacts_dir,TEST_DF)
        train_data_gcp=TRAIN_DF
        test_data_gcp=TEST_DF
        model_gcp=MODEL_PATH


@dataclass
class ModelEvaluationConfig:
        model_evaluation_artifacts_dir: str = os.path.join(
            ARTIFACTS_DIR, MODEL_EVALUATION_ARTIFACTS_DIR
        )
        EVAL_REPORT = os.path.join(model_evaluation_artifacts_dir,EVAL_REPORT)

@dataclass
class ModelPusherConfig:
    pass