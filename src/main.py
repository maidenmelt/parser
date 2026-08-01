from parser import get_page, parse_movie, save_result

def main():
    url = 'https://kinogo.ec/13411--velikaja-krasota.html'
    
    html = get_page(url)
    if not html:
        print("Не удалось загрузить страницу")
        return
    
    data = parse_movie(html)
    if data:
        print("Данные о фильме:")
        for key, value in data.items():
            print(f"{key}: {value}")
        save_result(data)
    else:
        print("Не удалось распарсить страницу")

if __name__ == '__main__':
    main()