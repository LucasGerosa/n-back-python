import os
from Parameter import Parameter
import sys; import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from utils.defaults import *

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = f'{ROOT_DIR}/../output'
RESULT_FILENAME = 'result.csv'

def createPlayerDirectoryIfNotExist(playerName) -> None:
    playerDir = f"{OUTPUT_DIR}/{playerName}"
    if not os.path.exists(playerDir):
        os.makedirs(playerDir, exist_ok=True)

def createOutputDirectoryIfNotExist():
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR, exist_ok=True)

def writeFile() -> None:
    f = open("output/result.csv", "x")

def getFolder() -> str:
    return "input/"

def retrieveFilename() -> str:
    return input("Give filename: ")

def readFromFile(bpm:float=DEFAULT_BPM, instrument:str=DEFAULT_INSTRUMENT) -> Parameter:
    while True:
        try:
            filename = retrieveFilename()
            f = open(getFolder() + filename, 'r')
            testCases = int(f.readline())

            p = Parameter()
            p.testCaseList = []
            from TestCase import TestCase
            for i in range(testCases):
                t = TestCase(i, int(f.readline()), int(f.readline()), bpm=bpm, instrument=instrument)
                print(t)
                p.testCaseList.append(t)

            return p
        except (TypeError, FileNotFoundError) as err:
            print(f"Error happened when retriving filename, try again. Error: {err}")
        


if __name__ == "__main__":
    readFromFile()

def createfile(playerName):
    createOutputDirectoryIfNotExist()
    createPlayerDirectoryIfNotExist(playerName)
    filename = f'{OUTPUT_DIR}/{playerName}/{RESULT_FILENAME}'
    return open(filename, "w", newline='')