import os
import time
import typing
import glob #module for gettiong files that match  requirement
import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'source')) #hacky way of making relative imports work
from notes import Note, Note_group, DEFAULT_NOTE_EXTENSION, DEFAULT_AUDIO_EXTENSION, AUDIO_FOLDER, NOTES_FOLDER, ROOT_DIR


def getNotes(instrument='piano', extension = DEFAULT_NOTE_EXTENSION, audio_folder = AUDIO_FOLDER) -> Note_group:
    path = os.path.join(ROOT_DIR, '..', NOTES_FOLDER, instrument, audio_folder, f"*.{extension}")
    file_paths = glob.glob(path)
    noteList = [Note(path = file_path) for file_path in file_paths] #List comprehension
    note_group = Note_group(noteList)
    return note_group

def cls():
    clear = lambda: os.system('cls' if os.name == 'nt' else 'clear')
    clear()

def printAndSleep(bpm: int, note_group) -> Note|None:
    cls()
    random_note = note_group.getRandomNote()
    return random_note

def test() -> None: #for debugging purposes
    note_group = getNotes(audio_folder='')
    print(note_group)
    note_group.play()



if __name__ == '__main__':
    test()
