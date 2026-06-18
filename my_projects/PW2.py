# Практическая работа 2 - Интерактивная версия
# Декораторы в Python

import sys

# ===== 1. ДЕКОРАТОР ЛОГИРОВАНИЯ =====

def logger(func):
    def wrapper(*args, **kwargs):
        print(f"🎯 Вызов функции {func.__name__} с аргументами {args} и {kwargs}")
        result = func(*args, **kwargs)
        print(f"📝 Функция {func.__name__} вернула {result}")
        return result
    return wrapper

# Функции с декоратором логирования
@logger
def add(a, b):
    return a + b

@logger
def divide(a, b):
    if b == 0:
        return "Ошибка: деление на ноль"
    return a / b

@logger
def greet(name):
    return f"Привет, {name}!"

# ===== 2. ДЕКОРАТОР ДОСТУПА =====

def require_role(allowed_roles):
    def decorator(func):
        def wrapper(user, *args, **kwargs):
            if user.get('role') in allowed_roles:
                return func(user, *args, **kwargs)
            else:
                print(f"🚫 Доступ запрещён пользователю {user['name']}")
                return None
        return wrapper
    return decorator

# Функции с декоратором доступа
@require_role(['admin'])
def delete_database(user):
    print(f"🗑️ База данных удалена пользователем {user['name']}")

@require_role(['admin', 'manager'])
def edit_settings(user):
    print(f"⚙️ Настройки изменены пользователем {user['name']}")

@require_role(['user', 'admin', 'manager'])
def view_data(user):
    print(f"👁️ Данные просмотрены пользователем {user['name']}")

# ===== ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ =====

def clear_screen():
    """Очистка экрана"""
    print("\n" * 50)

def print_menu():
    """Вывод главного меню"""
    print("=" * 60)
    print("          ПРАКТИЧЕСКАЯ РАБОТА 2 - ДЕКОРАТОРЫ")
    print("=" * 60)
    print("1. 🎯 Тестирование декоратора логирования")
    print("2. 🚪 Тестирование декоратора доступа")
    print("3. 🔄 Комбинирование декораторов")
    print("4. 📋 Показать код декораторов")
    print("0. ❌ Выход")
    print("=" * 60)

def test_logger_interactive():
    """Интерактивное тестирование декоратора логирования"""
    clear_screen()
    print("🎯 ТЕСТИРОВАНИЕ ДЕКОРАТОРА ЛОГИРОВАНИЯ")
    print("-" * 50)
    
    while True:
        print("\nДоступные функции:")
        print("1. ➕ Сложение (add)")
        print("2. ➗ Деление (divide)")
        print("3. 👋 Приветствие (greet)")
        print("0. ↩️ Назад")
        
        choice = input("\nВыберите функцию: ").strip()
        
        if choice == '1':
            try:
                a = float(input("Введите первое число: "))
                b = float(input("Введите второе число: "))
                print(f"\nРезультат: {add(a, b)}")
            except ValueError:
                print("❌ Ошибка: введите числа!")
                
        elif choice == '2':
            try:
                a = float(input("Введите делимое: "))
                b = float(input("Введите делитель: "))
                print(f"\nРезультат: {divide(a, b)}")
            except ValueError:
                print("❌ Ошибка: введите числа!")
                
        elif choice == '3':
            name = input("Введите имя: ")
            print(f"\nРезультат: {greet(name)}")
            
        elif choice == '0':
            break
        else:
            print("❌ Неверный выбор!")

def test_access_interactive():
    """Интерактивное тестирование декоратора доступа"""
    clear_screen()
    print("🚪 ТЕСТИРОВАНИЕ ДЕКОРАТОРА ДОСТУПА")
    print("-" * 50)
    
    # Предопределенные пользователи
    users = [
        {'name': 'Иван', 'role': 'admin'},
        {'name': 'Мария', 'role': 'manager'},
        {'name': 'Петр', 'role': 'user'},
        {'name': 'Анна', 'role': 'guest'}
    ]
    
    while True:
        print("\nВыберите пользователя:")
        for i, user in enumerate(users, 1):
            print(f"{i}. 👤 {user['name']} (роль: {user['role']})")
        print("5. 👤 Создать своего пользователя")
        print("0. ↩️ Назад")
        
        choice = input("\nВыберите пользователя: ").strip()
        
        if choice in ['1', '2', '3', '4']:
            user = users[int(choice) - 1]
            test_user_actions(user)
            
        elif choice == '5':
            user = create_custom_user()
            if user:
                test_user_actions(user)
                
        elif choice == '0':
            break
        else:
            print("❌ Неверный выбор!")

