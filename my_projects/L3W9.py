# 9. DateTime (разница дат)
from datetime import date

print("9. Разница дат:")
# ЗАМЕНИТЕ на вашу дату рождения
birthday = date(2005, 7, 27)  # Пример: 15 мая 2000 года
today = date.today()

# Дней с момента рождения
days_passed = (today - birthday).days
print(f"Дней с момента рождения: {days_passed}")

# Следующий день рождения
next_birthday = date(today.year, birthday.month, birthday.day)
if next_birthday < today:
    next_birthday = date(today.year + 1, birthday.month, birthday.day)

days_to_birthday = (next_birthday - today).days
print(f"Дней до следующего дня рождения: {days_to_birthday}")