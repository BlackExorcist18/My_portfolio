"""Конфигурация базы данных для системы тестирования."""

import os
from typing import Dict, Any


def get_database_config() -> Dict[str, Any]:
    """Получить конфигурацию базы данных из переменных окружения.
    
    Returns:
        Dict[str, Any]: Словарь с настройками подключения к БД.
    """
    # Попробуем загрузить из .env файла
    try:
        from dotenv import load_dotenv
        load_dotenv()
        print("✅ .env файл загружен")
    except ImportError:
        print("⚠️  dotenv не установлен, используем системные переменные окружения")
    
    # URL подключения к PostgreSQL
    database_url = os.getenv(
        'DATABASE_URL',
        'postgresql://quiz_user:quiz_password@localhost:5432/quiz_system'
    )
    
    # Настройки подключения
    config = {
        'host': os.getenv('DB_HOST', 'localhost'),
        'port': os.getenv('DB_PORT', '5432'),
        'database': os.getenv('DB_NAME', 'quiz_system'),
        'user': os.getenv('DB_USER', 'quiz_user'),
        'password': os.getenv('DB_PASSWORD', 'quiz_password'),
        'database_url': database_url
    }
    
    print(f"🔧 Конфигурация БД: {config['host']}:{config['port']}/{config['database']}")
    return config


def get_database_url() -> str:
    """Получить URL подключения к базе данных.
    
    Returns:
        str: URL для подключения к PostgreSQL.
    """
    return get_database_config()['database_url']