import os
import random
import time
import playsound

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

def cls():
    print(os.name)
    clear = lambda: os.system('cls' if os.name == 'nt' else 'clear')
    clear()

def printAndSleep(bpm: int) -> int:
    cls()
    number = random.randint(0, 10)

    # retrieve sound from id
    filename = retrieveNote(number)

    if (filename == None):
        print(number)
    else:
        playsound(filename)
        

    time.sleep(bpmToSeconds(bpm=60))
    return number

def bpmToSeconds(bpm: int) -> float:
    return 60 / bpm

def retrieveNote(note: int):
    filename = f"ROOT_DIR/../input/notas/"
    if (note == 0):
        filename += "do.aiff"
    else:
        filename = None
    
    return filename
