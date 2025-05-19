from itertools import combinations

def solve():
    n_cultures = 14
    n_plates = 5

    total_ways = 0
    for i in range(n_plates + 1):
        sign = (-1) ** i
        ways_to_choose_empty_plates = combinations(range(n_plates), i)
        ways_to_distribute_cultures = (n_plates - i) ** n_cultures
        total_ways += sign * sum(1 for _ in ways_to_choose_empty_plates) * ways_to_distribute_cultures

    print(f"Количество способов: {int(total_ways)}")

if __name__ == "__main__":
    solve()
    
