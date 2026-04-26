#!/bin/bash

PROJECT_ID="project-8b78e65a-e0ab-408d-ad5"
SERVICE_NAME="laptopml"
REGION="asia-south1"
TAG="latest"

# Build and push image
gcloud builds submit --tag gcr.io/$PROJECT_ID/$SERVICE_NAME
# docker buildx build -t gcr.io/$PROJECT_ID/$SERVICE_NAME:$TAG --platform linux/amd64

# Deploy to Cloud Run
gcloud run deploy $SERVICE_NAME \
  --image gcr.io/$PROJECT_ID/$SERVICE_NAME \
  --platform managed \
  --region $REGION \
  --allow-unauthenticated