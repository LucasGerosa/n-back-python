import pytest
import sys; import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from scales import Diatonic_Modes, Scale, rotate_iterable
from utils.note_str_utils import AVAILABLE_NOTES_TUPLE


def test_Diatonic_Modes():
	major_scale_intervals = Diatonic_Modes.BASE_INTERVALS
	assert Scale.generate_scale(major_scale_intervals, 'C') == ('C', 'D', 'E', 'F', 'G', 'A', 'B')
	assert Scale.generate_scale(rotate_iterable(major_scale_intervals, 3), 'C') == ('C', 'D', 'E', 'Gb', 'G', 'A', 'B')
	assert Scale.generate_scale((2, 2, 1, 2, 2, 2, 1), 'D') == ('D', 'E', 'Gb', 'G', 'A', 'B', 'Db')
	assert Scale.generate_scale((2, 2, 1, 2, 2, 2, 1), 'B') == ('B', 'Db', 'Eb', 'E', 'Gb', 'Ab', 'Bb')

def test_Scale():
	assert Scale.get_chromaticScale().notes_str_tuple == AVAILABLE_NOTES_TUPLE
	assert Scale.generate_scale((2, 2, 1, 2, 2, 2, 1), 'C') == ('C', 'D', 'E', 'F', 'G', 'A', 'B')
	assert Scale.get_relative_mode(Diatonic_Modes, 'D', 1).notes_str_tuple[0] == 'E'
	assert Scale.get_relative_mode(Diatonic_Modes, 'C', 3).notes_str_tuple == ('F', 'G', 'A', 'B', 'C', 'D', 'E')
	assert Scale.get_parallel_mode(Diatonic_Modes, 'C', 0).notes_str_tuple == ('C', 'D', 'E', 'F', 'G', 'A', 'B')
	assert Scale.get_parallel_mode(Diatonic_Modes, 'C', 1).notes_str_tuple == ('C', 'D', 'Eb', 'F', 'G', 'A', 'Bb')
	assert Scale.get_parallel_mode(Diatonic_Modes, 'C', 3).notes_str_tuple == ('C', 'D', 'E', 'Gb', 'G', 'A', 'B')
