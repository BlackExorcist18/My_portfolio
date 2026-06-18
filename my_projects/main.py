print('hello, GitHub')
# Лабораторная работа №2 - Все задания в одном файле

# ===== ЗАДАНИЯ 1.1-1.5 (Циклы) =====

def multiplication_table():
    """Л2З1.1 - Таблица умножения"""
    print("Таблица умножения:")
    for i in range(1, 10):
        for j in range(1, 10):
            print(f"{i}×{j}={i*j}\t", end="")
        print()

def sum_odd_numbers():
    """Л2З1.2 - Сумма нечётных чисел от 1 до 100"""
    sum_odd = 0
    for i in range(1, 101, 2):
        sum_odd += i
    print(f"Сумма нечётных чисел от 1 до 100: {sum_odd}")

def find_divisors():
    """Л2З1.3 - Нахождение делителей числа"""
    n = int(input("Введите число: "))
    print(f"Делители числа {n}:")
    for i in range(1, n + 1):
        if n % i == 0:
            print(i, end=" ")
    print()

def factorial():
    """Л2З1.4 - Вычисление факториала"""
    n = int(input("Введите число: "))
    factorial = 1
    for i in range(1, n + 1):
        factorial *= i
    print(f"Факториал числа {n} = {factorial}")

def fibonacci_sequence():
    """Л2З1.5 - Последовательность Фибоначчи"""
    n = int(input("Введите длину последовательности: "))
    fibonacci = [0, 1]
    for i in range(2, n):
        next_num = fibonacci[i-1] + fibonacci[i-2]
        fibonacci.append(next_num)
    print(f"Последовательность Фибоначчи: {fibonacci[:n]}")

# ===== ЗАДАНИЯ 2.1 (Списки) =====

def list_operations():
    """Л2З2.1 - Операции со списками"""
    import random
    numbers = [random.randint(-50, 50) for _ in range(10)]
    print(f"Сгенерированный список: {numbers}")
    
    even_numbers = [x for x in numbers if x % 2 == 0]
    print(f"Чётные элементы: {even_numbers}")
    print(f"Максимальное число: {max(numbers)}")
    print(f"Минимальное число: {min(numbers)}")
    
    user_numbers = []
    for i in range(5):
        num = int(input(f"Введите число {i+1}: "))
        user_numbers.append(num)
    user_numbers.sort()
    print(f"Отсортированный список: {user_numbers}")
    
    unique_list = []
    for num in numbers:
        if num not in unique_list:
            unique_list.append(num)
    print(f"Список без дубликатов: {unique_list}")
    
    if len(numbers) > 1:
        numbers[0], numbers[-1] = numbers[-1], numbers[0]
    print(f"Список после замены: {numbers}")

# ===== ЗАДАНИЯ 3.1-3.4 (Словари) =====

def student_grades():
    """Л2З3.1 - Средний балл студентов"""
    students = {"Вася": 4.5, "Гоша": 4.8, "Кузя": 3.9, "Антон": 5.0}
    average = sum(students.values()) / len(students)
    print(f"Средний балл: {average:.2f}")

def letter_count():
    """Л2З3.2 - Подсчёт букв в строке"""
    text = input("Введите строку: ")
    letter_count_dict = {}
    for char in text:
        if char != ' ':
            letter_count_dict[char] = letter_count_dict.get(char, 0) + 1
    print(f"Количество букв: {letter_count_dict}")

def squares_dict():
    """Л2З3.3 - Словарь квадратов чисел"""
    squares = {x: x*x for x in range(1, 11)}
    print(f"Квадраты чисел: {squares}")

def zip_dict():
    """Л2З3.4 - Объединение списков в словарь"""
    keys = ['a', 'b', 'c', 'd']
    values = [1, 2, 3, 4]
    combined_dict = dict(zip(keys, values))
    print(f"Объединённый словарь: {combined_dict}")

# ===== ЗАДАНИЯ 4.1-4.5 (Множества) =====

def set_operations():
    """Л2З4.1 - Операции с множествами"""
    set1 = {1, 2, 3, 4, 5}
    set2 = {4, 5, 6, 7, 8}
    print(f"Пересечение: {set1 & set2}")
    print(f"Объединение: {set1 | set2}")

def unique_words():
    """Л2З4.2 - Уникальные слова в тексте"""
    text = input("Введите текст: ")
    words = text.lower().split()
    unique_words_set = set(words)
    print(f"Уникальные слова: {unique_words_set}")

