import json
from src.client import send_message
from src.utils import load_json, read_file, save_json, get_logger
from src.config import settings
from .parser import get_page, parse_movie

logger = get_logger(__name__)

def analyze_movie(url):
    html = get_page(url)
    raw_data = parse_movie(html)
    
    if not raw_data:
        logger.error("Не удалось спарсить страницу")
        return None
    
    system_prompt = read_file(settings.PROMPTS_DIR / "movie_prompt.txt")
    schema = load_json(settings.SCHEMAS_DIR / "movie_schema.json")
    
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": f"Структурируй данные о фильме:\n{json.dumps(raw_data, ensure_ascii=False)}"}
    ]
    
    result = send_message(messages, schema)
    
    return result

if __name__ == "__main__":
    url = "https://kinogo.ec/13411--velikaja-krasota.html"
    result = analyze_movie(url)
    if result:
        print(json.dumps(result, indent=2, ensure_ascii=False))
        from src.config import settings
        save_json(result, settings.RESULTS_DIR / "movie_structured.json")