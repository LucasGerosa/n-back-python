import sys; import os
from typing import Tuple, Iterable, Type
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from utils.note_str_utils import AVAILABLE_NOTES_TUPLE
from utils.IOUtils import rotate_sequence


class Modes:
	pass

class Diatonic_Modes(Modes):
	modes = {0: 'Ionian', 1: 'Dorian', 2: 'Phrygian', 3: 'Lydian', 4: 'Mixolydian', 5: 'Aeolian', 6: 'Locrian'}
	BASE_INTERVALS = (2, 2, 1, 2, 2, 2, 1)

NATURAL_NOTES = ('C', 'D', 'E', 'F', 'G', 'A', 'B')
class Scale:
	def __init__(self, notes_str_tuple:Tuple[str], name:str, intervals:Tuple[int], mode=0):
		self.mode = mode
		self.intervals = intervals
		self.notes_str_tuple = notes_str_tuple
		self.name = name
	
	def __str__(self):
		return f'{self.root_note} {self.name} scale containing ' + str(self.notes_str_tuple)
	
	def find_able_up_down_semitones(self, semitones:int):
		assert semitones != 0, "Semitones start at 1. Calling this function without semitones makes no sense."
		
		if semitones > 0: #this ensures the semitones count starts at 1, making usage of this function more intuitive.
			semitones -= 1
		
		possible_notes = []
		note_i = 0
		for note in self.notes_str_tuple:
			if self.intervals[note_i + semitones] == 1:
				possible_notes.append(note)
			note_i += 1
		
		return possible_notes

	@staticmethod
	def get_note_index(note_name:str):
		return AVAILABLE_NOTES_TUPLE.index(note_name)
	
	@staticmethod
	def generate_scale(intervals:Tuple[int], root_note:str) -> Tuple[str]:
		interval_len = len(intervals)
		assert interval_len <= 12, f"The scale can't have more than 12 notes (12 intervals). {interval_len} intervals were given."
		assert root_note in AVAILABLE_NOTES_TUPLE, f"Invalid root note: {root_note}"
		notes_str_list = [root_note]
		index = Scale.get_note_index(root_note)
		for i in range(len(intervals) - 1):
			interval = intervals[i]
			notes_str_list.append(AVAILABLE_NOTES_TUPLE[(index + interval) % len(AVAILABLE_NOTES_TUPLE)])
			index += interval
		return tuple(notes_str_list)

	@staticmethod
	def get_chromaticScale():
		intervals = (1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1)
		return Scale(AVAILABLE_NOTES_TUPLE, "Chromatic", intervals)

	@staticmethod
	def get_relative_mode(modes_class:Type[Modes], main_root_note:str='C', mode=0):
		main_scale_intervals:Tuple[int] = modes_class.BASE_INTERVALS
		mode_intervals = rotate_sequence(main_scale_intervals, mode)
		main_scale_notes_str_tuple = Scale.generate_scale(main_scale_intervals, main_root_note)
		root_note = main_scale_notes_str_tuple[mode]
		notes_str_tuple = rotate_sequence(main_scale_notes_str_tuple, mode)
		name = root_note + ' ' + modes_class.modes[mode] 	
		return Scale(notes_str_tuple, name, mode_intervals, mode)
	
	@staticmethod
	def get_parallel_mode(modes_class:Type[Modes], root_note:str='C', mode=0):
		main_scale_intervals:Tuple[int] = modes_class.BASE_INTERVALS
		name = root_note + ' ' + modes_class.modes[mode]
		mode_intervals = rotate_sequence(main_scale_intervals, mode)
		notes_str_tuple = Scale.generate_scale(mode_intervals, root_note)
		return Scale(notes_str_tuple, name, mode_intervals, mode)

