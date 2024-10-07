import pytest
import sys; import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from note_str_utils import sort_notes, is_note_greater, convert_sharps_to_flats, get_final_list_notes


def test_sort_notes():
	assert sort_notes(['A3', 'a4', 'G3', 'B2']) == ['B2', 'G3', 'A3', 'A4']
	assert sort_notes(['A1', 'G0', 'G2', 'C2']) == ['G0', 'A1', 'C2', 'G2']

def test_is_note_greater():
	assert is_note_greater('C4', 'B4') == False
	assert is_note_greater('B5', 'A5') == True
	assert is_note_greater('C4', 'C4') == False

def test_convert_sharps_to_flats():
	assert convert_sharps_to_flats("ab#bb3") == "G3"
	assert convert_sharps_to_flats("Cbb2") == "Bb1"
	assert convert_sharps_to_flats('a###3') == 'C4'
	assert convert_sharps_to_flats('C#3') == 'Db3'
	assert convert_sharps_to_flats('B#3') == 'C4'
	assert convert_sharps_to_flats('b#3') == 'C4'
	assert convert_sharps_to_flats('Cbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb3') == 'Eb-7'

def test_get_final_list_notes():
	assert get_final_list_notes("A1   ;  C2") == ['A1', 'C2']
	assert get_final_list_notes("C2–B2") == get_final_list_notes("C2-B2")
	assert get_final_list_notes("C2;      B2") == ['C2', 'B2']
	assert get_final_list_notes("D3-C4") == ['D3', 'Eb3', 'E3', 'F3', 'Gb3', 'G3', 'Ab3', 'A3', 'Bb3', 'B3', 'C4']
	assert get_final_list_notes("A4-   G5; A1  -C2") == ['A1', 'Bb1', 'B1', 'C2', 'A4', 'Bb4', 'B4', 'C5', 'Db5', 'D5', 'Eb5', 'E5', 'F5', 'Gb5', 'G5']
	assert get_final_list_notes("A4-G5;C####2") == ['E2', 'A4', 'Bb4', 'B4', 'C5', 'Db5', 'D5', 'Eb5', 'E5', 'F5', 'Gb5', 'G5']
	assert get_final_list_notes("C4-C6") == ['C4', 'Db4', 'D4', 'Eb4', 'E4', 'F4', 'Gb4', 'G4', 'Ab4', 'A4', 'Bb4', 'B4', 'C5', 'Db5', 'D5', 'Eb5', 'E5', 'F5', 'Gb5', 'G5', 'Ab5', 'A5', 'Bb5', 'B5', 'C6']
	assert get_final_list_notes("Cbb2") == ['Bb1']