from collections import defaultdict
from typing import Dict, Iterable


def count_by_first_letter(titles: Iterable[str]) -> Dict[str, int]:
    """
    Подсчитывает количество элементов, начинающихся с каждой буквы.
    """

    counter: Dict[str, int] = defaultdict(int)
    for title in titles:
        if not title:
            continue
        first_char = title[0].upper()
        counter[first_char] += 1
    return dict(counter)


def serialize_counts(counts: Dict[str, int]) -> Iterable[str]:
    """
    Подготавливает содержимое CSV-файла (без заголовка).
    """
    for letter in sorted(counts.keys(), key=str.upper):
        yield f"{letter},{counts[letter]}"


def write_csv(counts: Dict[str, int], path: str = "beasts.csv") -> None:
    """
    Записывает итоговый CSV-файл.
    """
    with open(path, "w", encoding="utf-8") as f:
        for line in serialize_counts(counts):
            f.write(f"{line}\n")
