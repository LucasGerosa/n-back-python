import os
import time
import typing
import glob #module for gettiong files that match  requirement
import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'source'))
from notes import Note, Note_group, DEFAULT_NOTE_EXTENSION, DEFAULT_AUDIO_EXTENSION, AUDIO_FOLDER, NOTES_FOLDER, ROOT_DIR


def getNotes(instrument='piano', extension = DEFAULT_NOTE_EXTENSION) -> Note_group:
    path = os.path.join(ROOT_DIR, '..', NOTES_FOLDER, instrument, AUDIO_FOLDER, f"*.{extension}")
    file_paths = glob.glob(path)
    noteList = [Note(path = file_path) for file_path in file_paths] #List comprehension
    note_group = Note_group(noteList)
    return note_group

def cls():
    clear = lambda: os.system('cls' if os.name == 'nt' else 'clear')
    clear()

def printAndSleep(bpm: int) -> Note:
    cls()
    note_group = getNotes()
    random_note = note_group.getRandomNote()
    random_note.play()
    time.sleep(bpmToSeconds(bpm=60))
    return random_note

def bpmToSeconds(bpm: int) -> float:
    return 60 / bpm

def test() -> None: #for debugging purposes
    note_group = getNotes()
    note_group.play()