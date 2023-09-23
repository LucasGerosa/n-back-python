import csv
import string
import FileUtils
from enum import Enum
from typing import List
from xmlrpc.client import Boolean
import IOUtils
import sys; import os
import random
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from utils.defaults import *
from utils import notes_config, note_str_utils
import notes
import numpy as np
from fractions import Fraction
from PyQt6 import QtCore, QtGui, QtWidgets
from utils import PyQt6_utils
import io

class ResultEnum(Enum):
	ACERTO = 1
	ERRO = 2

def get_note_group_from_config(bpm=DEFAULT_BPM, instrument=DEFAULT_INSTRUMENT) -> notes.Note_group:
	setting_not_exist_msg = "Setting does not exist. The settings.ini file is corrupted or something is wrong with the program."
	note_value_str = notes_config.get_setting(notes_config.NOTE_VALUE_SETTING)
	try:
		note_value = float(Fraction(note_value_str))
	
	except ValueError:
		raise ValueError(f"The setting '{notes_config.NOTE_VALUE_SETTING}' needs to be a number. Got {note_value_str} instead. Reset your settings or contact the developers.")
	
	intensity = notes_config.get_intensity_setting()
	if intensity == None:
		raise Exception(setting_not_exist_msg)
	note_str = notes_config.get_notes_setting()
	if note_str == notes_config.get_notes_setting(notes_config.DEFAULT):
		note_group = IOUtils.getNotes(intensity=intensity, instrument=instrument, audio_folder='', create_sound=False, bpm=bpm, note_value=note_value)
		return note_group
	elif note_str == None:
		raise Exception(setting_not_exist_msg)
	note_str_list = note_str_utils.get_final_list_notes(note_str)
	note_list = [notes.get_note_from_note_name(intensity, note_str, note_value=note_value) for note_str in note_str_list]
	return notes.Note_group(note_list)

class TestCase:

	def __init__(self, layout:QtWidgets.QLayout, id:int, nBack:int, numberOfNotes:int, bpm:float=DEFAULT_BPM, instrument=DEFAULT_INSTRUMENT, mode = RANDOM_MODE) -> None:
		self.layout = layout
		self.id: int = id
		self.nBack: int = nBack
		self.numberOfNotes: int = numberOfNotes
		if mode == RANDOM_MODE:
			self.note_group = self.get_random_notes(bpm, instrument, numberOfNotes)
		elif mode == C_MAJOR_MODE:
			self.note_group = self.get_C_major_notes(bpm, instrument, numberOfNotes)
		else:
			raise ValueError(f"mode should be either '{RANDOM_MODE}' or '{C_MAJOR_MODE}'. Got '{mode}' instead.")
		assert self.isValidTestCase(), f"numberOfNotes should be > nBack. Got numberOfNotes = {self.numberOfNotes} and nBack = {self.nBack} instead."


		self.result: ResultEnum = ResultEnum.ERRO

	def __str__(self):
		return f"id: {self.id}, nBack is {self.nBack}, numberOfNotes is {self.numberOfNotes}"
	
	def get_random_notes(self, bpm:float, instrument:str, numberOfNotes:int) -> notes.Note_group:
		note_group = get_note_group_from_config(bpm=bpm, instrument=instrument)
		if note_group.notes == []:
			raise Exception("No notes were found. Check if the input folder exists and there are folders for the instruments with mp3 files inside.")
		notes_array = np.array(note_group.notes)
		random_notes_array = np.random.choice(notes_array, numberOfNotes)
		random_notes_group = notes.Note_group(random_notes_array.tolist())
		return random_notes_group

	def get_C_major_notes(self, bpm:float, instrument:str, numberOfNotes:int) -> notes.Note_group:
		note_group = get_note_group_from_config(bpm=bpm, instrument=instrument)
		if note_group.notes == []:
			raise Exception("No notes were found. Check if the input folder exists and there are folders for the instruments with mp3 files inside.")
		filtered_notes = []
		for note in note_group:
			print(note.name) #for debugging
			if not "#" in note.name and not "b" in note.name:
				filtered_notes.append(note)
		
		for note in filtered_notes: #for debugging
			print(note.name)

		filtered_note_group = notes.Note_group(filtered_notes)
		notes_array = np.array(filtered_note_group.notes)
		random_notes_array = np.random.choice(notes_array, numberOfNotes)
		random_notes_group = notes.Note_group(random_notes_array.tolist())
		return random_notes_group

	def validateAnswer(self, answer) -> None:
		# Check if n-back note equals to last note
		lastNote: int = self.note_group[-1]
		nBackNote: int = self.note_group[-1 - self.nBack]

		if lastNote == nBackNote:
			if answer == 1:
				self.result = ResultEnum.ACERTO
			elif answer == 2:
				self.result = ResultEnum.ERRO
			else:
				raise Exception("Unexpected value caused by bad handling of unexpected values. Ask the developers to fix this.")
		else:
			if answer == 1:
				self.result = ResultEnum.ERRO
			elif answer == 2:
				self.result = ResultEnum.ACERTO
			else:
				raise Exception("Unexpected value caused by bad handling of unexpected values. Ask the developers to fix this.")
		
		self.answer = answer

	def isValidTestCase(self) -> Boolean:
		return self.numberOfNotes > self.nBack
	
	@staticmethod
	def saveResults(testCaseList:list, playerName:str) -> None: #TODO: make it not overwrite the file with the same name
		def write_content_to_csv(writer, testCaseList):
			writer.writerow(['id', 'numberOfNotes', 'notesExecuted', 'nBack', 'answer', 'result'])
			for t in testCaseList:
				writer.writerow([t.id, t.numberOfNotes, ' '.join(note.name for note in t.note_group), t.nBack, t.answer, t.result])

		try:
			f = FileUtils.createfile(playerName)
		
		except PermissionError:
			print("Permission denied for creating the result file. Try running the program as administrator or putting it in the folder.")
			buffer = io.StringIO()
			writer = csv.writer(buffer, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
			write_content_to_csv(writer, testCaseList)
			print("Here's the content that would have been written to the file:\n", buffer.getvalue())
			buffer.close()

		else:
			with f:
				# create the csv writer
				writer = csv.writer(f, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
				write_content_to_csv(writer, testCaseList)

			f.close()

	@staticmethod
	def executeFromFile(playerName:str, bpm:float=DEFAULT_BPM, instrument:str=DEFAULT_INSTRUMENT) -> list:
		p = FileUtils.readFromFile(bpm=bpm, instrument=instrument)
		testCaseList:List[TestCase] = p.testCaseList
		for testCase in testCaseList:
			testCase.execute()
		return testCaseList

	
	@staticmethod
	def debug() -> None:
		NUMBER_OF_TESTCASES = 1
		NBACK = 4
		NUMBER_OF_NOTES = 6
		for id in range(NUMBER_OF_TESTCASES):
			try:
				testCase = TestCase(QtWidgets.QVBoxLayout(), id, NBACK, NUMBER_OF_NOTES, bpm = DEFAULT_BPM, instrument=DEFAULT_INSTRUMENT)
				testCase.execute()
			except Exception:
				import traceback
				print(traceback.format_exc())


if __name__ == "__main__":
	note_group = get_note_group_from_config()
	filtered_notes = []
	for note in note_group:
		print(note.name)
		if not "#" in note.name and not "b" in note.name:
			filtered_notes.append(note)
	filtered_note_group = notes.Note_group(filtered_notes)