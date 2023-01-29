import os
import Parameter

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = f'{ROOT_DIR}/../output'
RESULT_FILENAME = 'result.csv'
def createPlayerDirectoryIfNotExist(playerName):
    playerDir = f"{OUTPUT_DIR}/{playerName}"
    if not os.path.exists(playerDir):
        os.makedirs(playerDir, exist_ok=True)

def createOutputDirectoryIfNotExist():
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR, exist_ok=True)

def writeFile():
    f = open("output/result.csv", "x")

def getFolder():
    return "input/"

def retrieveFilename():
    return input("Give filename: ")

def readFromFile() -> Parameter:
    while True:
        try:
            filename = retrieveFilename()
            f = open(getFolder() + filename, 'r')
            testCases = int(f.readline())

            p = Parameter()
            p.testCaseList = []

            for i in range(testCases):
                from TestCase import TestCase
                t = TestCase(i, int(f.readline()), int(f.readline()))
                print(t)
                p.testCaseList.append(t)

            return p
        except TypeError as err:
            print(f"Error happened when retriving filename, try again. Error: {err}")

if __name__ == "__main__":
    readFromFile()

def createfile(playerName):
    createOutputDirectoryIfNotExist()
    createPlayerDirectoryIfNotExist(playerName)
    filename = f'{OUTPUT_DIR}/{playerName}/{RESULT_FILENAME}'
    return open(filename, "w", newline='')