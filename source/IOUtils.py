import os
import time
#import playsound
#import fnmatch
import typing
import glob #module for gettiong files that match  requirement
from notes import Note, Note_group, DEFAULT_NOTE_EXTENSION, DEFAULT_AUDIO_EXTENSION, AUDIO_FOLDER, NOTES_FOLDER


ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

def getNotes(directory = '', extension = DEFAULT_NOTE_EXTENSION) -> Note_group:
    file_paths = glob.glob(f"{ROOT_DIR}/../{NOTES_FOLDER}{directory}*.{extension}")
    noteList = [Note(path = file_path) for file_path in file_paths] #List comprehension
    note_group = Note_group(noteList)
    return note_group

def convertAudioFiles(convert_from = DEFAULT_AUDIO_EXTENSION, convert_to = DEFAULT_NOTE_EXTENSION, directory = AUDIO_FOLDER) -> None: #Converts all files from aiff to mp3
    note_group = getNotes(directory=directory, extension=convert_from)
    note_group.convert(new_extension=convert_to)
        

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

def test() -> None:
    note_group = getNotes()
    note_group.play()

if __name__ == '__main__':
    convertAudioFiles()
    test()
