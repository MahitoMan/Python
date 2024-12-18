from collections import Counter

def get_top_trimers(sequence):
    # Создаем список всех возможных тримеров
    trimers = [sequence[i:i+3] for i in range(len(sequence)-2)]
    
    # Считаем количество каждого тримера
    counter = Counter(trimers)
    
    # Находим 4 наиболее часто встречающихся тримера
    top_4 = counter.most_common(4)
    
    return [(trimer, count) for trimer, count in top_4]

# Основная логика программы
sequences = []
current_sequence = ""
empty_lines_count = 0

while True:
    try:
        line = input()
    except EOFError:
        break
    if not line.strip():
        empty_lines_count += 1
        if empty_lines_count == 2:
            sequences.append(current_sequence)
            break
        else:
            sequences.append(current_sequence)
            current_sequence = ""
    elif line.startswith(">"):
        if current_sequence:
            sequences.append(current_sequence)
        current_sequence = ""
    else:
        current_sequence += line.strip().upper()

for sequence in sequences:
    top_4 = get_top_trimers(sequence)
    print(f'Для последовательности {sequence}:')
    for trimer, count in top_4:
        print(f'{trimer} встречается {count} раз.')
