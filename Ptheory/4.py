import math

# Функция для вычисления биномиального коэффициента
def binomial_coefficient(n, k):
    return math.comb(n, k)

# Количество различных культур тканей
num_tissues = 6

# Количество различных культур бактерий
num_bacteria = 30

# Подсчет количества способов выбора бактерий
ways_to_choose_bacteria = (
    binomial_coefficient(num_bacteria, 1) +
    binomial_coefficient(num_bacteria, 2) +
    binomial_coefficient(num_bacteria, 3)
)

# Общее количество экспериментов
total_ways = num_tissues * ways_to_choose_bacteria

print(total_ways)

