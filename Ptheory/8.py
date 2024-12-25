import math

def combinations(n, k):
  """Вычисляет количество сочетаний из n по k."""
  return math.factorial(n) // (math.factorial(k) * math.factorial(n - k))

def solve():
    """Решает задачу и выводит ответ."""
    total_microdistricts = 40
    infected_microdistricts = 3
    selected_microdistricts = 8

    # Вычисляем количество способов выбрать 8 микрорайонов из всех 40
    total_combinations = combinations(total_microdistricts, selected_microdistricts)

    # Вычисляем количество способов выбрать 8 микрорайонов из здоровых 
    safe_combinations = combinations(total_microdistricts - infected_microdistricts, selected_microdistricts)

    # Вероятность того, что не будет объявлен карантин
    probability_no_quarantine = safe_combinations / total_combinations
    
    # Вероятность объявления карантина
    probability_quarantine = 1 - probability_no_quarantine


    print(f"Вероятность объявления карантина: {probability_quarantine:.4f}")

solve()

