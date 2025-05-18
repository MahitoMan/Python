# utils.py
"""
Вспомогательные функции для обработки ошибок.
"""
import sys
from typing import TextIO

def safe_open(filepath: str, mode: str = 'r', encoding: str = 'utf-8') -> TextIO:
    """
    Безопасно открывает файл, обрабатывая ошибки.

    Args:
        filepath: Путь к файлу.
        mode: Режим открытия файла.
        encoding: Кодировка файла.

    Returns:
        Объект файла (TextIO).

    Raises:
        FileNotFoundError: Если файл не найден.
        IOError: При других ошибках ввода/вывода.
    """
    try:
        return open(filepath, mode, encoding=encoding)
    except FileNotFoundError:
        print(f"Ошибка: Файл не найден по пути '{filepath}'.", file=sys.stderr)
        raise
    except IOError as e:
        print(f"Ошибка ввода/вывода при работе с файлом '{filepath}': {e}", file=sys.stderr)
        raise

# Другие вспомогательные функции могут быть добавлены здесь.

