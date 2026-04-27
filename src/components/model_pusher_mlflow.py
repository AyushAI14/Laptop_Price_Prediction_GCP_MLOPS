import pandas as pd
import mlflow
import mlflow.sklearn

from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, OrdinalEncoder, StandardScaler

from sklearn.linear_model import Ridge
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor, StackingRegressor
from xgboost import XGBRegressor

from src.entity.config_entity import *
from src.utils.logger import logger
import dagshub
import warnings
from gcp.monitoring.logging_config import gcp_logger

warnings.filterwarnings("ignore")

# dagshub.init(repo_owner='AyushAI14', repo_name='Laptop_Price_Prediction_GCP_MLOPS', mlflow=True)
# mlflow.set_tracking_uri('https://dagshub.com/AyushAI14/Laptop_Price_Prediction_GCP_MLOPS.mlflow')
# mlflow.set_experiment('Laptop_gcp')



class ModelPusher:

    def model_training(self):
        with mlflow.start_run(run_name="stacking_experiment",nested=True):

            # LOAD DATA 
            df = pd.read_csv(ModelTrainingConfig.train_data)
            test_df = pd.read_csv(ModelTrainingConfig.test_data)

            X_train = df.drop(columns=['Price (Inr)', 'Unnamed: 0', 'Unnamed: 0.1'])
            y_train = df['Price (Inr)']

            # X_test = test_df.drop(columns=['Price (Inr)', 'Unnamed: 0', 'Unnamed: 0.1'])
            # y_test = test_df['Price (Inr)']
            train_dataset = mlflow.data.from_pandas(df, source=ModelTrainingConfig.train_data, name="training-data")
            test_dataset = mlflow.data.from_pandas(test_df, source=ModelTrainingConfig.test_data, name="training-data")

            mlflow.log_input(train_dataset,"train_df")
            mlflow.log_input(test_dataset,"test_df")


            # PREPROCESSOR 
            preprocessor = ColumnTransformer(
                transformers=[
                    ('num', StandardScaler(), [3,4,9,10,11,12]),
                    ('ohe', OneHotEncoder(drop='first'), [1,2,5,6]),
                    ('ord', OrdinalEncoder(), [0,7,8]),
                ],
                remainder='passthrough'
            )

            # MODELS 
            rf = RandomForestRegressor(n_estimators=350, random_state=3,
                                      max_samples=0.5, max_features=0.75, max_depth=15)

            gbdt = GradientBoostingRegressor(n_estimators=100, max_features=0.5)
            xgb = XGBRegressor(n_estimators=25, learning_rate=0.3, max_depth=5)

            stack = StackingRegressor(
                estimators=[('rf', rf), ('gbdt', gbdt), ('xgb', xgb)],
                final_estimator=Ridge(alpha=100)
            )

            pipeline = Pipeline([
                ('preprocessor', preprocessor),
                ('model', stack)
            ])

            # TRAIN 
            logger.info("Training model...")
            pipeline.fit(X_train, y_train)

            # LOGGING 
            mlflow.log_param("model", "stacking")

            mlflow.log_param("rf_n_estimators", 350)
            mlflow.log_param("rf_random_state", 3)
            mlflow.log_param("rf_max_samples", 0.5)
            mlflow.log_param("rf_max_features", 0.7)
            mlflow.log_param("rf_max_depth", 15)

            mlflow.log_param("xgb_n_estimators", 25)
            mlflow.log_param("xgb_learning_rate", 0.3)
            mlflow.log_param("xgb_max_depth", 5)

            mlflow.log_param("gb_n_estimators",100)
            mlflow.log_param("gb_max_features", 0.5)


            mlflow.set_tag("stage", "experiment")
            mlflow.set_tag("model_type", "stacking")

            mlflow.sklearn.log_model(
                sk_model=pipeline,
                artifact_path="model",
                input_example=X_train.head(3)
            )

            logger.info("MLflow logging completed.")
            gcp_logger("MLflow logging completed.")


if __name__=="__main__":
    demo = ModelPusher()
    demo.model_training()