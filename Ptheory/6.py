import numpy as np
from scipy.special import comb
import itertools

spots = np.arange(2, 24, 2)
prob_spot = 1 / len(spots)

def solve():
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

if __name__ == "__main__":
    solve()
