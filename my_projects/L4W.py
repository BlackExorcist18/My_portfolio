# Лабораторная работа 4

# 1. Базовый класс
class Transport:
    def __init__(self, brand, speed):
        self.brand = brand
        self.speed = speed
    
    def move(self):
        print(f"Transport is moving at {self.speed} km/h")
    
    def __str__(self):
        return f"Transport: {self.brand}, Speed: {self.speed}"


# 2. Наследники
class Car(Transport):
    def __init__(self, brand, speed, seats):
        super().__init__(brand, speed)
        self.seats = seats
    
    def honk(self):
        print("Beep beep!")
    
    def move(self):
        print(f"Car {self.brand} is driving at {self.speed} km/h")
    
    def __str__(self):
        return f"Car: {self.brand}, Speed: {self.speed}, Seats: {self.seats}"
    
    # 3. Магические методы
    def __len__(self):
        return self.seats
    
    def __eq__(self, other):
        if isinstance(other, Car):
            return self.speed == other.speed
        return NotImplemented
    
    def __add__(self, other):
        if isinstance(other, Car):
            return self.speed + other.speed
        return NotImplemented


class Bike(Transport):
    def __init__(self, brand, speed, bike_type):
        super().__init__(brand, speed)
        self.type = bike_type
    
    def move(self):
        print(f"Bike {self.brand} is cycling at {self.speed} km/h")
    
    def __str__(self):
        return f"Bike: {self.brand}, Speed: {self.speed}, Type: {self.type}"


# 4. Практика использования
def main():
    print("=== ЛАБОРАТОРНАЯ РАБОТА 4 ===")
    
    # Создание объектов
    print("\n1. Создание объектов:")
    transport = Transport("Generic", 60)
    car1 = Car("Toyota", 120, 5)
    car2 = Car("Honda", 130, 4)
    bike = Bike("Giant", 25, "mountain")
    
    # Вывод объектов
    print("\n2. Вывод объектов (__str__):")
    print(transport)
    print(car1)
    print(car2)
    print(bike)
    
    # Проверка методов move() и honk()
    print("\n3. Проверка методов move() и honk():")
    transport.move()
    car1.move()
    bike.move()
    car1.honk()
    
    # Использование len(car)
    print(f"\n4. Количество мест в car1 (len(car1)): {len(car1)}")
    
    # Сравнение двух машин
    print(f"\n5. Сравнение car1 и car2 (car1 == car2): {car1 == car2}")
    
    # Сложение скоростей двух машин
    print(f"\n6. Сумма скоростей car1 + car2: {car1 + car2}")
    
    # Попытка сложить машину и велосипед
    print("\n7. Попытка сложить car1 и bike:")
    try:
        result = car1 + bike
        print(f"Результат: {result}")
    except TypeError as e:
        print(f"Ошибка: {e}")
        print("Объяснение: Сложение работает только между объектами Car, так как метод __add__ проверяет тип с помощью isinstance()")
    
    # 5. Дополнительное задание - полиморфизм
    print("\n8. Дополнительное задание - полиморфизм:")
    vehicles = [
        Transport("Generic", 60),
        Car("Toyota", 120, 5),
        Bike("Giant", 25, "mountain"),
        Car("BMW", 150, 4),
        Bike("Trek", 30, "road")
    ]
    
    print("Список транспортных средств:")
    for vehicle in vehicles:
        vehicle.move()
    
    print("\n9. Принцип ООП:")
    print("Демонстрируется принцип ПОЛИМОРФИЗМА:")
    print("- Разные объекты (Transport, Car, Bike) имеют метод move()")
    print("- Каждый объект выполняет move() по-своему")
    print("- Единый интерфейс для разных типов объектов")
    print("- Возможность работать с разными типами через общий интерфейс")
    print("- В цикле for мы вызываем move() для каждого объекта, не зная его конкретного типа")


if __name__ == "__main__":
    main()