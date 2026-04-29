# Laptop Price Prediction MLOps Project on GCP

This repository contains an end-to-end MLOps project for predicting laptop prices using a Stacking Regressor model. The project is designed with a robust architecture that leverages Google Cloud Platform (GCP) for storage, deployment, and monitoring, while using industry-standard tools for data versioning and experiment tracking.

## Project Overview

The goal of this project is to build a scalable and production-ready machine learning pipeline that predicts the price of a laptop based on its specifications (e.g., RAM, CPU, GPU, OS, etc.). 

### Key Features:
- **Data Ingestion:** Automated data retrieval from Google Cloud Storage (GCS).
- **Data Transformation:** Comprehensive preprocessing and feature engineering.
- **Model Training:** Advanced stacking ensemble model combining Random Forest, Gradient Boosting, and XGBoost.
- **Experiment Tracking:** Integration with **MLflow** and **DagsHub** for tracking parameters, metrics, and models.
- **Data Versioning:** Managed via **DVC** to ensure reproducibility.
- **Deployment:** Containerized deployment using **FastAPI** and **Google Cloud Run**.
- **Monitoring:** Centralized logging and monitoring using **GCP Cloud Logging** and **Monitoring**.
- **CI/CD:** Automated testing and deployment pipelines via **GitHub Actions** and **Google Cloud Build**.

---

## Architecture

The project follows a modular architecture:
1.  **Data Layer:** Data is stored in GCS and versioned using DVC.
2.  **Pipeline Layer:** Modular components for ingestion, transformation, training, evaluation, and pushing.
3.  **Tracking Layer:** MLflow (hosted on DagsHub) tracks all experiments and model versions.
4.  **Serving Layer:** FastAPI provides an endpoint for real-time predictions, hosted on Cloud Run.
5.  **Monitoring Layer:** Custom GCP loggers track pipeline events and performance.

---

## Project Structure

```text
├── .github/workflows/       # GitHub Actions for CI/CD
├── artifacts/               # Local storage for intermediate data and models
├── gcp/                     # GCP-specific deployment and monitoring logic
│   ├── deployment/          # Cloud Run and Vertex AI deployment scripts
│   ├── monitoring/          # GCP Logging and Monitoring configuration
│   └── pipelines/           # GCP Pipeline definitions (KFP)
├── notebook/                # Jupyter notebooks for EDA and experimentation
├── scripts/                 # Utility shell scripts (GCS upload, deployment)
├── src/                     # Core project source code
│   ├── components/          # ML pipeline stages (Ingestion, Trainer, etc.)
│   ├── entity/              # Configuration and artifact entities
│   ├── mlflow_tracking/     # MLflow integration logic
│   ├── pipelines/           # Local training and prediction pipelines
│   └── utils/               # Common utility functions (GCP, logging, etc.)
├── cloudbuild.yaml          # Google Cloud Build configuration
├── Dockerfile               # Containerization for deployment
├── dvc.yaml                 # DVC pipeline definition
└── requirements.txt         # Python dependencies
```

---

## Tech Stack

- **Languages:** Python 3.12+
- **Libraries:** Pandas, NumPy, Scikit-learn, XGBoost, Joblib
- **Web Framework:** FastAPI, Uvicorn
- **MLOps:** DVC, MLflow, DagsHub
- **Cloud (GCP):** Cloud Storage, Cloud Run, Vertex AI, Cloud Build, Cloud Logging
- **DevOps:** Docker, GitHub Actions

---

## Getting Started

### 1. Clone the repository
```bash
git clone https://github.com/AyushAI14/Laptop_Price_Prediction_GCP_MLOPS.git
cd Laptop_Price_Prediction_GCP_MLOPS
```

### 2. Set up Virtual Environment
```bash
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
uv pip install -r requirements.txt
```

### 3. GCP Configuration
Ensure you have the Google Cloud CLI installed and authenticated:
```bash
gcloud auth login
gcloud auth application-default login
```
Set your environment variables in a `.env` file (refer to `src/constants/__init__.py` for bucket names).

---

## MLOps Workflow

### Data Versioning (DVC)
Data is stored in GCS and tracked via DVC.
```bash
dvc pull
```

### Experiment Tracking (MLflow)
Experiments are logged to DagsHub. You can view the dashboard at:
`https://dagshub.com/AyushAI14/Laptop_Price_Prediction_GCP_MLOPS.mlflow`

Run the tracking pipeline:
```bash
python src/mlflow_tracking/mlflow_logger.py
```

### Training Pipeline
Execute the full pipeline locally:
```bash
python main.py
```

---

## Deployment

### Cloud Run (FastAPI)
The application is containerized and can be deployed to Cloud Run using:
```bash
bash scripts/deploy_cloud_run.sh
```
Access the API documentation at `https://<your-cloud-run-url>/docs`.

---

## Monitoring & Logging

The project uses custom log handlers to send events to **GCP Cloud Logging**. You can monitor pipeline stages, errors, and performance metrics directly in the GCP Console.

---

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
