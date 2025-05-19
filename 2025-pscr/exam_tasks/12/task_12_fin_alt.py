import pandas as pd
import numpy as np
from collections import defaultdict
import math
import os
import sys # Импорт модуля sys для работы с аргументами командной строки

class Atom:
    """
    Класс для представления атома в структуре PDB.
    """
    def __init__(self, serial, atom_name, res_name, chain_id, res_seq, x, y, z):
        """
        Инициализация объекта Atom.

        Args:
            serial (int): Серийный номер атома.
            atom_name (str): Имя атома.
            res_name (str): Имя аминокислоты.
            chain_id (str): Идентификатор цепи.
            res_seq (int): Номер аминокислоты.
            x (float): Координата X.
            y (float): Координата Y.
            z (float): Координата Z.
        """
        self.serial = serial
        self.atom_name = atom_name.strip()
        self.res_name = res_name.strip()
        self.chain_id = chain_id
        self.res_seq = res_seq
        self.coords = np.array([x, y, z], dtype=float)

    def __repr__(self):
        return f"<Atom {self.serial} {self.atom_name} {self.res_name}{self.res_seq} ({self.chain_id})>"

def parse_pdb(pdb_filepath):
    """
    Парсинг PDB файла, извлечение данных атомов и связей.

    Args:
        pdb_filepath (str): Путь к PDB файлу.

    Returns:
        tuple: Словарь атомов ({serial: Atom}) и множество уникальных связей (tuple(sorted(s1, s2))).
    """
    atoms = {}
    raw_bonds = []

    try:
        with open(pdb_filepath, 'r') as f:
            for line in f:
                if line.startswith("ATOM"):
                    try:
                        # Парсинг строки ATOM согласно формату PDB
                        serial = int(line[6:11])
                        atom_name = line[12:16]
                        res_name = line[17:20]
                        chain_id = line[21]
                        res_seq = int(line[22:26])
                        x = float(line[30:38])
                        y = float(line[38:46])
                        z = float(line[46:54])
                        atoms[serial] = Atom(serial, atom_name, res_name, chain_id, res_seq, x, y, z)
                    except ValueError as e:
                        print(f"Пропущена некорректная строка ATOM: {line.strip()} из-за ошибки: {e}")
                        continue
                    except IndexError:
                         print(f"Пропущена некорректная строка ATOM (неверная длина): {line.strip()}")
                         continue


                elif line.startswith("CONECT"):
                    try:
                        # Парсинг строки CONECT согласно формату PDB
                        atom_serial_1 = int(line[6:11])

                        # Извлечение серийных номеров связанных атомов
                        bonded_atom_serials_str = []
                        if len(line) > 11: bonded_atom_serials_str.append(line[11:16].strip())
                        if len(line) > 16: bonded_atom_serials_str.append(line[16:21].strip())
                        if len(line) > 21: bonded_atom_serials_str.append(line[21:26].strip())
                        if len(line) > 26: bonded_atom_serials_str.append(line[26:31].strip())

                        for bonded_serial_str in bonded_atom_serials_str:
                            if bonded_serial_str:
                                atom_serial_2 = int(bonded_serial_str)
                                # Добавление связи (уникальный кортеж)
                                raw_bonds.append(tuple(sorted((atom_serial_1, atom_serial_2))))
                    except ValueError as e:
                        print(f"Пропущена некорректная строка CONECT: {line.strip()} из-за ошибки: {e}")
                        continue
                    except IndexError:
                         print(f"Пропущена некорректная строка CONECT (неверная длина): {line.strip()}")
                         continue

    except FileNotFoundError:
        # Обработка ошибки отсутствия файла
        print(f"Ошибка: Файл не найден по пути {pdb_filepath}")
        return {}, set()
    except Exception as e:
        print(f"Произошла ошибка при чтении файла {pdb_filepath}: {e}")
        return {}, set()

    unique_bonds = set(raw_bonds)
    return atoms, unique_bonds

def calculate_distance(coords1, coords2):
    """
    Вычисление расстояния между 3D точками.

    Args:
        coords1 (np.array): Координаты точки 1.
        coords2 (np.array): Координаты точки 2.

    Returns:
        float: Евклидово расстояние.
    """
    # Использование np.linalg.norm
    return np.linalg.norm(coords1 - coords2)

def calculate_average_bond_lengths(pdb_filepath):
    """
    Расчет средних длин внутримолекулярных связей по типу аминокислоты.

    Args:
        pdb_filepath (str): Путь к PDB файлу.

    Returns:
        pd.DataFrame: Таблица средних длин связей. Пустой DataFrame в случае ошибки/отсутствия данных.
    """
    atoms, unique_bonds = parse_pdb(pdb_filepath)

    if not atoms:
        return pd.DataFrame()

    # Структура для хранения длин связей
    bond_lengths_data = defaultdict(lambda: defaultdict(list))

    for s1, s2 in unique_bonds:
        # Проверка наличия атомов
        if s1 not in atoms or s2 not in atoms:
            continue

        atom1 = atoms[s1]
        atom2 = atoms[s2]

        # Фильтр внутримолекулярных связей
        if (atom1.res_name == atom2.res_name and
            atom1.res_seq == atom2.res_seq and
            atom1.chain_id == atom2.chain_id):

            dist = calculate_distance(atom1.coords, atom2.coords)

            # Формирование ключа типа связи
            bond_type_key = tuple(sorted((atom1.atom_name, atom2.atom_name)))

            bond_lengths_data[atom1.res_name][bond_type_key].append(dist)

    # Подготовка данных для DataFrame
    output_data = []
    for res_name, atom_pairs_dict in bond_lengths_data.items():
        for (atom_n1, atom_n2), lengths_list in atom_pairs_dict.items():
            if lengths_list:
                avg_length = np.mean(lengths_list)
                count = len(lengths_list)
                output_data.append({
                    "Тип аминокислоты": res_name,
                    "Атом 1": atom_n1,
                    "Атом 2": atom_n2,
                    "Средняя длина связи": avg_length,
                    "Количество связей": count
                })

    if not output_data:
        print("Внутримолекулярные связи, подходящие под критерии, не найдены в файле "
              "или PDB файл не содержит таких связей/атомов.")
        return pd.DataFrame()

    df = pd.DataFrame(output_data)
    # Сортировка DataFrame
    df = df.sort_values(by=["Тип аминокислоты", "Атом 1", "Атом 2"]).reset_index(drop=True)
    return df

if __name__ == '__main__':
    # Проверка аргументов командной строки
    if len(sys.argv) < 2:
        print("Использование: python ваш_скрипт.py <путь_к_pdb_файлу>")
        sys.exit(1)

    # Получение пути к файлу
    pdb_file_path = sys.argv[1]

    # Проверка существования файла
    if not os.path.exists(pdb_file_path):
        print(f"Ошибка: Файл не найден по пути: {pdb_file_path}")
        sys.exit(1)

    print(f"\nНачинается анализ файла: {pdb_file_path}")
    results_df = calculate_average_bond_lengths(pdb_file_path)

    if not results_df.empty:
        print("\nРезультаты расчета средних длин связей:")
        # Вывод DataFrame в консоль без усечения
        with pd.option_context('display.max_rows', None,
                               'display.max_columns', None,
                               'display.width', 1000):
            print(results_df)

    else:
        print(f"Анализ файла {pdb_file_path} завершен. Данные для таблицы не сформированы.")
