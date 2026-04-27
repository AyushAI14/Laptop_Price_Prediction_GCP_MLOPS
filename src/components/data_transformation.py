import os
from src.entity.config_entity import *
import pandas as pd
from src.utils.helpers import *
from src.utils.gcp_utils import *
from matplotlib import pyplot as plt
import seaborn as sns
import mlflow
import dagshub
from gcp.monitoring.logging_config import gcp_logger
from src.utils.logger import logger



# dagshub.init(repo_owner='AyushAI14', repo_name='Laptop_Price_Prediction_GCP_MLOPS', mlflow=True)
#  mlflow.set_tracking_uri('https://dagshub.com/AyushAI14/Laptop_Price_Prediction_GCP_MLOPS.mlflow')
# mlflow.set_experiment('Laptop_gcp')

class DataTransformation:
    def __init__(self):
        create_file_folder(DataTransformationConfig.transformes_data_file_path)
        os.makedirs(DataTransformationConfig.eda_store_path,exist_ok=True)
        self.df = pd.read_csv(DataIngestionConfig.gcp_data_file_path)

    def eda(self):

        with mlflow.start_run(run_name="EDA",nested=True):

            # BASIC INFO 
            mlflow.log_param("num_rows", self.df.shape[0])
            mlflow.log_param("num_columns", self.df.shape[1])

            nulls = self.df.isnull().sum().sum()
            duplicates = self.df.duplicated().sum()

            mlflow.log_metric("total_nulls ", int(nulls))
            mlflow.log_metric("total_duplicates", int(duplicates))

            # SAVE SUMMARY
            summary_path = os.path.join(DataTransformationConfig.eda_store_path, "summary.csv")
            self.df.describe().to_csv(summary_path)
            mlflow.log_artifact(summary_path, artifact_path="eda")

            # PLOTS
            sns.set_style("whitegrid")

            # Price distribution
            if 'Price (Euro)' in self.df.columns:
                plt.figure()
                sns.histplot(self.df['Price (Euro)'], kde=True)
                plt.title("Price Distribution (Euro)")

                plot_path = os.path.join(DataTransformationConfig.eda_store_path, "price_dist.png")
                plt.savefig(plot_path)
                mlflow.log_artifact(plot_path, artifact_path="eda/plots")
                plt.close()

            # Categorical plots
            categorical_cols = ['Company', 'OpSys', 'GPU_Company']

            for col in categorical_cols:
                if col in self.df.columns:
                    plt.figure()
                    self.df[col].value_counts().plot(kind='bar')
                    plt.title(f"{col} Distribution")
                    plt.xticks(rotation=45)

                    plot_path = os.path.join(DataTransformationConfig.eda_store_path, f"{col}_dist.png")
                    plt.savefig(plot_path)
                    mlflow.log_artifact(plot_path, artifact_path="eda/plots")
                    plt.close()

            # Company vs Price
            if 'Company' in self.df.columns and 'Price (Inr)' in self.df.columns:
                plt.figure()
                sns.barplot(data=self.df, x="Company", y="Price (Inr)")
                plt.xticks(rotation=45)
                plt.title("Company vs Price")

                plot_path = os.path.join(DataTransformationConfig.eda_store_path, "company_vs_price.png")
                plt.savefig(plot_path)
                mlflow.log_artifact(plot_path, artifact_path="eda/plots")
                plt.close()
            mlflow.log_artifact(__file__)
            logger.info("EDA logged to MLflow")
            gcp_logger("EDA logged to MLflow")
    def featureEngineering(self):
        logger.info("Starting Feature Engineering Process")
        gcp_logger("Starting Feature Engineering Process")
        df = self.df
        df['Price (Inr)'] = df['Price (Euro)']*109.86
        df['GPU_Tier'] = df['GPU_Type'].apply(lambda x:gpu_tier(x))
        df['CPU_Tier'] = df['CPU_Type'].apply(lambda x:cpu_tier(x))
        df['OpSys'] = df['OpSys'].apply(lambda x:os_identifier(x))
        df['Product'] = df['Product'].apply(lambda x:extract_series(x))
        premium = ['MacBook','XPS','ThinkPad','EliteBook','Spectre','Alienware','ROG']
        df['is_premium'] = df['Product'].apply(lambda x: 1 if x in premium else 0)
        df[['SSD','HDD','Flash']] = df['Memory'].apply(lambda x: pd.Series(process_memory(x)))
        df['Company'] = df['Company'].apply(lambda x:pd.Series(other_companies(x)))
        df.drop(columns=['Inches','Weight (kg)','Price (Euro)','CPU_Type','GPU_Type','ScreenResolution','Memory','Product'],inplace=True)
        logger.info("dropped some columns")
        gcp_logger("dropped some columns")
        df.to_csv(DataTransformationConfig.transformes_data_file_path)
        logger.info(f'Saved the process data to {DataTransformationConfig.transformes_data_file_path}')
        gcp_logger("Saved the process data to {DataTransformationConfig.transformes_data_file_path}")
        logger.info(" Feature Engineering Process Successfully Completed")
        gcp_logger("Feature Engineering Process Successfully Completed")
        logger.info("Uploading Processed data to GCP ")
        gcp_logger("Uploading Processed data to GCP ")
        upload_blob(DataIngestionConfig.gcp_bucket_name,DataTransformationConfig.gcp_bucket_blob_processed,DataTransformationConfig.transformes_data_file_path)
        logger.info(" Processed data on GCP Successfully Uploaded")
        gcp_logger(" Processed data on GCP Successfully Uploaded")
        
if __name__=="__main__":
    demo = DataTransformation()
    # demo.eda()
    demo.featureEngineering()
