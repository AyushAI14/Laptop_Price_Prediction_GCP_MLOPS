from google.cloud import logging


def gcp_logger(message):
    logging_client = logging.Client()
    log_name = "my-log"
    logger = logging_client.logger(log_name)
    logger.log_text(message)