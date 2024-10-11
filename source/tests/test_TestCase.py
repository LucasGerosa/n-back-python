import pytest
import sys; import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from TestCase import NbackTestCase, TonalDiscriminationTaskTestCase, VolumeTestCase


# def test_TonalDiscriminationTaskTestCase():
# 	pass

# def test_VolumeTestCase():
# 	volumeTestCase = VolumeTestCase()
# 	for note in volumeTestCase.note_group:
		
# def test_NbackTestCase():
# 	nback_test_case = NbackTestCase()
	

# def test_is_note_greater():
# 	assert is_note_greater('C4', 'B4') == False
# 	assert is_note_greater('B5', 'A5') == True
# 	assert is_note_greater('C4', 'C4') == False

# def test_is_note_greater_invalid():
# 	with pytest.raises(ValueError):
# 		is_note_greater('X', 'C4')
