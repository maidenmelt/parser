import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

class Settings:
    LLAMA_API_URL: str = os.getenv("LLAMA_API_URL", "http://127.0.0.1:10000/v1/chat/completions")
    API_KEY: str = os.getenv("LLAMA_API_KEY", "12345")
    REQUEST_TIMEOUT: int = 200

    DATA_DIR: Path = BASE_DIR / "data"
    RESULTS_DIR: Path = BASE_DIR / "results"
    SCHEMAS_DIR: Path = BASE_DIR / "schemas"
    PROMPTS_DIR: Path = BASE_DIR / "prompts"
    LOGS_DIR: Path = BASE_DIR / "logs"

    INPUT_FILE: str = "investfuture_last100.json"
    OUTPUT_FILE: str = "results_analyzed.json"
    SCHEMA_FILE: str = "movie_schema.json"
    PROMPT_FILE: str = "movie_prompt.txt"

    TEMPERATURE: float = 0.3
    TOP_K: int = 20
    TOP_P: float = 0.95

    MAX_RETRIES: int = 5
    RETRY_DELAY: int = 2

settings = Settings()

for dir_path in [
    settings.DATA_DIR,
    settings.RESULTS_DIR,
    settings.SCHEMAS_DIR,
    settings.PROMPTS_DIR,
    settings.LOGS_DIR
]:
    dir_path.mkdir(parents=True, exist_ok=True)