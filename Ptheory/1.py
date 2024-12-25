import math

# Функция для первой части выражения
def first_part():
    result = 0
    for i in range(5, 16):
        result += math.comb(40, i) * math.comb(40 - i, i)
    return result

# Функция для второй части выражения
def second_part():
    return (
        math.comb(15, 5) * math.comb(10, 5) +
        math.comb(15, 6) * math.comb(9, 6) +
        math.comb(15, 7) * math.comb(8, 7)
    )

# Итоговый результат
first_result = first_part()
second_result = second_part()
total_result = first_result * second_result
print(total_result)
