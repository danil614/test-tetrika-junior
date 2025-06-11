from pathlib import Path

from task2.client import fetch_animal_titles
from task2.processor import count_by_first_letter, write_csv


def main() -> None:
    print("Загружаем список животных с русской Википедии...")
    titles = fetch_animal_titles()
    print(f"Всего получено статей: {len(titles)}")

    counts = count_by_first_letter(titles)
    write_csv(counts)

    print(f"Файл beasts.csv успешно создан в {Path.cwd()}")


if __name__ == "__main__":
    main()
