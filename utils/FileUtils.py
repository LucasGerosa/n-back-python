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

def createfile(playerName, test = RESULT_FILENAME, outputDir = OUTPUT_DIR, folder = ""):
	createOutputDirectoryIfNotExist()
	createPlayerDirectoryIfNotExist(playerName)
	full_dir = os.path.join(outputDir,playerName, folder)
	if not os.path.exists(full_dir):
		os.makedirs(full_dir, exist_ok=True)

	# Initialize the base filename and the counter
	base_filename = os.path.join(full_dir, test + EXTENSION)

	counter = 1
	filename = base_filename

	# Check if the file exists, and if it does, increment the counter and try again
	while os.path.isfile(filename):
		filename = f'{base_filename[:-4]}{counter}{base_filename[-4:]}'  # Insert counter before file extension
		counter += 1

	return open(filename, "w", newline=''), filename