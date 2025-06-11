"""
Задача:
Определить общее время одновременного присутствия ученика и учителя
на уроке (т. е. когда оба находятся «в он-лайне» и этот отрезок
целиком попадает в границы урока).

Данные:
intervals = {
    'lesson': [start, finish],
    'pupil':  [in1, out1, in2, out2, ...],
    'tutor':  [in1, out1, in2, out2, ...],
}
Все значения – UNIX-time в секундах.
"""

from typing import List, Tuple, Dict


def _pairs(raw: List[int]) -> List[Tuple[int, int]]:
    """
    Превращаем плоский список вида [in, out, in, out, …]
    в список пар [(in, out), …].
    """
    if len(raw) % 2:
        raise ValueError("Number of points must be even (in/out).")
    return [(raw[i], raw[i + 1]) for i in range(0, len(raw), 2)]


def _crop(intervals: List[Tuple[int, int]],
          border: Tuple[int, int]) -> List[Tuple[int, int]]:
    """
    Обрезаем интервалы по границам border.
    border – (start, end) урока.
    """
    start_lesson, end_lesson = border
    cropped: List[Tuple[int, int]] = []
    for start, end in intervals:
        # пересечение двух отрезков
        left = max(start, start_lesson)
        right = min(end, end_lesson)
        if left < right:  # есть ненулевая длина
            cropped.append((left, right))
    return cropped


def _merge(intervals: List[Tuple[int, int]]) -> List[Tuple[int, int]]:
    """
    Сливаем пересекающиеся/смежные интервалы.
    """
    if not intervals:
        return []

    intervals.sort()
    merged: List[Tuple[int, int]] = [intervals[0]]

    for start, end in intervals[1:]:
        last_start, last_end = merged[-1]
        if start <= last_end:  # наложение или касание
            merged[-1] = (last_start, max(last_end, end))
        else:
            merged.append((start, end))
    return merged


def _intersection_time(a: List[Tuple[int, int]],
                       b: List[Tuple[int, int]]) -> int:
    """
    Суммируем длины пересечений двух наборов непересекающихся интервалов.
    """
    i = j = 0
    common = 0
    while i < len(a) and j < len(b):
        a_start, a_end = a[i]
        b_start, b_end = b[j]

        left = max(a_start, b_start)
        right = min(a_end, b_end)
        if left < right:
            common += right - left

        # двигаем тот указатель, чей интервал раньше закончился
        if a_end < b_end:
            i += 1
        else:
            j += 1
    return common


def appearance(intervals: Dict[str, List[int]]) -> int:
    """
    Основная функция задачи.
    1) Превращаем входные списки в интервалы.
    2) Обрезаем их границами урока.
    3) Сливаем пересекающиеся интервалы (на случай дублей/накладок).
    4) Считаем пересечение двух множеств интервалов.
    """
    lesson = tuple(intervals['lesson'])
    pupil = _pairs(intervals['pupil'])
    tutor = _pairs(intervals['tutor'])

    pupil = _merge(_crop(pupil, lesson))
    tutor = _merge(_crop(tutor, lesson))

    return _intersection_time(pupil, tutor)


# -------------------------- Тесты --------------------------

tests = [
    {
        'intervals': {
            'lesson': [1594663200, 1594666800],
            'pupil': [1594663340, 1594663389,
                      1594663390, 1594663395,
                      1594663396, 1594666472],
            'tutor': [1594663290, 1594663430,
                      1594663443, 1594666473],
        },
        'answer': 3117,
    },
    {
        'intervals': {
            'lesson': [1594702800, 1594706400],
            'pupil': [1594702789, 1594704500,
                      1594702807, 1594704542,
                      1594704512, 1594704513,
                      1594704564, 1594705150,
                      1594704581, 1594704582,
                      1594704734, 1594705009,
                      1594705095, 1594705096,
                      1594705106, 1594706480,
                      1594705158, 1594705773,
                      1594705849, 1594706480,
                      1594706500, 1594706875,
                      1594706502, 1594706503,
                      1594706524, 1594706524,
                      1594706579, 1594706641],
            'tutor': [1594700035, 1594700364,
                      1594702749, 1594705148,
                      1594705149, 1594706463],
        },
        'answer': 3577,
    },
    {
        'intervals': {
            'lesson': [1594692000, 1594695600],
            'pupil': [1594692033, 1594696347],
            'tutor': [1594692017, 1594692066,
                      1594692068, 1594696341],
        },
        'answer': 3565,
    },
]

if __name__ == '__main__':
    for i, test in enumerate(tests):
        test_answer = appearance(test['intervals'])
        assert test_answer == test['answer'], f'Error on test case {i}, got {test_answer}, expected {test["answer"]}'
    print('Все тесты пройдены успешно!')
