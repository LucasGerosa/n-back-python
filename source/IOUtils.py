import os
import random
import time
import playsound
import fnmatch

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
AUDIO_EXTENSION = 'mp3'

def getNoteFiles() -> list:
    directory = f"{ROOT_DIR}/../input/notas/"
    files = [file for file in os.listdir(directory) if fnmatch.fnmatch(file, '*.' + AUDIO_EXTENSION)]
    return files

noteFiles = getNoteFiles()

def cls():
    clear = lambda: os.system('cls' if os.name == 'nt' else 'clear')
    clear()

def printAndSleep(bpm: int) -> int:
    cls()
    number = random.randint(0, len(noteFiles) - 1)

    # retrieve sound from id
    filename = noteFiles[number]

    #playsound(filename) #FIXME

    time.sleep(bpmToSeconds(bpm=60))
    return number

def bpmToSeconds(bpm: int) -> float:
    return 60 / bpm
