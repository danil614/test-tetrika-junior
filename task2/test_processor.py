from task2.processor import count_by_first_letter, serialize_counts


def test_count_by_first_letter_basic():
    titles = [
        "Акула",
        "Аист",
        "бобр",
        "Воробей",
        "ёж",
        "",  # пустая строка должна игнорироваться
        "123 Крот",  # первый символ не-буква
    ]
    expected = {
        "А": 2,
        "Б": 1,
        "В": 1,
        "Ё": 1,
        "1": 1,
    }
    assert count_by_first_letter(titles) == expected


def test_serialize_counts_sorted():
    counts = {"Б": 2, "А": 1, "В": 3}
    lines = list(serialize_counts(counts))
    assert lines == ["А,1", "Б,2", "В,3"]  # сортировка по алфавиту
