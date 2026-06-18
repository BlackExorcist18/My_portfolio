#!/usr/bin/env python3
"""Тестовый скрипт для проверки документации."""

from nancy import loader, engine, results, commands

def test_documentation():
    """Проверяет доступность документации для всех модулей."""
    
    print("=" * 60)
    print("ТЕСТИРОВАНИЕ ДОКУМЕНТАЦИИ")
    print("=" * 60)
    
    # Проверка модуля loader
    print("\n1. Модуль loader:")
    print(help(loader))
    
    print("\n2. Функция load_tests:")
    print(help(loader.load_tests))
    
    print("\n3. Функция save_tests:")
    print(help(loader.save_tests))
    
    # Проверка класса QuizEngine
    print("\n4. Класс QuizEngine:")
    print(help(engine.QuizEngine))
    
    print("\n5. Метод start_quiz:")
    print(help(engine.QuizEngine.start_quiz))
    
    # Проверка функций results
    print("\n6. Функция show_results:")
    print(help(results.show_results))
    
    print("\n7. Функция save_results:")
    print(help(results.save_results))
    
    # Проверка команд
    print("\n8. Функция setup_parser:")
    print(help(commands.setup_parser))

if __name__ == "__main__":
    test_documentation()