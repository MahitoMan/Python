import numpy as np

# Определим вероятности различных генотипов
p_CC = 0.05
p_Cc = 0.10
p_Cb = 0.15
p_Cs = 0.20
p_Ca_star = 0.25
p_ca_star_a_star = 0.03
p_cbcb = 0.07
p_cbc = 0.08
p_cbCs = 0.09
p_cbCa_star = 0.11
p_cc = 0.02
p_csCa_star = 0.04

# Определим вероятности событий
P_A = p_CC + p_Cc + p_Cb + p_Cs + p_Ca_star
P_B = P_A**2 # Вероятность, что 2 кошки - сплошные альбиносы (если это подразумевалось)
P_C = p_csCa_star
P_D = 1 - p_cc
P_E = p_cbcb + p_cbc + p_cbCs + p_cbCa_star + p_ca_star_a_star

# Вычислим вероятности сложных событий (с учетом анализа)
P_a = P_B # AB эквивалентно B
P_b = P_C  # CE эквивалентно C
P_c = 1- P_E # DĒ эквивалентно Ē
P_d = (1 - P_A) * P_C * P_D
P_e = P_A # A ∪ B эквивалентно A
P_f = P_A * (1 - P_D) + (1 - P_A) * P_D # Корректная формула для A Δ D
P_g = P_E - P_C # E \ C
P_h = 0 # (A ∪ B) \ E, противоречие поэтому вероятность 0

print("Вероятность события a): {:.4f}".format(P_a))
print("Вероятность события b): {:.4f}".format(P_b))
print("Вероятность события c): {:.4f}".format(P_c))
print("Вероятность события d): {:.4f}".format(P_d))
print("Вероятность события e): {:.4f}".format(P_e))
print("Вероятность события f): {:.4f}".format(P_f))
print("Вероятность события g): {:.4f}".format(P_g))
print("Вероятность события h): {:.4f}".format(P_h))
