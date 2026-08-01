import json
import logging
import time
import requests
from bs4 import BeautifulSoup

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def get_page(url):
    session = requests.Session()
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
        'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
        'Referer': 'https://www.google.com/',
        'Upgrade-Insecure-Requests': '1',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-User': '?1',
        'Cache-Control': 'max-age=0',
    }
    
    session.headers.update(headers)
    
    logger.info(f"Загружаем: {url}")
    
    try:
        response = session.get(url, timeout=30)
        
        # Cloudflare проверка
        if 'Just a moment' in response.text:
            logger.warning("Cloudflare, пробуем ещё раз...")
            time.sleep(3)
            response = session.get(url, timeout=30)
        
        with open('debug_page.html', 'w', encoding='utf-8') as f:
            f.write(response.text)
        logger.info(f"Загружено, длина: {len(response.text)}")
        
        response.raise_for_status()
        return response.text
    
    except Exception as e:
        logger.error(f"Ошибка: {e}")
        return None


def parse_movie(html):
    if not html:
        return None
    
    if 'Just a moment' in html:
        logger.error("Страница заблокирована Cloudflare")
        return None
    
    soup = BeautifulSoup(html, 'html.parser')
    
    # Название
    title_tag = soup.find('h1')
    title = title_tag.text.strip() if title_tag else None
    
    if not title:
        logger.error("Не удалось найти название")
        return None
    
    logger.info(f"Название: {title}")
    
    # Рейтинги
    rating_kp = None
    rating_imdb = None
    
    rates_div = soup.find('div', class_='rates')
    if rates_div:
        for rate in rates_div.find_all('div', class_='rate'):
            text = rate.text.strip()
            if 'КП:' in text:
                rating_kp = text.replace('КП:', '').strip()
            elif 'ИМДб:' in text:
                rating_imdb = text.replace('ИМДб:', '').strip()
    
    # Год
    year_tag = soup.find('b', string='Вышел в:')
    if year_tag:
        year = year_tag.find_next('a')
        year = year.text.strip() if year else None
    else:
        year = None
    
    # Страна
    country_tag = soup.find('b', string='Сняли в:')
    if country_tag:
        country = country_tag.find_next('a')
        country = country.text.strip() if country else None
    else:
        country = None
    
    # Длительность
    duration_tag = soup.find('b', string='Длительность:')
    if duration_tag:
        duration = duration_tag.next_sibling
        duration = duration.strip() if duration else None
    else:
        duration = None
    
    # Описание
    desc_block = soup.find('div', class_='description__block')
    if desc_block:
        desc_div = desc_block.find('div')
        description = desc_div.text.strip() if desc_div else None
    else:
        description = None
    
    return {
        'title': title,
        'rating_kp': rating_kp,
        'rating_imdb': rating_imdb,
        'year': year,
        'country': country,
        'duration': duration,
        'description': description,
    }


def save_result(data):
    with open('movie_data.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    logger.info("Результат сохранён в movie_data.json")