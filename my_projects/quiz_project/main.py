#!/usr/bin/env python3
"""Главный файл системы тестирования (Quiz).

Этот модуль предоставляет точку входа в приложение системы тестирования.
Обрабатывает аргументы командной строки и запускает соответствующие команды.

Использование:
    python main.py list - показать тесты
    python main.py create - создать тест
    python main.py run "Название теста" - запустить тест
    python main.py results - показать результаты
"""

import argparse
import sys
from nancy.commands import setup_parser, handle_commands


def main():
    """Основная функция приложения.
    
    Настраивает парсер аргументов, обрабатывает команды 
    и управляет потоком выполнения приложения.
    """
    parser = setup_parser()
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    try:
        handle_commands(args)
    except KeyboardInterrupt:
        print("\n\nПрограмма прервана пользователем")
    except Exception as e:
        print(f"Произошла ошибка: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()