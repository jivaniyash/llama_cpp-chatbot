import logging
from datetime import datetime
import os

# Create logs directory if it does not exist
logging_path = "./logs"
if not os.path.exists(logging_path):
    os.makedirs(logging_path)

# Configure logging
log_filename = os.path.join(logging_path, f"logs-{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.log")
logging.basicConfig(
    filename=log_filename,
    filemode="a",
    format='%(asctime)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

