import json
import httpx
from src.config import settings

try:
    from src.utils import get_logger
    logger = get_logger(__name__)
except ImportError:
    import logging
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)


class ModelClient:
    def __init__(self):
        self.api_url = settings.LLAMA_API_URL
        self.api_key = settings.API_KEY
        self.timeout = settings.REQUEST_TIMEOUT

        self.client = httpx.Client(
            timeout=self.timeout,
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.api_key}"
            }
        )

    def ask(self, messages, schema=None, temperature=None, top_p=None, top_k=None):
        if temperature is None:
            temperature = settings.TEMPERATURE
        if top_p is None:
            top_p = settings.TOP_P
        if top_k is None:
            top_k = settings.TOP_K

        payload = {
            "model": "llama",
            "messages": messages,
            "temperature": temperature,
            "top_p": top_p,
            "top_k": top_k,
            "stream": False
        }

        if schema:
            payload["response_format"] = {
                "type": "json_schema",
                "json_schema": schema
            }

        try:
            response = self.client.post(self.api_url, json=payload)
            response.raise_for_status()

            data = response.json()
            content = data["choices"][0]["message"]["content"]

            try:
                result = json.loads(content)
            except json.JSONDecodeError:
                result = {"raw_output": content}

            return result

        except Exception as e:
            logger.error(f"Ошибка: {e}")
            raise

    def close(self):
        self.client.close()


def send_message(messages, schema=None):
    client = ModelClient()
    try:
        return client.ask(messages, schema)
    finally:
        client.close()