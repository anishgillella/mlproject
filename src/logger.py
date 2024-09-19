import logging
import os
from datetime import datetime

# Generate a log file name based on the current date and time
LOG_FILE = f"{datetime.now().strftime('%m-%d_%Y_%H_%M_%S')}.log"

# Define the directory where log files will be stored
log_dir = os.path.join(os.getcwd(), "logs")

# Create the log directory if it doesn't already exist
os.makedirs(log_dir, exist_ok=True)

# Define the full path to the log file
LOG_FILE_PATH = os.path.join(log_dir, LOG_FILE)

# Configure the logging settings
logging.basicConfig(
    filename=LOG_FILE_PATH,  # Log messages will be written to this file
    format='%(asctime)s - %(levelname)s - %(message)s',  # Define the format of log messages
    level=logging.INFO,  # Set the logging level to INFO
)

# Example usage: logging.info("Logging has started")
