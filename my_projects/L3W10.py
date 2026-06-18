# 10. DateTime (форматирование строк)
from datetime import datetime

def format_datetime(dt):
    months = {
        1: "января", 2: "февраля", 3: "марта", 4: "апреля",
        5: "мая", 6: "июня", 7: "июля", 8: "августа",
        9: "сентября", 10: "октября", 11: "ноября", 12: "декабря"
    }
    
    day = dt.day
    month = months[dt.month]
    year = dt.year
    time = dt.strftime("%H:%M")
    
    return f"Сегодня {day} {month} {year} года, время: {time}"

print("10. Форматирование даты и времени:")
formatted_date = format_datetime(datetime.now())
print(formatted_date)