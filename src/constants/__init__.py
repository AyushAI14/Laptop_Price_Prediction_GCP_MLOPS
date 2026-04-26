import os
from datetime import datetime

TIMESTAMPS = datetime.now().strftime("%d/%m/%Y-%H:%M:%S")
LOG_FILENAME = 'logs.log'

ARTIFACTS_DIR = 'artifacts'
DATA_INGESTION_ARTIFACTS_DIR = 'DataIngestionArtifacts'
GCP_DATA_FILE_NAME='gcp_bucket_laptop.csv'

DATA_TRANSFORMATION_ARTIFACTS_DIR = 'DataTransformationArtifacts'
PROCESS_DATA_FILE_NAME = 'processed_laptop.csv'
MODEL_TRAINING_ARTIFACTS_DIR = 'ModelTrainingArtifacts'
MODEL_EVALUATION_ARTIFACTS_DIR = 'ModelEvaluationArtifacts'

MODEL_PATH = 'v1_stacked_model.pkl'
GCP_BUCKET_NAME='laptop_dataset_gcp_bucket'
GCP_BUCKET_URI='gs://laptop_dataset_gcp_bucket/laptop_price - dataset.csv'
GCP_BLOB_NAME='laptop_price - dataset.csv'
GCP_PROCESSED_BLOB_NAME='laptop_price_dataset_processed.csv'
EDA='eda'
TRAIN_DF= 'train_df.csv'
TEST_DF= 'test_df.csv'
EVAL_REPORT= "eval_report.txt"