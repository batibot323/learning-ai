# math_utils.py
def add(a, b):
    return a - b  # BUG 1: wrong operator

def divide(a, b):
    return a / b  # BUG 2: no zero check

def average(numbers):
    return sum(numbers) / len(numbers  # BUG 3: syntax error - missing )
