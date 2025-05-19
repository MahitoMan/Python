def solve():
    """Решает задачу и выводит ответ."""
    # Пропорция ульев
    proportion_i = 3
    proportion_c = 5
    proportion_s = 4
    total_proportion = proportion_i + proportion_c + proportion_s
    
    # Доли ульев от общего количества
    p_i = proportion_i / total_proportion
    p_c = proportion_c / total_proportion
    p_s = proportion_s / total_proportion
    
    # Вероятности трутней в ульях
    p_drone_i = 0.20
    p_drone_c = 0.10
    p_drone_s = 0.15
    
    # Вероятности рабочих пчел в ульях
    p_worker_i = 1 - p_drone_i
    p_worker_c = 1 - p_drone_c
    p_worker_s = 1 - p_drone_s

    # Вероятность извлечения рабочей пчелы
    probability_worker = p_worker_i * p_i + p_worker_c * p_c + p_worker_s * p_s

    # Вероятность, что за неделю не будет трутней
    probability_no_drone_week = probability_worker**7 

    print(f"Вероятность, что за неделю не встретится трутней: {probability_no_drone_week:.4f}")

solve()