def common_elements():
    """Л2З4.3 - Общие элементы двух списков"""
    list1 = [1, 2, 3, 4, 5]
    list2 = [4, 5, 6, 7, 8]
    common = set(list1) & set(list2)
    print(f"Общие элементы: {common}")

def subset_check():
    """Л2З4.4 - Проверка подмножества"""
    set_a = {1, 2, 3}
    set_b = {1, 2, 3, 4, 5}
    print(f"set_a является подмножеством set_b: {set_a.issubset(set_b)}")

def filter_set():
    """Л2З4.5 - Фильтрация множества"""
    number_set = {1, 5, 10, 15, 20}
    threshold = int(input("Введите число: "))
    filtered_set = {x for x in number_set if x >= threshold}
    print(f"Отфильтрованное множество: {filtered_set}")

# ===== ЗАДАНИЯ 5.1-5.8 (Комбинированные структуры) =====

def unique_values():
    """Л2З5.1 - Уникальные значения в списке"""
    import random
    numbers = [random.randint(1, 10) for _ in range(20)]
    print(f"Исходный список: {numbers}")
    
    unique_numbers = []
    for i in range(len(numbers)):
        current_number = numbers[i]
        count = 0
        for j in range(len(numbers)):
            if numbers[j] == current_number:
                count += 1
        if count == 1:
            unique_numbers.append(current_number)
    
    print(f"Уникальные значения: {unique_numbers}")

def frequency_dict():
    """Л2З5.2 - Словарь частот"""
    import random
    numbers = [random.randint(1, 10) for _ in range(15)]
    print(f"Исходный список: {numbers}")
    
    frequency_dict = {}
    for num in numbers:
        frequency_dict[num] = frequency_dict.get(num, 0) + 1
    
    print(f"Частоты элементов: {frequency_dict}")

def long_words_set():
    """Л2З5.3 - Множество длинных слов"""
    words = ["компьютер","компьютер", "программа", "алгоритм", "данные", "код", "язык", "разработка", "искусственный", "интеллект", "машинное", "обучение"]
    print(f"Исходный список слов: {words}")
    
    long_words = {word for word in words if len(word) > 5}
    print(f"Слова длиннее 5 символов: {long_words}")

def word_count():
    """Л2З5.4 - Подсчёт слов в предложении"""
    sentence = input("Введите предложение: ").lower()
    print(f"Введенное предложение: {sentence}")
    
    word_count_dict = {}
    for word in sentence.split():
        word = word.strip('.,!?;:')
        if word:
            word_count_dict[word] = word_count_dict.get(word, 0) + 1
    
    print(f"Количество вхождений слов: {word_count_dict}")

def remove_duplicates():
    """Л2З5.5 - Удаление дубликатов"""
    duplicate_list = [1, 2, 2, 3, 4, 4, 5, 5, 5, 6, 7, 7, 8]
    print(f"Исходный список с дубликатами: {duplicate_list}")
    
    unique_list = list(set(duplicate_list))
    print(f"Список без дубликатов: {unique_list}")

def most_expensive_product():
    """Л2З5.6 - Самый дорогой товар"""
    products = {
        "ноутбук": 45000, 
        "смартфон": 25000, 
        "наушники": 5000, 
        "планшет": 35000,
        "монитор": 15000,
        "клавиатура": 3000
    }
    print("Товары и цены:")
    for product, price in products.items():
        print(f"  {product}: {price} руб.")
    
    most_expensive = max(products, key=products.get)
    print(f"\nСамый дорогой товар: {most_expensive} ({products[most_expensive]} руб.)")

def name_frequency():
    """Л2З5.7 - Частота имен"""
    names = ["Алексей", "Екатерина", "Дмитрий", "София", "Алексей", "Екатерина", "Алексей", "Михаил", "Дмитрий", "София", "Михаил", "Алексей"]
    print(f"Исходный список имен: {names}")
    
    name_count = {}
    for name in names:
        name_count[name] = name_count.get(name, 0) + 1
    
    repeated_names = [name for name, count in name_count.items() if count > 1]
    most_common = max(name_count, key=name_count.get)
    
    print(f"Повторяющиеся имена: {repeated_names}")
    print(f"Самое частое имя: '{most_common}' (встречается {name_count[most_common]} раз)")
    print(f"Статистика по всем именам: {name_count}")

