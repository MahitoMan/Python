# Функция для расчета количества допустимых триплетов
def count_valid_sequences():
    # Всего возможно 64 триплета
    total_triplets = 4 ** 3
    
    # Три из них являются стоп-кодонами
    stop_codons = ["UAA", "UAG", "UGA"]
    
    # Количество допустимых триплетов
    valid_triplets = total_triplets - len(stop_codons)
    
    # Четыре триплета перед стоп-кодоном
    sequences_before_stop = valid_triplets ** 4
    
    # Три возможных стоп-кодона
    possible_stop_codons = len(stop_codons)
    
    # Общее количество допустимых последовательностей
    total_sequences = sequences_before_stop * possible_stop_codons
    
    return total_sequences

# Вызываем функцию и выводим результат
print(count_valid_sequences())
