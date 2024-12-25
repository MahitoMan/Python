import numpy as np
from scipy.special import comb
import itertools

def solve():
    # Возможные значения пятен
    spots = np.arange(2, 24, 2)
    
    # Вероятность каждого конкретного значения пятна
    prob_spot = 1 / len(spots)
    
    # 1. Вероятность того, что при выборе двух особей суммарное число пятен равно 42
    prob_sum_42 = 2 / (len(spots) ** 2)
    print(f"Вероятность (сумма 42): {prob_sum_42:.4f}")

    # 2. Вероятность того, что при выборе двух особей суммарное число пятен не превышает 20
    count = 0
    for s1 in spots:
        for s2 in spots:
            if s1 + s2 <= 20:
                count += 1
    prob_sum_le_20 = count / (len(spots) ** 2)
    print(f"Вероятность (сумма <= 20): {prob_sum_le_20:.4f}")

    # 3. Вероятность того, что при выборе трех особей суммарное число пятен превышает 60
    prob_sum_gt_60 = 4 / (len(spots) ** 3)
    print(f"Вероятность (сумма > 60): {prob_sum_gt_60:.4f}")

    # 4. Вероятность того, что при выборе 10 особей, не менее чем у двух особей будет ровно по два пятна
    n = 10
    k = 2
    p = 1 / 11
    q = 1 - p
    prob_at_least_2 = 1 - (comb(n, 0) * (p**0) * (q**10) + comb(n, 1) * (p**1) * (q**(n-1)))
    print(f"Вероятность (хотя бы у 2 по 2): {prob_at_least_2:.4f}")

    # 5. Вероятность того, что при выборе двух пар особей, суммарное число пятен в первой паре совпадает с суммарным числом пятен во второй
    pair_sums = {}
    for pair in itertools.product(spots, repeat=2):
        s = sum(pair)
        if s not in pair_sums:
            pair_sums[s] = 1
        else:
            pair_sums[s] += 1

    total_combinations = len(spots) ** 2
    probabilities = [(v * (v - 1)) / total_combinations ** 2 for v in pair_sums.values()]
    prob_same_sum = sum(probabilities)
    print(f"Вероятность (суммы совпадают): {prob_same_sum:.4f}")

if __name__ == "__main__":
    solve()