def first_occurrence():
    """Л2З5.8 - Первые вхождения символов"""
    text = input("Введите строку: ")
    print(f"Введенная строка: '{text}'")
    
    first_occurrence_dict = {}
    for index, char in enumerate(text):
        if char not in first_occurrence_dict:
            first_occurrence_dict[char] = index
    
    print("Первые вхождения символов:")
    for char, position in first_occurrence_dict.items():
        print(f"  '{char}': позиция {position}")

# ===== ГЛАВНОЕ МЕНЮ =====

def main():
    """Главная функция с меню выбора заданий"""
    while True:
        print("\n" + "="*50)
        print("ЛАБОРАТОРНАЯ РАБОТА №2 - ВСЕ ЗАДАНИЯ")
        print("="*50)
        print("1. Задания 1.1-1.5 (Циклы)")
        print("2. Задание 2.1 (Списки)")
        print("3. Задания 3.1-3.4 (Словари)")
        print("4. Задания 4.1-4.5 (Множества)")
        print("5. Задания 5.1-5.8 (Комбинированные структуры)")
        print("0. Выход")
        print("="*50)
        
        choice = input("Выберите группу заданий: ")
        
        if choice == "1":
            print("\n--- ЗАДАНИЯ 1.1-1.5 (ЦИКЛЫ) ---")
            print("1.1 - Таблица умножения")
            print("1.2 - Сумма нечётных чисел")
            print("1.3 - Делители числа")
            print("1.4 - Факториал")
            print("1.5 - Последовательность Фибоначчи")
            sub_choice = input("Выберите задание (1.1-1.5): ")
            
            if sub_choice == "1.1":
                multiplication_table()
            elif sub_choice == "1.2":
                sum_odd_numbers()
            elif sub_choice == "1.3":
                find_divisors()
            elif sub_choice == "1.4":
                factorial()
            elif sub_choice == "1.5":
                fibonacci_sequence()
                
        elif choice == "2":
            print("\n--- ЗАДАНИЕ 2.1 (СПИСКИ) ---")
            list_operations()
            
        elif choice == "3":
            print("\n--- ЗАДАНИЯ 3.1-3.4 (СЛОВАРИ) ---")
            print("3.1 - Средний балл студентов")
            print("3.2 - Подсчёт букв")
            print("3.3 - Квадраты чисел")
            print("3.4 - Объединение списков")
            sub_choice = input("Выберите задание (3.1-3.4): ")
            
            if sub_choice == "3.1":
                student_grades()
            elif sub_choice == "3.2":
                letter_count()
            elif sub_choice == "3.3":
                squares_dict()
            elif sub_choice == "3.4":
                zip_dict()
                
        elif choice == "4":
            print("\n--- ЗАДАНИЯ 4.1-4.5 (МНОЖЕСТВА) ---")
            print("4.1 - Операции с множествами")
            print("4.2 - Уникальные слова")
            print("4.3 - Общие элементы")
            print("4.4 - Проверка подмножества")
            print("4.5 - Фильтрация множества")
            sub_choice = input("Выберите задание (4.1-4.5): ")
            
            if sub_choice == "4.1":
                set_operations()
            elif sub_choice == "4.2":
                unique_words()
            elif sub_choice == "4.3":
                common_elements()
            elif sub_choice == "4.4":
                subset_check()
            elif sub_choice == "4.5":
                filter_set()
                
        elif choice == "5":
            print("\n--- ЗАДАНИЯ 5.1-5.8 (КОМБИНИРОВАННЫЕ) ---")
            print("5.1 - Уникальные значения")
            print("5.2 - Словарь частот")
            print("5.3 - Длинные слова")
            print("5.4 - Подсчёт слов")
            print("5.5 - Удаление дубликатов")
            print("5.6 - Самый дорогой товар")
            print("5.7 - Частота имен")
            print("5.8 - Первые вхождения")
            sub_choice = input("Выберите задание (5.1-5.8): ")
            
            if sub_choice == "5.1":
                unique_values()
            elif sub_choice == "5.2":
                frequency_dict()
            elif sub_choice == "5.3":
                long_words_set()
            elif sub_choice == "5.4":
                word_count()
            elif sub_choice == "5.5":
                remove_duplicates()
            elif sub_choice == "5.6":
                most_expensive_product()
            elif sub_choice == "5.7":
                name_frequency()
            elif sub_choice == "5.8":
                first_occurrence()
                
        elif choice == "0":
            print("Выход из программы...")
            break
        else:
            print("Неверный выбор! Попробуйте снова.")

if __name__ == "__main__":
    main()