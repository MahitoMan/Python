# oop_vcf_parser.py
"""
Модуль для парсинга и фильтрации VCF-файлов.
Фильтрует варианты по списку целевых генов.
"""
import sys
from typing import Set, Iterator, Optional, List, Tuple

# Импорт вспомогательной функции
try:
    from utils import safe_open
except ImportError as e:
    print(f"Ошибка импорта модуля: {e}. Убедитесь, что utils.py "
          "находится в том же каталоге или доступен в PYTHONPATH.", file=sys.stderr)
    sys.exit(1)

class VcfFilter:
    """
    Класс для фильтрации VCF-файлов на основе списка целевых генов.
    """
    def __init__(
        self,
        vcf_file_path: str,
        target_genes: Set[str],
        ann_tag: str = "ANN",
        gene_name_index: int = 3
    ):
        """
        Инициализация фильтра VCF.

        Args:
            vcf_file_path: Путь к VCF-файлу.
            target_genes: Множество целевых генов для фильтрации.
            ann_tag: Тег в поле INFO, содержащий аннотации генов.
            gene_name_index: Индекс имени гена в строке аннотации.
        """
        self.vcf_file_path: str = vcf_file_path
        self.target_genes: Set[str] = target_genes
        self.ann_tag: str = ann_tag
        self.gene_name_index: int = gene_name_index
        self._filtered_variant_info: List[Tuple[str, str, str, str]] = [] # Хранение информации об отобранных вариантах

    def _extract_genes_from_info(self, info_field: str) -> Set[str]:
        """
        Извлечение уникальных имен генов из поля INFO VCF-файла.

        Args:
            info_field: Строка поля INFO из VCF.

        Returns:
            Множество (set) строковых имен генов.
        """
        genes: Set[str] = set()
        info_entries: List[str] = info_field.split(';')
        tag_to_find: str = self.ann_tag + '='

        for entry in info_entries:
            if entry.startswith(tag_to_find):
                annotations_concatenated: str = entry[len(tag_to_find):]
                individual_annotations: List[str] = annotations_concatenated.split(',')
                for annotation_str in individual_annotations:
                    fields: List[str] = annotation_str.split('|')
                    if len(fields) > self.gene_name_index and fields[self.gene_name_index]:
                        gene_name_full: str = fields[self.gene_name_index]
                        gene_name_base: str = gene_name_full.split('.')[0]
                        if gene_name_base:
                            genes.add(gene_name_base)
        return genes

    def _generate_filtered_vcf_lines(self) -> Iterator[str]:
        """
        Генератор отфильтрованных строк VCF.
        Читает VCF, фильтрует по целевым генам и выдает строки.
        Собирает информацию об отобранных вариантах.

        Yields:
            Строка из VCF-файла.
        """
        processed_variants_count: int = 0
        matched_variants_count: int = 0
        current_line_number: int = 0

        self._filtered_variant_info = [] # Очистка списка перед обработкой

        print(f"Чтение и фильтрация VCF файла: {self.vcf_file_path}", file=sys.stderr)
        try:
            with safe_open(self.vcf_file_path, 'r') as vcf_file:
                for current_line_number, line_content in enumerate(vcf_file, 1):
                    line: str = line_content.strip()
                    if not line:
                        continue

                    if line.startswith('##') or line.startswith('#CHROM'):
                        yield line
                        continue

                    processed_variants_count += 1
                    fields: List[str] = line.split('\t')

                    min_vcf_fields: int = 8
                    if len(fields) < min_vcf_fields:
                        print(f"Предупреждение (строка {current_line_number}): Пропущена строка с некорректным форматом VCF (ожидается минимум {min_vcf_fields} полей): {line[:100]}...", file=sys.stderr)
                        continue

                    info_field: str = fields[7]
                    variant_genes: Set[str] = self._extract_genes_from_info(info_field)

                    if not self.target_genes.isdisjoint(variant_genes):
                        yield line
                        matched_variants_count +=1
                        chrom = fields[0]
                        pos = fields[1]
                        id_field = fields[2] if fields[2] != '.' else '.'
                        intersecting_genes = sorted(list(variant_genes.intersection(self.target_genes)))
                        genes_str = ", ".join(intersecting_genes) if intersecting_genes else "N/A"
                        self._filtered_variant_info.append((chrom, pos, id_field, genes_str))

        except FileNotFoundError:
            return
        except IOError:
            return
        except Exception as e:
            print(f"Критическая ошибка при обработке VCF-файла '{self.vcf_file_path}' (строка ~{current_line_number}): {e}", file=sys.stderr)
            return

        print(f"Обработано вариантов в VCF: {processed_variants_count}", file=sys.stderr)
        print(f"Найдено вариантов, аннотированных на целевые гены: {matched_variants_count}", file=sys.stderr)


    def process_and_output(self, output_file_path: Optional[str]) -> None:
        """
        Обрабатывает VCF и выводит результат.
        Выводит список отобранных вариантов с генами в stderr.
        """
        lines_written_or_printed: int = 0

        filtered_lines_generator: Iterator[str] = self._generate_filtered_vcf_lines()

        try:
            if output_file_path:
                with safe_open(output_file_path, 'w') as outfile:
                    for line in filtered_lines_generator:
                        outfile.write(line + '\n')
                        lines_written_or_printed +=1
                if lines_written_or_printed > 0 :
                     print(f"Отфильтрованный VCF сохранен в: {output_file_path}", file=sys.stderr)
                else:
                     print(f"В VCF файле '{self.vcf_file_path}' не найдено вариантов, соответствующих критериям, для записи в файл.", file=sys.stderr)
            else:
                for line in filtered_lines_generator:
                    print(line)
                    lines_written_or_printed +=1
                if lines_written_or_printed == 0:
                     print(f"В VCF файле '{self.vcf_file_path}' не найдено вариантов, соответствующих критериям, для вывода в stdout.", file=sys.stderr)

        except IOError as e:
            print(f"Ошибка при записи в выходной файл '{output_file_path}': {e}", file=sys.stderr)
        except Exception as e:
            print(f"Неожиданная ошибка во время вывода результатов: {e}", file=sys.stderr)

        if self._filtered_variant_info:
            print("\n--- Список отобранных вариантов (CHROM:POS:ID - Гены) ---", file=sys.stderr)
            sorted_variants = sorted(self._filtered_variant_info, key=lambda x: (x[0], int(x[1]), x[3]))
            for variant in sorted_variants:
                 print(f"{variant[0]}:{variant[1]}:{variant[2]} - {variant[3]}", file=sys.stderr)
            print("----------------------------------------------------------", file=sys.stderr)
        elif lines_written_or_printed > 0:
             print("\n--- Варианты, соответствующие критериям, не найдены ---", file=sys.stderr)
             print("----------------------------------------------------------", file=sys.stderr)

# if __name__ == "__main__":
#     pass