def create_custom_user():
    """Создание пользовательского пользователя"""
    print("\nСоздание пользователя:")
    name = input("Введите имя: ").strip()
    if not name:
        print("❌ Имя не может быть пустым!")
        return None
        
    print("Доступные роли: admin, manager, user, guest")
    role = input("Введите роль: ").strip().lower()
    if role not in ['admin', 'manager', 'user', 'guest']:
        print("❌ Неверная роль!")
        return None
        
    return {'name': name, 'role': role}

def test_user_actions(user):
    """Тестирование действий для конкретного пользователя"""
    print(f"\n👤 Тестирование для пользователя: {user['name']} (роль: {user['role']})")
    print("-" * 40)
    
    actions = [
        ("🗑️ Удалить базу данных", delete_database),
        ("⚙️ Изменить настройки", edit_settings),
        ("👁️ Просмотреть данные", view_data)
    ]
    
    for i, (desc, func) in enumerate(actions, 1):
        print(f"{i}. {desc}")
    print("0. ↩️ Назад")
    
    while True:
        choice = input("\nВыберите действие: ").strip()
        if choice == '1':
            delete_database(user)
        elif choice == '2':
            edit_settings(user)
        elif choice == '3':
            view_data(user)
        elif choice == '0':
            break
        else:
            print("❌ Неверный выбор!")

def test_combined_decorators():
    """Тестирование комбинированных декораторов"""
    clear_screen()
    print("🔄 КОМБИНИРОВАНИЕ ДЕКОРАТОРОВ")
    print("-" * 50)
    
    # Создаем функцию с обоими декораторами
    @logger
    @require_role(['admin'])
    def secure_operation(user):
        result = f"Безопасная операция выполнена пользователем {user['name']}"
        print(f"✅ {result}")
        return result
    
    print("Создана функция secure_operation с двумя декораторами:")
    print("@logger")
    print("@require_role(['admin'])")
    print("\nЭта функция будет:")
    print("1. 🎯 Логировать все вызовы")
    print("2. 🚪 Проверять права доступа")
    
    users = [
        {'name': 'Админ', 'role': 'admin'},
        {'name': 'Обычный пользователь', 'role': 'user'}
    ]
    
    for user in users:
        input(f"\nНажмите Enter для тестирования с пользователем {user['name']}...")
        print(f"\n👤 Пользователь: {user['name']} (роль: {user['role']})")
        result = secure_operation(user)
        if result:
            print(f"📊 Финальный результат: {result}")

def show_code():
    """Показать код декораторов"""
    clear_screen()
    print("📋 КОД ДЕКОРАТОРОВ")
    print("=" * 60)
    
    print("\n1. 🎯 ДЕКОРАТОР ЛОГИРОВАНИЯ:")
    print("""```python
def logger(func):
    def wrapper(*args, **kwargs):
        print(f"Вызов функции {func.__name__} с аргументами {args} и {kwargs}")
        result = func(*args, **kwargs)
        print(f"Функция {func.__name__} вернула {result}")
        return result
    return wrapper
```""")
    
    print("\n2. 🚪 ДЕКОРАТОР ДОСТУПА:")
    print("""```python
def require_role(allowed_roles):
    def decorator(func):
        def wrapper(user, *args, **kwargs):
            if user.get('role') in allowed_roles:
                return func(user, *args, **kwargs)
            else:
                print(f"Доступ запрещён пользователю {user['name']}")
                return None
        return wrapper
    return decorator
```""")
    
    input("\nНажмите Enter для возврата в меню...")

# ===== ГЛАВНАЯ ПРОГРАММА =====

def main():
    """Главная функция программы"""
    while True:
        clear_screen()
        print_menu()
        
        choice = input("Выберите пункт меню: ").strip()
        
        if choice == '1':
            test_logger_interactive()
        elif choice == '2':
            test_access_interactive()
        elif choice == '3':
            test_combined_decorators()
        elif choice == '4':
            show_code()
        elif choice == '0':
            print("\n👋 До свидания!")
            break
        else:
            print("❌ Неверный выбор! Попробуйте снова.")
            input("Нажмите Enter для продолжения...")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Программа завершена пользователем!")
        sys.exit(0)