import math

def permutations(n, k):
    """Вычисляет количество размещений из n по k."""
    return math.factorial(n) // math.factorial(n - k)

def solve():
    """Решает задачу и выводит ответ."""
    n_cultures = 14
    n_petri_dishes = 5

    # Выбираем 5 культур и распределяем их по 5 чашкам (размещения)
    first_stage_ways = permutations(n_cultures, n_petri_dishes)

    # Распределяем оставшиеся 9 культур по 5 чашкам
    remaining_cultures = n_cultures - n_petri_dishes
    second_stage_ways = n_petri_dishes ** remaining_cultures

    total_ways = first_stage_ways * second_stage_ways
    print(f"Количество способов распределить культуры: {total_ways}")

solve()
