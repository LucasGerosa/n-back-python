import sys; import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from utils.general_utils import *

def test_rotate_sequence():
	assert rotate_sequence(('C', 'D', 'E', 'F', 'G', 'A', 'B'), 1) == ('D', 'E', 'F', 'G', 'A', 'B', 'C')
	assert rotate_sequence(('C', 'D', 'E', 'F', 'G', 'A', 'B'), 2) == ('E', 'F', 'G', 'A', 'B', 'C', 'D')
	assert rotate_sequence(('C', 'D', 'E', 'F', 'G', 'A', 'B'), 3) == ('F', 'G', 'A', 'B', 'C', 'D', 'E')

def test_repeat_values_to_size():
	assert repeat_values_to_size(3, 1, 2) == [1, 1, 2, 2]
	assert repeat_values_to_size(1, 1, 2, True) == [1, 2, True]
	assert repeat_values_to_size(0, 1, 2, True) == []
	assert repeat_values_to_size(-1, 1, 2, True) == []

def test_isEven():
	assert isEven(2) == True
	assert isEven(3) == False
	assert isEven(0) == True
	assert isEven(-2) == True
	assert isEven(-3) == False

def test_lower_first_letter():
	assert lower_first_letter('Hello') == 'hello'
	assert lower_first_letter('hello') == 'hello'
	assert lower_first_letter('hELLO') == 'hELLO'

def test_is_float_or_fraction():
	assert is_float_or_fraction('1/2') == 0.5
	assert is_float_or_fraction('1') == 1.0
	assert is_float_or_fraction('1.0') == 1.0
	assert not is_float_or_fraction('a')