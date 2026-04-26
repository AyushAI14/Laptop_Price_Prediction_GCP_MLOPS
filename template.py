import os
from pathlib import Path


# List of files to be created
list_of_files = [
    f"./README.md",
    f"./requirements.txt",
    f"./.env",
    f"./.gitignore",
    f"./Dockerfile",
    f"./Makefile",

    # Configs
    f"./configs/config.yaml",
    f"./configs/params.yaml",
    f"./configs/gcp_config.yaml",

    # Artifacts
    f"./artifacts/.gitkeep",

    # # Notebooks
    # f"/notebooks/eda.ipynb",

    # Core src
    f"./src/__init__.py",

    f"./src/constants/__init__.py",
    f"./src/constants/constants.py",

    f"./src/utils/__init__.py",
    f"./src/utils/logger.py",
    f"./src/utils/helpers.py",
    f"./src/utils/gcp_utils.py",

    f"./src/entity/__init__.py",
    f"./src/entity/config_entity.py",
    f"./src/entity/artifact_entity.py",

    f"./src/components/__init__.py",
    f"./src/components/data_ingestion.py",
    f"./src/components/data_validation.py",
    f"./src/components/data_transformation.py",
    f"./src/components/model_trainer.py",
    f"./src/components/model_evaluation.py",
    f"./src/components/model_pusher.py",

    f"./src/pipelines/__init__.py",
    f"./src/pipelines/training_pipeline.py",
    f"./src/pipelines/batch_prediction_pipeline.py",

    f"./src/mlflow_tracking/__init__.py",
    f"./src/mlflow_tracking/mlflow_logger.py",

    # GCP layer
    f"./gcp/pipelines/pipeline_definition.py",
    f"./gcp/pipelines/pipeline_runner.py",

    # KFP components
    f"./gcp/pipelines/components/data_ingestion/component.py",
    f"./gcp/pipelines/components/data_ingestion/Dockerfile",

    f"./gcp/pipelines/components/preprocessing/component.py",
    f"./gcp/pipelines/components/preprocessing/Dockerfile",

    f"./gcp/pipelines/components/training/component.py",
    f"./gcp/pipelines/components/training/Dockerfile",

    f"./gcp/pipelines/components/evaluation/component.py",
    f"./gcp/pipelines/components/evaluation/Dockerfile",

    f"./gcp/pipelines/components/deployment/component.py",
    f"./gcp/pipelines/components/deployment/Dockerfile",

    # Training
    f"./gcp/training/trainer/train.py",
    f"./gcp/training/trainer/model.py",
    f"./gcp/training/Dockerfile",

    # Deployment
    f"./gcp/deployment/vertex_endpoint.py",
    f"./gcp/deployment/cloud_run/app.py",
    f"./gcp/deployment/cloud_run/predictor.py",
    f"./gcp/deployment/cloud_run/Dockerfile",

    # Monitoring
    f"./gcp/monitoring/drift_detection.py",
    f"./gcp/monitoring/logging_config.py",
    f"./gcp/monitoring/metrics_config.py",

    # Pub/Sub
    f"./gcp/pubsub/triggers.py",

    # Scripts
    f"./scripts/upload_to_gcs.sh",
    f"./scripts/run_pipeline.sh",
    f"./scripts/deploy_vertex.sh",
    f"./scripts/deploy_cloud_run.sh",

    # Tests
    f"./tests/test_data_pipeline.py",
    f"./tests/test_model.py",
    f"./tests/test_api.py",

    # CI/CD
    f"./.github/workflows/ci_cd.yaml",
    f"./cloudbuild.yaml",
]


for file_path in list_of_files:
    file_path = Path(file_path)
    file_dir,filename = os.path.split(file_path)
    if file_path.parent != Path("."):
        os.makedirs(file_path.parent, exist_ok=True)
    if (not os.path.exists(file_path)) or (os.path.getsize(file_path)==0):
        with open(file_path,'w') as f:
            f.write("")
        print(f"{file_path} Created Successfully !")
    else:
        print(f"file exist at {file_path}")