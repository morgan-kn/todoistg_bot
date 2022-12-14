import logging

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
    filename="logs.log"
)
logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler())