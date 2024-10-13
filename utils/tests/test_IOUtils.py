import sys; import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from IOUtils import *

def test_rotate_sequence():
	assert rotate_sequence(('C', 'D', 'E', 'F', 'G', 'A', 'B'), 1) == ('D', 'E', 'F', 'G', 'A', 'B', 'C')
	assert rotate_sequence(('C', 'D', 'E', 'F', 'G', 'A', 'B'), 2) == ('E', 'F', 'G', 'A', 'B', 'C', 'D')
	assert rotate_sequence(('C', 'D', 'E', 'F', 'G', 'A', 'B'), 3) == ('F', 'G', 'A', 'B', 'C', 'D', 'E')