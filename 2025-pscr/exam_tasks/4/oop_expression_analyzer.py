# oop_expression_analyzer.py
"""
Модуль для анализа данных дифференциальной экспрессии.
Определяет гены со статистически значимыми изменениями экспрессии.
"""
import pandas as pd
import re
import sys
from typing import Set, List, Optional, Dict, Any

# Импорт вспомогательной функции для безопасного открытия файла
try:
    from utils import safe_open
except ImportError as e:
    print(f"Ошибка импорта модуля: {e}. Убедитесь, что utils.py "
          "находится в том же каталоге или доступен в PYTHONPATH.", file=sys.stderr)
    sys.exit(1)

class ExpressionAnalyzer:
    """
    Класс для анализа данных дифференциальной экспрессии генов.
    """
    def __init__(
        self,
        diff_expr_file: str,
        pval_threshold: float = 0.05,
        log2fc_threshold: float = 1.0,
        min_experiments: int = 2
    ):
        """
        Инициализация анализатора экспрессии с параметрами фильтрации.

        Args:
            diff_expr_file: Путь к файлу с данными дифференциальной экспрессии.
            pval_threshold: Порог p-value.
            log2fc_threshold: Порог абсолютного значения log2 Fold Change.
            min_experiments: Минимальное количество экспериментов для значимости.
        """
        self.diff_expr_file: str = diff_expr_file
        self.pval_threshold: float = pval_threshold
        self.log2fc_threshold: float = log2fc_threshold
        self.min_experiments: int = min_experiments
        self._df: Optional[pd.DataFrame] = None # Хранение загруженного DataFrame

    def _load_data(self) -> bool:
        """
        Загрузка данных дифференциальной экспрессии из файла.

        Returns:
            True, если данные успешно загружены и не пусты, иначе False.
        """
        print(f"Загрузка данных из файла: {self.diff_expr_file}", file=sys.stderr)
        try:
            with safe_open(self.diff_expr_file, 'r') as f:
                self._df = pd.read_csv(f, sep=',', engine='python')

            if self._df.empty:
                print(f"Предупреждение: Файл таблицы экспрессии '{self.diff_expr_file}' пуст.", file=sys.stderr)
                self._df = None
                return False

            required_base_column: str = 'gene_id'
            if required_base_column not in self._df.columns:
                print(f"Ошибка: Обязательная колонка '{required_base_column}' не найдена в таблице экспрессии.", file=sys.stderr)
                self._df = None
                return False

            print("Данные успешно загружены.", file=sys.stderr)
            return True

        except FileNotFoundError:
            self._df = None
            return False
        except pd.errors.EmptyDataError:
            print(f"Ошибка: Файл таблицы экспрессии '{self.diff_expr_file}' пуст или не содержит данных.", file=sys.stderr)
            self._df = None
            return False
        except pd.errors.ParserError:
            print(f"Ошибка: Не удалось разобрать файл таблицы экспрессии '{self.diff_expr_file}'. Проверьте формат.", file=sys.stderr)
            self._df = None
            return False
        except Exception as e:
            print(f"Неожиданная ошибка при чтении файла таблицы экспрессии '{self.diff_expr_file}': {e}", file=sys.stderr)
            self._df = None
            return False

    def find_target_genes(self) -> Set[str]:
        """
        Анализирует данные и определяет целевые гены.

        Returns:
            Множество идентификаторов (str) целевых генов.
            Возвращает пустое множество в случае ошибок или если гены не найдены.
        """
        if self._df is None and not self._load_data():
            return set()

        exp_ids: Set[str] = set()
        for col_name in self._df.columns:
            match = re.search(r'exp(\w+?)_pval', col_name, re.IGNORECASE)
            if match:
                exp_id = match.group(1)
                if f'exp{exp_id}_log2FC' in self._df.columns:
                     exp_ids.add(exp_id)

        if not exp_ids:
            print("Ошибка: Не удалось определить парные колонки экспериментов (exp<ID>_pval и exp<ID>_log2FC) "
                  "из заголовков таблицы.", file=sys.stderr)
            return set()

        sorted_experiment_ids: List[str] = sorted(list(exp_ids))
        print(f"Обнаружены данные для {len(sorted_experiment_ids)} экспериментов. ID: {sorted_experiment_ids}", file=sys.stderr)

        significant_exp_counts = pd.Series(0, index=self._df.index)

        for exp_num_str in sorted_experiment_ids:
            pval_col = f'exp{exp_num_str}_pval'
            log2fc_col = f'exp{exp_num_str}_log2FC'

            if pval_col in self._df.columns and log2fc_col in self._df.columns:
                pval_series = pd.to_numeric(self._df[pval_col], errors='coerce').fillna(1.0)
                log2fc_series = pd.to_numeric(self._df[log2fc_col], errors='coerce').fillna(0.0)

                is_significant_in_current_exp = (pval_series < self.pval_threshold) & (abs(log2fc_series) >= self.log2fc_threshold)

                significant_exp_counts += is_significant_in_current_exp.astype(int)

        target_genes_df = self._df[significant_exp_counts >= self.min_experiments]

        required_base_column: str = 'gene_id'
        if required_base_column not in target_genes_df.columns:
             print(f"Ошибка: Колонка '{required_base_column}' отсутствует после фильтрации.", file=sys.stderr)
             return set()

        target_genes = set(target_genes_df[required_base_column].dropna().astype(str))

        if target_genes:
            print(f"Найдено {len(target_genes)} целевых генов, удовлетворяющих критериям.", file=sys.stderr)
        else:
            print("Целевые гены, удовлетворяющие критериям, не найдены.", file=sys.stderr)

        return target_genes

# if __name__ == "__main__":
#     pass

