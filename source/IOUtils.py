import os
import time
import typing
import glob #module for gettiong files that match  requirement
import sys, os
import random
import math
sys.path.append(os.path.join(os.path.dirname(__file__), '..')) #hacky way of making relative imports work
from utils.defaults import *
from source.notes import Note, Note_group, DEFAULT_NOTE_EXTENSION, DEFAULT_AUDIO_EXTENSION, AUDIO_FOLDER, NOTES_FOLDER, ROOT_DIR
from utils import notes_config

def getNotes(intensity, instrument:str = DEFAULT_INSTRUMENT, extension = DEFAULT_NOTE_EXTENSION, audio_folder = AUDIO_FOLDER, create_sound:bool=True, bpm:float=DEFAULT_BPM, note_value:float=DEFAULT_NOTE_VALUE) -> Note_group:

    path = os.path.join(ROOT_DIR, '..', NOTES_FOLDER, instrument, audio_folder, f"*.{extension}")
    file_paths = glob.glob(path)
    noteList = [Note(path = file_path, create_sound=create_sound, bpm=bpm, note_value=note_value) for file_path in file_paths if intensity in file_path] #List comprehension
    note_group = Note_group(noteList)
    return note_group

def cls():
    clear = lambda: os.system('cls' if os.name == 'nt' else 'clear')
    clear()

def test() -> None: #for debugging purposes
    note_group = getNotes(intensity='mf',audio_folder='')
    print(note_group)
    note_group.play()

def isEven(number:int) -> bool:
	return number % 2 == 0

def create_random_boolean_list(size): #will create a list of booleans with half of the values being True and the other half False, in a random order, unless the size is odd, in which case it will be approximately half True and half False (rounded up)
	# Ensure size is even
	#if size % 2 != 0:
	#	raise ValueError("The size must be an even number.")
	
	# Create a list with half True and half False values
	half_size = math.ceil(size / 2)
	boolean_list = [True] * half_size + [False] * half_size
	
	# Shuffle the list to randomize the order
	random.shuffle(boolean_list)
	
	return boolean_list


if __name__ == '__main__':
    #test()
    print(create_random_boolean_list(8))
