import os
import random
import time

def cls():
    print(os.name)
    clear = lambda: os.system('cls' if os.name == 'nt' else 'clear')
    clear()

def printAndSleep(bpm: int) -> int:
    cls()
    number = random.randint(0, 10)
    print(number)
    time.sleep(bpmToSeconds(bpm=60))
    return number

def bpmToSeconds(bpm: int) -> float:
    return 60 / bpm