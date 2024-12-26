from utils import get_logger


logger = get_logger(__name__)


class GPRCClient:

    def __init__(self, *args, **kwargs):
        if "user_id" in kwargs:
            self.user_id = kwargs["user_id"]

    def send_url(self, url: str) -> str:
        logger.info(f"URL: {url}")
        return "DATA Bill"