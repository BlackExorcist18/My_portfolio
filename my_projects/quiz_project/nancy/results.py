"""Модуль для работы с результатами тестирования."""

import json
from typing import Dict, Any
import datetime
from .db_session import get_db_manager


def show_results(results: Dict[str, Any]) -> None:
    """Отображает результаты тестирования в консоли."""
    print("\n" + "=" * 50)
    print("РЕЗУЛЬТАТЫ ТЕСТИРОВАНИЯ")
    print("=" * 50)
    print(f"Тест: {results['test_name']}")
    print(f"Правильных ответов: {results['score']} из {results['total_questions']}")
    print(f"Процент правильных ответов: {results['percentage']:.1f}%")
    
    if results['passed']:
        print("✅ ТЕСТ ПРОЙДЕН!")
    else:
        print("❌ ТЕСТ НЕ ПРОЙДЕН!")
    print("=" * 50)


def save_results(results: Dict[str, Any], filename: str = "results.json", use_database: bool = False) -> bool:
    """Сохраняет результаты тестирования."""
    if use_database:
        try:
            db_manager = get_db_manager()
            return db_manager.save_test_result(results)
        except RuntimeError:
            print("❌ База данных не инициализирована")
            return False
    else:
        return save_results_to_file(results, filename)


def save_results_to_file(results: Dict[str, Any], filename: str = "results.json") -> bool:
    """Сохраняет результаты тестирования в JSON файл."""
    try:
        # Загружаем существующие результаты
        try:
            with open(filename, 'r', encoding='utf-8') as file:
                all_results = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            all_results = []
        
        # Добавляем timestamp
        results_with_time = results.copy()
        results_with_time['timestamp'] = datetime.datetime.now().isoformat()
        
        all_results.append(results_with_time)
        
        # Сохраняем обратно
        with open(filename, 'w', encoding='utf-8') as file:
            json.dump(all_results, file, ensure_ascii=False, indent=2)
        
        print(f"Результаты сохранены в {filename}")
        return True
        
    except Exception as e:
        print(f"Ошибка при сохранении результатов: {e}")
        return False


def show_database_results(test_name: str = None, limit: int = 10) -> None:
    """Показывает результаты из базы данных."""
    try:
        db_manager = get_db_manager()
        results = db_manager.get_test_results(test_name, limit)
        
        print(f"\nИстория результатов (база данных):")
        print("=" * 60)
        for result in results:
            status = "✅ ПРОЙДЕН" if result['passed'] else "❌ НЕ ПРОЙДЕН"
            print(f"Тест: {result['test_name']}")
            print(f"Пользователь: {result['user_name']}")
            print(f"Результат: {result['score']}/{result['total_questions']} ({result['percentage']}%) - {status}")
            print(f"Время: {result['completed_at'].strftime('%Y-%m-%d %H:%M:%S')}")
            print("-" * 40)
    except RuntimeError:
        print("❌ База данных не инициализирована")