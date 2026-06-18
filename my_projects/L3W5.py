# 5. Собственный генератор
def fibonacci(n):
    a, b = 0, 1
    count = 0
    while count < n:
        yield a
        a, b = b, a + b
        count += 1

print("5. Числа Фибоначчи:")
for num in fibonacci(5):
    print(num, end=" ")
print()