"""Модуль для глобальной сессии базы данных."""

from .database import DatabaseManager

# Глобальный менеджер БД
db_manager = None

def get_db_manager() -> DatabaseManager:
    """Получить глобальный менеджер базы данных.
    
    Returns:
        DatabaseManager: Менеджер базы данных.
        
    Raises:
        RuntimeError: Если база данных не инициализирована.
    """
    if db_manager is None:
        raise RuntimeError("База данных не инициализирована. Вызовите init_database() сначала.")
    return db_manager

def set_db_manager(manager: DatabaseManager) -> None:
    """Установить глобальный менеджер базы данных.
    
    Args:
        manager (DatabaseManager): Менеджер базы данных.
    """
    global db_manager
    db_manager = manager