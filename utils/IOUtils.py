import os
import time
import typing
import glob #module for gettiong files that match  requirement
import sys, os
import math
sys.path.append(os.path.join(os.path.dirname(__file__), '..')) #hacky way of making relative imports work
from utils.defaults import *
from notes.notes import Note, Note_group, DEFAULT_NOTE_EXTENSION, DEFAULT_AUDIO_EXTENSION, AUDIO_FOLDER, NOTES_FOLDER, ROOT_DIR

def getAllNotes(intensity=DEFAULT_INTENSITY, instrument:str = DEFAULT_INSTRUMENT, extension:str = DEFAULT_AUDIO_EXTENSION, audio_folder:str = AUDIO_FOLDER, will_create_sound:bool=True, bpm:float=DEFAULT_BPM, note_value:float=DEFAULT_NOTE_VALUE) -> Note_group: #type:ignore

	path = os.path.join(ROOT_DIR, '..', NOTES_FOLDER, instrument, audio_folder, f"*.{extension}")
	file_paths = glob.glob(path)
	note_str_list = []
	for file_path in file_paths:
		note_str_list.append(Note.get_note_attributes_from_path(file_path)[-2])
	
	note_group = Note_group(note_str_list, intensity, bpm, will_create_sound, instrument, note_value, audio_folder, extension)
	return note_group

# def test() -> None: #for debugging purposes
# 	note_group = getNotes(intensity='mf',audio_folder='')
# 	print(note_group)
# 	note_group.play()

def isEven(number:int) -> bool:
	return number % 2 == 0

def rotate_sequence(old_sequence:list | tuple, index:int) -> list | tuple:
	new_sequence = old_sequence[index:] + old_sequence[:index]
	return new_sequence

def repeat_values_to_size(list_size:int, *values):
	divided_size = math.ceil(list_size / len(values))
	values_list = []
	for value in values:
		values_list += [value] * divided_size
	return values_list

if __name__ == '__main__':
	#size = 3
	#print(repeat_values_to_size(size, 1, 2))
	print(getAllNotes(will_create_sound=False))