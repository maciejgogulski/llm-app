import logging
import os

def setup_logging():
    level = os.getenv('LOGGING_LEVEL', 'INFO')
    logging.basicConfig(
        level=getattr(logging, level),
        format='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
        handlers=[logging.StreamHandler()]  # Log to stdout
    )
