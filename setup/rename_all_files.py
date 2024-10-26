import os, sys, glob
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from utils import general_utils
from utils.defaults import *
from notes import notes

def lower_first_letter_all_note_files():
	'''This function only needs to be run for older versions of the program that didn't automatically lower the first letter of note files when downloading. Only needs to be run manually.'''
	for instrument in VALID_INSTRUMENTS:
		path = os.path.join(notes.ROOT_DIR, '..', notes.NOTES_FOLDER, instrument, f"*.mp3")
		file_paths = glob.glob(path)
		for file_path in file_paths:
			rest_of_file_path = os.path.split(file_path)[0]
			file_name = os.path.split(file_path)[-1]
			os.rename(file_path, os.path.join(rest_of_file_path, general_utils.lower_first_letter(file_name)))

if __name__ == '__main__':
	lower_first_letter_all_note_files()