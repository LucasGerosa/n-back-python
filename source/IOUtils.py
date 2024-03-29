import os
import time
import typing
import glob #module for gettiong files that match  requirement
import sys, os
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


if __name__ == '__main__':
    test()
