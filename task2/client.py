from typing import List

import requests

API_URL = "https://ru.wikipedia.org/w/api.php"


def fetch_animal_titles(limit_per_request: int = 500) -> List[str]:
    """
    Загружает все страницы из категории «Животные по алфавиту»
    и возвращает список их заголовков.
    """

    session = requests.Session()
    titles: List[str] = []

    params = {
        "action": "query",
        "format": "json",
        "list": "categorymembers",
        "cmtitle": "Категория:Животные_по_алфавиту",
        "cmlimit": limit_per_request,
        "cmnamespace": 0,  # только статьи (без подкатегорий, файлов и пр.)
    }

    while True:
        # В случае сетевых проблем бросим исключение requests, пусть вылетит наружу.
        resp = session.get(API_URL, params=params, timeout=30)
        resp.raise_for_status()
        data = resp.json()

        members = data.get("query", {}).get("categorymembers", [])
        titles.extend(member["title"] for member in members)

        # Продолжаем постранично вытягивать, пока не исчезнет cmcontinue
        if "continue" in data:
            params.update(data["continue"])
        else:
            break

    return titles
