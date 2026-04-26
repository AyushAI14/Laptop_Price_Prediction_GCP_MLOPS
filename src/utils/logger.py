from src.constants import *
import logging
import sys
import os

log_dir = os.path.join(os.getcwd(),'Logs',TIMESTAMPS)
os.makedirs(log_dir,exist_ok=True)

log_file = os.path.join(log_dir,LOG_FILENAME)

logging.basicConfig(
    level=logging.INFO,
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler(log_file)
    ],
    format="[ %(asctime)s ] %(lineno)d %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger() 
# if __name__=="__main__":
#     logger = logging.getLogger()  # this is making unable to load logger as module level