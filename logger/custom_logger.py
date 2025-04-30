import logging
import os

# Ensure logs directory exists
log_dir = os.path.join(os.path.dirname(__file__), '..', 'logs')
os.makedirs(log_dir, exist_ok=True)

log_file = os.path.join(log_dir, "run_log.txt")

logging.basicConfig(
    filename=log_file,
    level=logging.INFO,
    format='[%(asctime)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

def log_event(message):
    logging.info(message)
