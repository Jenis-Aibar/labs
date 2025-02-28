import math
import time
from functools import reduce

# 1. Умножение всех чисел в списке
def multiply_list(lst):
    return reduce(lambda x, y: x * y, lst)

# 2. Подсчет количества заглавных и строчных букв
def count_upper_lower(s):
    upper = sum(1 for c in s if c.isupper())
    lower = sum(1 for c in s if c.islower())
    return upper, lower

# 3. Проверка на палиндром
def is_palindrome(s):
    return s == s[::-1]

# 4. Корень числа через заданное время
def delayed_sqrt(num, delay_ms):
    time.sleep(delay_ms / 1000)
    return f"Square root of {num} after {delay_ms} milliseconds is {math.sqrt(num)}"

# 5. Проверка всех элементов кортежа
def all_true(tpl):
    return all(tpl)

# Тесты
print(multiply_list([1, 2, 3, 4]))  # 24
print(count_upper_lower("Hello World!"))  # (2, 8)
print(is_palindrome("radar"))  # True
print(delayed_sqrt(25100, 2123))  # Square root of 25100 after 2123 milliseconds is 158.43...
print(all_true((True, True, False)))  # False