import os
from src.entity.config_entity import *
import pandas as pd
from src.utils.logger import logger
from src.utils.helpers import *
from src.utils.gcp_utils import *
import dagshub
import warnings
import mlflow
import joblib as jb
from sklearn.metrics import r2_score,mean_absolute_error
warnings.filterwarnings("ignore")

dagshub.init(repo_owner='AyushAI14', repo_name='Laptop_Price_Prediction_GCP_MLOPS', mlflow=True)
mlflow.set_tracking_uri('https://dagshub.com/AyushAI14/Laptop_Price_Prediction_GCP_MLOPS.mlflow')
mlflow.set_experiment('Laptop_gcp')

class ModelEvaluation:
    def __init__(self):
        create_file_folder(ModelEvaluationConfig.EVAL_REPORT)
        self.test_df = pd.read_csv(ModelTrainingConfig.test_data)
        self.model = jb.load(ModelTrainingConfig.model_training_file_path)

    
    def evaluation(self):
        with mlflow.start_run(run_name='evaluation'):
            df = self.test_df
            X_test,y_test =  df.drop(columns =['Price (Inr)','Unnamed: 0.1','Unnamed: 0']),df['Price (Inr)']
            pipesr =  self.model
            y_pred = pipesr.predict(X_test)
            print(y_pred[:5])
            print('R2 score',r2_score(y_test,y_pred))
            print('MAE',mean_absolute_error(y_test,y_pred))
            srr2 = r2_score(y_test,y_pred)
            mlflow.log_metric('r2_score',srr2)
            srmae = mean_absolute_error(y_test,y_pred)
            mlflow.log_metric('mean_absolute_error',srmae)
            
            with open(ModelEvaluationConfig.EVAL_REPORT,'w') as f:
                f.write(f'StackingRegressor regression : r2score {srr2} , mae {srmae}')
            logger.info(f"Evaluation metric file is saved here{ModelEvaluationConfig.EVAL_REPORT}")


if __name__=="__main__":
    demo=ModelEvaluation()
    demo.evaluation()