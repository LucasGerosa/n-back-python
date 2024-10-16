import pytest
import sys; import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from note_str_utils import sort_notes, is_note_greater, convert_sharps_to_flats, get_final_list_notes, get_greater_note, shift_note_by_semitones, get_list_notes_able_up_down_semitones


def test_sort_notes():
	assert sort_notes(['A3', 'a4', 'G3', 'B2']) == ['B2', 'G3', 'A3', 'A4']
	assert sort_notes(['A1', 'G0', 'G2', 'C2']) == ['G0', 'A1', 'C2', 'G2']

def test_is_note_greater():
	assert is_note_greater('C4', 'B4') == False
	assert is_note_greater('B5', 'A5') == True
	assert is_note_greater('C4', 'C4') == False
	assert is_note_greater('A123', 'A124') == False

def test_is_note_greater_invalid():
	with pytest.raises(ValueError):
		is_note_greater('X', 'C4')
	
	with pytest.raises(ValueError):
		is_note_greater('Xb5', 'C4')

	with pytest.raises(TypeError):
		is_note_greater(4, 'C4')

def test_get_greater_note():
	assert get_greater_note('C4', 'B4') == 'B4'
	assert get_greater_note('B5', 'A5') == 'B5'
	assert get_greater_note('C4', 'C4') == 'C4'

def test_convert_sharps_to_flats():
	assert convert_sharps_to_flats("ab#bb3") == "G3"
	assert convert_sharps_to_flats("Cbb2") == "Bb1"
	assert convert_sharps_to_flats('a###3') == 'C4'
	assert convert_sharps_to_flats('C#3') == 'Db3'
	assert convert_sharps_to_flats('B#3') == 'C4'
	assert convert_sharps_to_flats('b#3') == 'C4'
	assert convert_sharps_to_flats('Cbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb3') == 'Eb-7'

def test_convert_sharps_to_flats_invalid():
	with pytest.raises(ValueError):
		convert_sharps_to_flats('Xb5')

def test_get_final_list_notes():
	assert get_final_list_notes("A1   ;  C2") == ['A1', 'C2']
	assert get_final_list_notes("C2–B2") == get_final_list_notes("C2-B2")
	assert get_final_list_notes("C2;      B2") == ['C2', 'B2']
	assert get_final_list_notes("D3-C4") == ['D3', 'Eb3', 'E3', 'F3', 'Gb3', 'G3', 'Ab3', 'A3', 'Bb3', 'B3', 'C4']
	assert get_final_list_notes("A4-   G5; A1  -C2") == ['A1', 'Bb1', 'B1', 'C2', 'A4', 'Bb4', 'B4', 'C5', 'Db5', 'D5', 'Eb5', 'E5', 'F5', 'Gb5', 'G5']
	assert get_final_list_notes("A4-G5;C####2") == ['E2', 'A4', 'Bb4', 'B4', 'C5', 'Db5', 'D5', 'Eb5', 'E5', 'F5', 'Gb5', 'G5']
	assert get_final_list_notes("C4-C6") == ['C4', 'Db4', 'D4', 'Eb4', 'E4', 'F4', 'Gb4', 'G4', 'Ab4', 'A4', 'Bb4', 'B4', 'C5', 'Db5', 'D5', 'Eb5', 'E5', 'F5', 'Gb5', 'G5', 'Ab5', 'A5', 'Bb5', 'B5', 'C6']
	assert get_final_list_notes("Cbb2") == ['Bb1']
	assert get_final_list_notes("C##276") == ['D276']
	assert get_final_list_notes("C4F4G5") == ['C4', 'F4', 'G5']
	assert get_final_list_notes("C4-C5-C6") == get_final_list_notes("C4-C5;C6")
	assert get_final_list_notes("C4-C5-C6-C7") == get_final_list_notes("C4-C5;C6-C7")
	assert get_final_list_notes("C5-C4") == get_final_list_notes("C4-C5")

def test_shift_note_by_semitones():
	assert shift_note_by_semitones('C4', 0) == 'C4'
	assert shift_note_by_semitones('C4', 1) == 'Db4'
	assert shift_note_by_semitones('C4', 2) == 'D4'
	assert shift_note_by_semitones('C4', -1) == 'B3'

def test_get_list_notes_able_up_down_semitones():
	note_list = ['C4', 'D4', 'E4', 'F4', 'G4', 'A4', 'B4', 'C5']
	note_list1 = ['C4', 'D4', 'E4', 'F4', 'G4', 'A4', 'B4']
	note_list2 = ['F4', 'G4', 'A4', 'B4', 'C5', 'C4', 'D4', 'E4']
	assert get_list_notes_able_up_down_semitones(note_list, 1) == ['E4', 'B4']
	assert get_list_notes_able_up_down_semitones(note_list1, 1) == ['E4']
	assert get_list_notes_able_up_down_semitones(note_list, -1) == ['F4', 'C5']
	assert get_list_notes_able_up_down_semitones(note_list1, -1) == ['F4']
	assert get_list_notes_able_up_down_semitones(note_list2, 1) == ['E4', 'B4']
	assert get_list_notes_able_up_down_semitones(note_list2, 2) == ['C4', 'D4', 'F4', 'G4', 'A4']
	assert get_list_notes_able_up_down_semitones(note_list, 0) == note_list