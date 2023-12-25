import logging

logger = logging.getLogger(__name__)
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] - %(message)s"))
logger.setLevel(logging.INFO)
logger.addHandler(handler)
