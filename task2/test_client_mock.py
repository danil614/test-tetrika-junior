from unittest.mock import patch

from task2.client import fetch_animal_titles

# Заготовка фрагментов, которые отдаст MediaWiki-API
FIRST_PAGE = {
    "batchcomplete": "",
    "continue": {"cmcontinue": "page|next|1", "continue": "-||"},
    "query": {
        "categorymembers": [
            {"pageid": 1, "ns": 0, "title": "Акула"},
            {"pageid": 2, "ns": 0, "title": "Бобр"},
        ]
    },
}
SECOND_PAGE = {
    "batchcomplete": "",
    "query": {
        "categorymembers": [
            {"pageid": 3, "ns": 0, "title": "Воробей"},
        ]
    },
}


class _MockResponse:
    """Примитивная реализация объекта requests.Response"""

    def __init__(self, payload):
        self._payload = payload
        self.status_code = 200

    def raise_for_status(self):
        pass  # статус 200, без ошибок

    def json(self):
        return self._payload


@patch("task2.client.requests.Session")
def test_fetch_animal_titles_paginated(mock_session_cls):
    """Проверяем, что пагинация обрабатывается корректно."""
    # Настраиваем последовательность ответов
    mock_session = mock_session_cls.return_value
    mock_session.get.side_effect = [
        _MockResponse(FIRST_PAGE),
        _MockResponse(SECOND_PAGE),
    ]

    titles = fetch_animal_titles(limit_per_request=2)  # лимит не важен тут
    assert titles == ["Акула", "Бобр", "Воробей"]
    # убедимся, что было два сетевых вызова
    assert mock_session.get.call_count == 2
