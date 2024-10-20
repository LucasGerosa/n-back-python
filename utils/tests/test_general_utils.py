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