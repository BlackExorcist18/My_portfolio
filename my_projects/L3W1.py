# 1. List comprehension (простое преобразование!)
squares = [x**2 for x in range(1, 11)]
print("1. Квадраты чисел от 1 до 10:", squares)
x = []
for i in range(1,11):
    x.append(i**2)
print(x)