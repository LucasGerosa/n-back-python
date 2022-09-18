import os
import random
import time

def cls():
    os.system('cls' if os.name=='nt' else 'clear')

def printAndSleep(bpm: int) -> int:
    cls()
    number = print(random.randint(0, 10))
    time.sleep(bpmToSeconds(bpm=60))
    return number

def bpmToSeconds(bpm: int) -> float:
    return 60 / bpm