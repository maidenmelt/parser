import json
import logging
from pathlib import Path
from datetime import datetime
from src.config import settings


def get_logger(name, log_file=None):
    if log_file is None:
        log_file = name.replace("src.", "").replace(".", "_") + ".log"

    log_path = settings.LOGS_DIR / log_file
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    if logger.handlers:
        return logger

    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    file_handler = logging.FileHandler(log_path, encoding="utf-8")
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    return logger


def read_file(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()


def load_json(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_json(data, file_path):
    file_path.parent.mkdir(parents=True, exist_ok=True)
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def get_timestamp():
    return datetime.now().isoformat()


def cut_text(text, max_len=100):
    if len(text) <= max_len:
        return text
    return text[:max_len] + "..."