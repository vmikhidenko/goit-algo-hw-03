import os
import shutil
import argparse
from pathlib import Path
import sys
import fnmatch

# Список системних файлів та директорій для ігнорування
IGNORE_FILES = {
    '.DS_Store',        # macOS
    'Thumbs.db',        # Windows
    'desktop.ini',      # Windows
    'ehthumbs.db',      # Windows
    'Icon\r',           # macOS
    '._*.swp',          # macOS та інші
}

IGNORE_DIRS = {
    '__pycache__',
    '.git',
    '.svn',
    '.hg',
    '.idea',
    '.vscode',
}

def parse_arguments():
    """
    Парсинг аргументів командного рядка.
    Повертає шлях до вихідної директорії, шлях до директорії призначення та прапорець тесту.
    """
    parser = argparse.ArgumentParser(description="Рекурсивно копіює файли та сортує їх за розширеннями, ігноруючи системні файли.")
    parser.add_argument("source", type=str, nargs='?', help="Шлях до вихідної директорії.")
    parser.add_argument("destination", nargs='?', default=None, type=str, help="Шлях до директорії призначення.")
    parser.add_argument("--test", action="store_true", help="Запустити тестове копіювання на визначеній директорії.")
    args = parser.parse_args()
    return args.source, args.destination, args.test

def is_ignored(file_or_dir: Path) -> bool:
    """
    Перевіряє, чи є файл або директорія системним або схованим і повинен бути ігнорований.

    :param file_or_dir: Path об'єкт файлу або директорії.
    :return: True, якщо файл або директорія повинні бути ігноровані, інакше False.
    """
    name = file_or_dir.name

    # Ігнорування схованих файлів та директорій (починаються з крапки)
    if name.startswith('.'):
        return True

    # Ігнорування специфічних файлів
    if name in IGNORE_FILES:
        return True

    # Додавання підтримки шаблонів (наприклад, '._*.swp')
    for pattern in IGNORE_FILES:
        if '*' in pattern:
            if fnmatch.fnmatch(name, pattern):
                return True

    return False

def copy_file(file_path: Path, destination_root: Path):
    """
    Копіює файл у відповідну піддиректорію за розширенням.

    :param file_path: Path об'єкт вихідного файлу.
    :param destination_root: Path об'єкт кореневої директорії призначення.
    """
    try:
        if file_path.is_file():
            # Отримуємо розширення файлу без крапки, якщо воно є
            extension = file_path.suffix[1:].lower() if file_path.suffix else "no_extension"
            # Створюємо піддиректорію за розширенням
            target_dir = destination_root / extension
            target_dir.mkdir(parents=True, exist_ok=True)
            # Копіюємо файл до цільової директорії
            shutil.copy2(file_path, target_dir / file_path.name)
            print(f"Скопійовано: {file_path} -> {target_dir / file_path.name}")
    except Exception as e:
        print(f"Помилка при копіюванні файлу '{file_path}': {e}")

def recursive_copy(source_dir: Path, destination_root: Path):
    """
    Рекурсивно перебирає директорію, копіює файли до директорії призначення,
    сортує їх у піддиректорії за розширенням файлів, ігноруючи системні файли.

    :param source_dir: Path об'єкт вихідної директорії.
    :param destination_root: Path об'єкт кореневої директорії призначення.
    """
    try:
        for item in source_dir.iterdir():
            if is_ignored(item):
                print(f"Ігноровано: {item} (системний або схований файл/директорія)")
                continue

            if item.is_dir():
                if item.name in IGNORE_DIRS:
                    print(f"Ігноровано директорію: {item} (системна директорія)")
                    continue
                # Рекурсивно обробляємо піддиректорію
                recursive_copy(item, destination_root)
            elif item.is_file():
                # Копіюємо файл
                copy_file(item, destination_root)
            else:
                print(f"Ігноровано: {item} (не файл і не директорія)")
    except PermissionError as pe:
        print(f"Недостатньо прав доступу до '{source_dir}': {pe}")
    except Exception as e:
        print(f"Помилка при обробці '{source_dir}': {e}")

def copy_and_sort_files(source: str, destination: str):
    """
    Початкова функція для копіювання та сортування файлів.

    :param source: Шлях до вихідної директорії.
    :param destination: Шлях до директорії призначення.
    """
    source_path = Path(source).resolve()
    destination_path = Path(destination).resolve()

    # Перевірка наявності вихідної директорії
    if not source_path.exists():
        print(f"Вихідна директорія '{source_path}' не існує.")
        sys.exit(1)

    if not source_path.is_dir():
        print(f"Вказаний вихідний шлях '{source_path}' не є директорією.")
        sys.exit(1)

    # Створюємо директорію призначення, якщо вона не існує
    try:
        destination_path.mkdir(parents=True, exist_ok=True)
    except Exception as e:
        print(f"Не вдалося створити директорію призначення '{destination_path}': {e}")
        sys.exit(1)

    # Починаємо рекурсивне копіювання
    recursive_copy(source_path, destination_path)

def test_copy():
    """
    Тестова функція для копіювання файлів з визначеної директорії.
    """
    test_source = "/Users/volodymyrmikhidenko/Documents/Previous hw/project-DreamTeam15/Project"
    test_destination = "/Users/volodymyrmikhidenko/Documents/Previous hw/project-DreamTeam15/dist_test"

    print(f"Тестове копіювання з '{test_source}' до '{test_destination}'")

    # Очищуємо директорію призначення перед копіюванням, якщо вона існує
    if Path(test_destination).exists():
        try:
            shutil.rmtree(test_destination)
            print(f"Очищено директорію призначення '{test_destination}' перед тестом.")
        except Exception as e:
            print(f"Не вдалося очистити директорію призначення '{test_destination}': {e}")
            sys.exit(1)

    copy_and_sort_files(test_source, test_destination)
    print("Тестове копіювання завершено.")

def main():
    source, destination, is_test = parse_arguments()
    if is_test:
        test_copy()
    else:
        if not source:
            print("Не вказано вихідну директорію. Використовуйте --help для отримання інформації.")
            sys.exit(1)
        if not destination:
            destination = "dist"  # За замовчуванням 'dist' якщо не вказано
        copy_and_sort_files(source, destination)

if __name__ == "__main__":
    main()

"""
Для тесту взято проєкт з минулих домашніх завдань, скрипт відсортував всі основні файли, відсортував їх по відповідних директоріях, а також - проігнорував всі системні файли
"""

"""
Тестовий промпт:

/usr/local/bin/python3 "/Users/volodymyrmikhidenko/Documents/Previous hw/project-DreamTeam15/Task1.py" "/Users/volodymyrmikhidenko/Documents/Previous hw/project-DreamTeam15/Project" "/Users/volodymyrmikhidenko/Documents/Previous hw/project-DreamTeam15/dist"
"""
