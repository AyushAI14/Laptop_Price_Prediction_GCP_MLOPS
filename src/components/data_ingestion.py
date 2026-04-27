import os
from src.entity.config_entity import *
import pandas as pd
from src.utils.gcp_utils import download_blob,upload_blob
from src.utils.logger import logger
from src.utils.helpers import *
from gcp.monitoring.logging_config import gcp_logger

class DataIngestion:
    def __init__(self):
        create_file_folder(DataIngestionConfig.gcp_data_file_path)

    def Save_data_from_gcp(self):
        
        logger.info("Starting Data Ingestion from GCP bucket ")
        gcp_logger("Starting Data Ingestion from GCP bucket")
        download_blob(DataIngestionConfig.gcp_bucket_name,DataIngestionConfig.gcp_bucket_blob,DataIngestionConfig.gcp_data_file_path)
        logger.info("Data Ingestion from GCP bucket is Successfully completed")
        gcp_logger("Data Ingestion from GCP bucket is Successfully completed")

    # def Upload_data_to_gcp(self):
    #     logger.info("Starting uploading file to GCP bucket")
    #     upload_blob(DataIngestionConfig.gcp_bucket_name,DataTransformationConfig.gcp_bucket_blob_processed,DataIngestionConfig.gcp_data_file_path)
    #     nlogger.info("Uploading file to GCP bucket is Successfully completed")

if __name__=="__main__":
    demo = DataIngestion()
    demo.Save_data_from_gcp()
    # demo.Upload_data_to_gcp()