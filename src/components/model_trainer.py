import os
from src.entity.config_entity import *
import pandas as pd
from src.utils.logger import logger
from src.utils.helpers import *
from src.utils.gcp_utils import *
from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder,OrdinalEncoder
from sklearn.preprocessing import StandardScaler
import joblib as jb
from gcp.monitoring.logging_config import gcp_logger
from sklearn.linear_model import Ridge
from sklearn.ensemble import RandomForestRegressor,GradientBoostingRegressor,StackingRegressor
from xgboost import XGBRegressor

class ModelTraining:
    def __init__(self):
        
        create_file_folder(ModelTrainingConfig.model_training_file_path)

    def traintestsplit(self):
        logger.info('Loading transformed data ')
        gcp_logger("event=LOAD_DATA stage=training component=model_training")
        df= pd.read_csv(DataTransformationConfig.transformes_data_file_path)
        logger.info('Traing test split start')
        gcp_logger("event=TRAIN_TEST_SPLIT_START stage=training component=model_training")
        
        train_df,test_df = train_test_split(df,test_size=0.15,random_state=2)

        train_df.to_csv(ModelTrainingConfig.train_data)
        test_df.to_csv(ModelTrainingConfig.test_data)
        logger.info(f"Train test data save to {ModelTrainingConfig.train_data}")
        gcp_logger("event=SAVE_SPLIT_DATA stage=training component=model_training status=success")
        logger.info("Uploading Processed data to GCP ")
        gcp_logger("event=UPLOAD_SPLIT_DATA_START stage=training component=model_training")
        upload_blob(DataIngestionConfig.gcp_bucket_name,ModelTrainingConfig.train_data_gcp,ModelTrainingConfig.train_data)
        upload_blob(DataIngestionConfig.gcp_bucket_name,ModelTrainingConfig.test_data_gcp,ModelTrainingConfig.test_data)
        logger.info("train test split data on GCP Successfully Uploaded")
        gcp_logger("event=UPLOAD_SPLIT_DATA_COMPLETE stage=training component=model_training status=success")

    def model_training(self):
        """
        This function train stacked regessor model and push the model to gcp storage bucket
        """
        df= pd.read_csv(ModelTrainingConfig.train_data)
        X_train = df.drop(columns =['Price (Inr)','Unnamed: 0.1','Unnamed: 0'])
        y_train = df['Price (Inr)']

        step1 = ColumnTransformer(
        transformers=[
            ('scaler',StandardScaler(),[3,4,9,10,11,12]),
            ('OneHotEncd',OneHotEncoder(drop='first'),[1,2,5,6]),
            ('OrdinalEncod',OrdinalEncoder(),[0,7,8]),
        ],remainder='passthrough'
        )
        estimators = [
            ('rf', RandomForestRegressor(n_estimators=350,random_state=3,max_samples=0.5,max_features=0.75,max_depth=15)),
            ('gbdt',GradientBoostingRegressor(n_estimators=100,max_features=0.5)),
            ('xgb', XGBRegressor(n_estimators=25,learning_rate=0.3,max_depth=5))
        ]

        step2 = StackingRegressor(estimators=estimators, final_estimator=Ridge(alpha=100))
        pipesr = Pipeline(
            [('step1',step1),
            ('step2',step2)]
        )
        logger.info('Model is Fitting')
        gcp_logger("event=MODEL_FIT_START stage=training component=model_training")
        pipesr.fit(X_train,y_train)
        logger.info('Model is Fitting Done Successfully')
        gcp_logger("event=MODEL_FIT_COMPLETE stage=training component=model_training status=success")
        logger.info("Dumping model to gcp and artifact")
        gcp_logger("event=MODEL_DUMP_START stage=training component=model_training")
        jb.dump(pipesr,ModelTrainingConfig.model_training_file_path)
        logger.info("Uploading Model to GCP")
        gcp_logger("event=MODEL_UPLOAD_START stage=training component=model_training")
        upload_blob(DataIngestionConfig.gcp_bucket_name,ModelTrainingConfig.model_gcp,ModelTrainingConfig.model_training_file_path)
        logger.info("Model on GCP Successfully Uploaded")
        gcp_logger("event=MODEL_UPLOAD_COMPLETE stage=training component=model_training status=success")
        logger.info("Mlflow logging is in progress")
        gcp_logger("event=MLFLOW_LOGGING stage=training component=model_training")

if __name__=="__main__":
    demo = ModelTraining()
    demo.traintestsplit()
    demo.model_training()