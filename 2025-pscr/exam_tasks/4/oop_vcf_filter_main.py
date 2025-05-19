# oop_vcf_filter_main.py
"""
Основной скрипт для фильтрации VCF-файлов по дифференциальной экспрессии генов.
"""
import argparse
import sys
from typing import Set, Optional, List

# Импорт необходимых классов
try:
    from oop_expression_analyzer import ExpressionAnalyzer
    from oop_vcf_parser import VcfFilter
except ImportError as e:
    print(f"Ошибка импорта модуля: {e}. Убедитесь, что oop_expression_analyzer.py, oop_vcf_parser.py "
          "и utils.py находятся в том же каталоге или доступны в PYTHONPATH.", file=sys.stderr)
    sys.exit(1)


def main() -> None:
    """
    Главная функция программы.
    Обрабатывает аргументы командной строки и запускает процесс фильтрации.
    """
    parser = argparse.ArgumentParser(
        description=(
            "Фильтрует VCF-файл на основе данных о дифференциальной экспрессии генов. "
            "Отбираются варианты из VCF, аннотированные на гены, которые показали "
            "статистически значимые изменения экспрессии в заданном числе экспериментов. "
            "По умолчанию результат выводится в стандартный поток вывода (stdout)."
        ),
        formatter_class=argparse.RawTextHelpFormatter
    )

    parser.add_argument(
        "diff_expr_file",
        type=str,
        help="Путь к файлу с данными о дифференциальной экспрессии (TSV/CSV)."
    )
    parser.add_argument(
        "vcf_file",
        type=str,
        help="Путь к входному VCF-файлу для фильтрации."
    )

    parser.add_argument(
        "-o", "--output_file",
        type=str,
        default=None,
        help="Путь к выходному отфильтрованному VCF-файлу. Если не указан, вывод в stdout."
    )

    exp_group = parser.add_argument_group('Параметры анализа экспрессии')
    exp_group.add_argument(
        "--pval",
        type=float,
        default=0.05,
        help="Порог p-value (по умолчанию: 0.05)."
    )
    exp_group.add_argument(
        "--log2fc",
        type=float,
        default=1.0,
        help="Порог абсолютного значения log2 Fold Change (по умолчанию: 1.0)."
    )
    exp_group.add_argument(
        "--min_exp",
        type=int,
        default=2,
        help="Минимальное количество экспериментов со значимыми изменениями (по умолчанию: 2)."
    )

    vcf_info_group = parser.add_argument_group('Параметры парсинга VCF INFO поля')
    vcf_info_group.add_argument(
        "--ann_tag",
        type=str,
        default="ANN",
        help="Тег в поле INFO VCF-файла, содержащий аннотации генов (по умолчанию: 'ANN')."
    )
    vcf_info_group.add_argument(
        "--gene_idx",
        type=int,
        default=3,
        help="Индекс (0-based) имени гена в строке аннотации (поля разделены '|'). Для SnpEff 'ANN' это обычно 3. По умолчанию: 3."
    )

    args = parser.parse_args()

    print("--- Начало процесса фильтрации VCF (ООП версия) ---", file=sys.stderr)

    print("\nШаг 1: Анализ таблицы дифференциальной экспрессии с помощью ExpressionAnalyzer...", file=sys.stderr)
    analyzer = ExpressionAnalyzer(
        diff_expr_file=args.diff_expr_file,
        pval_threshold=args.pval,
        log2fc_threshold=args.log2fc,
        min_experiments=args.min_exp
    )

    target_genes: Set[str] = analyzer.find_target_genes()

    if target_genes:
        sorted_target_genes: List[str] = sorted(list(target_genes))
        print("\n--- Список целевых генов, удовлетворяющих критериям экспрессии ---", file=sys.stderr)
        for gene in sorted_target_genes:
            print(gene, file=sys.stderr)
        print("-------------------------------------------------------------------", file=sys.stderr)

    if not target_genes:
        print("Целевые гены не найдены на основе предоставленных критериев. "
              "Фильтрация VCF не будет производить значимых результатов.", file=sys.stderr)
        print("--- Процесс фильтрации VCF завершен (целевые гены не найдены) ---", file=sys.stderr)
        sys.exit(0)

    print(f"\nШаг 2: Фильтрация VCF-файла '{args.vcf_file}' по {len(target_genes)} целевым генам с помощью VcfFilter...", file=sys.stderr)
    vcf_filter = VcfFilter(
        vcf_file_path=args.vcf_file,
        target_genes=target_genes,
        ann_tag=args.ann_tag,
        gene_name_index=args.gene_idx
    )

    vcf_filter.process_and_output(
        output_file_path=args.output_file
    )

    print("\n--- Процесс фильтрации VCF завершен ---", file=sys.stderr)

if __name__ == "__main__":
    main()
