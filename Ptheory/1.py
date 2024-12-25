import math

def combinations(n, k):
    """
    Вычисляет количество сочетаний из n по k.
    
    :param int n: Общее количество объектов.
    :param int k: Количество выбираемых объектов.
    :return: Количество сочетаний из n по k.
    """
    return math.comb(n, k)

def permutations(n, k):
    """
    Вычисляет количество размещений из n по k.
    
    :param int n: Общее количество объектов.
    :param int k: Количество выбираемых объектов.
    :return: Количество размещений из n по k.
    """
    return math.factorial(n) // math.factorial(n - k)

def solve():
    """
    Решает задачу и выводит ответы для обоих случаев.
    """
    total_white_mice = 40
    total_brown_mice = 15
    min_white_mice = 5
    max_white_mice = 15
    min_brown_mice = 5
    max_brown_mice = 10

    total_ways_identical = 0
    total_ways_distinct = 0

    for white_mice in range(min_white_mice, max_white_mice + 1):
        for brown_mice in range(min_brown_mice, max_brown_mice + 1):
            # Мыши одинаковые
            num_ways_identical = combinations(total_white_mice, white_mice) * combinations(total_brown_mice, brown_mice)
            total_ways_identical += num_ways_identical

            # Мыши разные
            num_ways_distinct = (permutations(total_white_mice, white_mice) * permutations(total_brown_mice, brown_mice))**2
            total_ways_distinct += num_ways_distinct

    print(f"Количество способов (мыши одинаковые): {total_ways_identical}")
    print(f"Количество способов (мыши различаются): {total_ways_distinct}")

# Запуск решения
solve()