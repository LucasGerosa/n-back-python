import pytest
import sys; import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import note_str_utils


def test_sort_notes():
	assert sort_notes(notes) == sorted_notes

def test_is_note_greater():
	assert is_note_greater('C', 'B') == False  # C is not greater than B
	assert is_note_greater('B', 'A') == True  # B is greater than A

def test_convert_sharps_to_flats():
	assert convert_sharps_to_flats(sharps) == flats

def test_get_final_list_notes():
