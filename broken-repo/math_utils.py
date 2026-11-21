# math_utils.py
def add(a, b):
    return a - b  # BUG: wrong operator

def divide(a, b):
    return a / b  # BUG: no zero check

def average(nums):
    return sum(nums) / len(nums)
