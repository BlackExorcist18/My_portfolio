# 8. DateTime (текущая дата и время)
from datetime import datetime

print("8. Текущая дата и время:")
current_datetime = datetime.now()
print(f"Текущая дата и время: {current_datetime}")
print(f"Только текущая дата: {current_datetime.date()}")
print(f"Только текущее время: {current_datetime.time()}")