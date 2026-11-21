# test_math.py  
import pytest
from math_utils import add, divide

def test_add():
    assert add(2, 3) == 5
    assert add(-1, 1) == 0

def test_divide():
    assert divide(10, 2) == 5
    assert divide(9, 3) == 3

def test_divide_by_zero():
    with pytest.raises(ValueError):
        divide(5, 0)

# def test_average():
#     assert average([1, 2, 3]) == 2.0
#     assert average([10, 20]) == 15.0
