from collections import Counter

def get_top_trimers(sequence):
    # Создаем список всех возможных тримеров
    trimers = [sequence[i:i + 3] for i in range(len(sequence) - 2)]
    
    # Считаем количество каждого тримера
    counter = Counter(trimers)
    
    # Находим 4 наиболее часто встречающихся тримера
    top_4 = counter.most_common(4)
    
    return [(trimer, count) for trimer, count in top_4]

# Основное решение
sequences = []
current_sequence = ""

while True:
    try:
        line = input()
    except EOFError:
        break
    if not line.strip():
        continue
    elif line.startswith('>'):
        if current_sequence:
            sequences.append(current_sequence)
        current_sequence = ""
    else:
        current_sequence += line.strip().upper()

if current_sequence:
    sequences.append(current_sequence)

for sequence in sequences:
    top_4 = get_top_trimers(sequence)
    print(f'\nДля последовательности {sequence}:')
    for trimer, count in top_4:
        print(f'{trimer} встречается {count} раз.')