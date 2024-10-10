import os
import sys; import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from defaults import *


ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = f'{ROOT_DIR}/../output'
RESULT_FILENAME = 'result'
EXTENSION = '.csv'

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

# def readFromFile(bpm:float=DEFAULT_BPM, instrument:str=DEFAULT_INSTRUMENT) -> Parameter:
# 	while True:
# 		try:
# 			filename = retrieveFilename()
# 			f = open(getFolder() + filename, 'r')
# 			testCases = int(f.readline())

# 			p = Parameter()
# 			p.testCaseList = []
# 			from TestCase import TestCase
# 			for i in range(testCases):
# 				t = TestCase(i, int(f.readline()), int(f.readline()), bpm=bpm, instrument=instrument)
# 				print(t)
# 				p.testCaseList.append(t)

# 			return p
# 		except (TypeError, FileNotFoundError) as err:
# 			print(f"Error happened when retriving filename, try again. Error: {err}")


if __name__ == "__main__":
	# readFromFile()
	pass

def createfile(playerName, test = RESULT_FILENAME, outputDir = OUTPUT_DIR):
	createOutputDirectoryIfNotExist()
	createPlayerDirectoryIfNotExist(playerName)

	# Initialize the base filename and the counter
	base_filename = f'{outputDir}/{playerName}/{test}{EXTENSION}'

	counter = 1
	filename = base_filename

	# Check if the file exists, and if it does, increment the counter and try again
	while os.path.isfile(filename):
		filename = f'{base_filename[:-4]}{counter}{base_filename[-4:]}'  # Insert counter before file extension
		counter += 1

	return open(filename, "w", newline='')