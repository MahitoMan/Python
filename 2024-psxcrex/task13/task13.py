import math

# Функция для вычисления евклидова расстояния между двумя точками
def distance(p1, p2):
    return math.sqrt((p2[0] - p1[0])**2 + (p2[1] - p1[1])**2 + (p2[2] - p1[2])**2)

# Список для хранения координат атомов 'CA'
ca_atoms = []

# Чтение данных из стандартного ввода
while True:
    line = input().strip()  # Убираем лишние пробелы и символы новой строки
    
    if not line or len(ca_atoms) >= 2 and ca_atoms[-1][0] == '' and ca_atoms[-2][0] == '':
        break  # Завершаем цикл при двух подряд пустых строках
    
    if line.startswith('ATOM') and 'CA' in line[12:16]:
        # Разделяем строку на части по пробелам
        parts = line.split()
        
        # Извлекаем координаты атома 'CA'
        try:
            x = float(parts[6])
            y = float(parts[7])
            z = float(parts[8])
            
            # Добавляем координаты в список
            ca_atoms.append((x, y, z))
        except ValueError as e:
            print(f"Ошибка преобразования строки '{line}' в координаты: {e}")

# Проверяем наличие хотя бы двух атомов 'CA'
if len(ca_atoms) < 2:
    print("Недостаточно атомов 'CA'")
else:
    # Вычисление расстояний между соседними атомами 'CA'
    distances = [distance(ca_atoms[i], ca_atoms[i+1]) for i in range(len(ca_atoms)-1)]
    
    # Выводим результаты
    for dist in distances:
        print(f"{dist:.3f}")