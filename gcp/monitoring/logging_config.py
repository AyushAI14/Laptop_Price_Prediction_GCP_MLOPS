from google.cloud import logging
from google.cloud.logging_v2.resource import Resource

logging_client = logging.Client()
log_name = "ml-pipeline"
logger = logging_client.logger(log_name)

res = Resource(
    type="cloud_run_revision",
    labels={
        "service_name": "laptop-service",
        "location": "asia-south1"
    }
)

def gcp_logger(message,severity='INFO',**kwargs):
    logger.log_struct(
        {
            "message":message,
            **kwargs
        },
        severity=severity,
        resource=res
    )

# def gcp_logger(message):
#     logger.log_text(message)