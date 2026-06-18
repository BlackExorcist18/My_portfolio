# 6. Decimal (точные вычисления)
from decimal import Decimal, getcontext

def deposit_calculator():
    # Устанавливаем точность вычислений
    getcontext().prec = 10
    
    # Ввод данных
    initial_amount = Decimal(input("\n6. Введите начальную сумму вклада (руб.): "))
    interest_rate = Decimal(input("Введите годовую процентную ставку (%): "))
    years = Decimal(input("Введите срок вклада (лет): "))
    
    # Расчет по формуле ежемесячной капитализации
    # S = P * (1 + r/(12*100))^(12*t)
    monthly_rate = interest_rate / Decimal('12') / Decimal('100')
    months = years * Decimal('12')
    final_amount = initial_amount * (1 + monthly_rate) ** months
    
    # Округляем до копеек (2 знака после запятой)
    final_amount = final_amount.quantize(Decimal('0.01'))
    profit = final_amount - initial_amount
    
    print(f"Итоговая сумма вклада: {final_amount} руб.")
    print(f"Общая прибыль: {profit} руб.")

# Запуск калькулятора вкладов
if __name__ == "__main__":
    deposit_calculator()