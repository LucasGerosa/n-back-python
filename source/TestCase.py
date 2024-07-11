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

class TestCase: #(nback)

	def __init__(self, layout:QtWidgets.QLayout, id:int, nBack:int, numberOfNotes:int, bpm:float=DEFAULT_BPM, instrument=DEFAULT_INSTRUMENT, mode = RANDOM_MODE, isLastNoteDifferent = None, isLastNoteUp = None) -> None:
		self.layout = layout
		self.id: int = id
		self.nBack: int = nBack
		self.isLastNoteDifferent = isLastNoteDifferent
		self.isLastNoteUp = isLastNoteUp
		if numberOfNotes < 2:
			raise ValueError(f"numberOfNotes should be > 1. Got {numberOfNotes} instead.")
		self.numberOfNotes: int = numberOfNotes - 1

		if mode == RANDOM_MODE:
			self.note_group = self.get_random_notes(bpm, instrument)
		elif mode == RANDOM_C_MAJOR_MODE:
			self.note_group = self.get_random_C_major_notes(bpm, instrument)
		elif mode == TONAL_C_MAJOR_MODE:
			self.note_group = self.get_tonal_C_major_notes(bpm, instrument)
		else:
			raise ValueError(f"mode should be either '{RANDOM_MODE}' or '{RANDOM_C_MAJOR_MODE}' or '{TONAL_C_MAJOR_MODE}'. Got '{mode}' instead.")
		assert self.isValidTestCase(), f"numberOfNotes should be > nBack. Got numberOfNotes = {self.numberOfNotes} and nBack = {self.nBack} instead."

		self.note_group.notes.append(self.get_last_note(self.nBack))
		print("Note group:")
		for note in self.note_group:
			print(note.name)
		print()
		self.result: ResultEnum = ResultEnum.ERRO

	def __str__(self):
		return f"id: {self.id}, nBack is {self.nBack}, numberOfNotes is {self.numberOfNotes}"
	'''
	
	def get_random_notes(self, bpm:float, instrument:str) -> notes.Note_group:
		note_group = get_note_group_from_config(bpm=bpm, instrument=instrument)
		if note_group.notes == []:
			raise Exception("No notes were found. Check if the input folder exists and there are folders for the instruments with mp3 files inside.")
		notes_array = np.array(note_group.notes)
		random_notes_array = np.random.choice(notes_array, self.numberOfNotes)
		random_notes_group = notes.Note_group(random_notes_array.tolist())
		return random_notes_group
	'''
	def get_random_C_major_notes(self, bpm:float, instrument:str) -> notes.Note_group:
		note_group = get_note_group_from_config(bpm=bpm, instrument=instrument)
		if note_group.notes == []:
			raise Exception("No notes were found. Check if the input folder exists and there are folders for the instruments with mp3 files inside.")
		filtered_notes = []
		#print('Notes in the note group:')
		for note in note_group:
			#print(note.name) #for debugging
			if not "#" in note.name and not "b" in note.name:
				filtered_notes.append(note)
		
		'''
		print('Filtered notes:')
		for note in filtered_notes: #for debugging
			print(note.name)'''

		filtered_note_group = notes.Note_group(filtered_notes)
		notes_array = np.array(filtered_note_group.notes)
		random_notes_array = np.random.choice(notes_array, self.numberOfNotes)
		random_notes_group = notes.Note_group(random_notes_array.tolist())
		
		return random_notes_group
	'''
	def get_tonal_C_major_notes(self, bpm:float, instrument:str) -> notes.Note_group:
		notes_str_list = (TONAL_C_MAJOR_DEFAULT_SEQUENCES * ((self.numberOfNotes - 1 // len(TONAL_C_MAJOR_DEFAULT_SEQUENCES)) + 1))[:self.numberOfNotes - 1]
		notes_list = [notes.get_note_from_note_name(intensity='mf', note_name=note_str, bpm=bpm, instrument=instrument) for note_str in notes_str_list]
		tonal_notes_group = notes.Note_group(notes_list)
		return tonal_notes_group
	'''

	def get_last_note(self, nBack:int) -> notes.Note: 
		note = self.note_group.notes[-nBack]
		if self.isLastNoteDifferent == False:
			return note
		elif self.isLastNoteDifferent == True:
			if self.isLastNoteUp == True: #if up, will go up a half step (semitone)
				return note.add_semitone(1)
			elif self.isLastNoteUp == False:
				return note.add_semitone(-1)
			else:
				raise ValueError(f"isLastNoteUp should be either True or False. Got {self.isLastNoteUp} instead. If it's None, the last note is the same as the n-back note.")
		else:
			raise ValueError(f"isLastNoteDifferent should be either True or False. Got {self.isLastNoteDifferent} instead.")
		

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
		if answer == 1:
			answer = 'same'
		elif answer == 2:
			answer = 'different'
		print(f"Answer: {answer}; Result: {self.result}\n\n")

	def isValidTestCase(self) -> Boolean:
		return self.numberOfNotes >= self.nBack
	
	@staticmethod
	def saveResults(testCaseList_list:list, playerName:str) -> None: #TODO: make it not overwrite the file with the same name
		def write_content_to_csv(writer, testCaseList_list):
			writer.writerow(['id', 'numberOfNotes', 'notesExecuted', 'nBack', 'answer', 'result', 'Quantity of correct answers', 'Quantity of incorrect answers', 'Total quantity of correct answers', 'Total quantity of incorrect answers'])

			total_quantity_right_answers = 0
			total_quantity_wrong_answers = 0
			for testCaseList in testCaseList_list:
				quantity_right_answers = 0
				quantity_wrong_answers = 0
				for t in testCaseList:
					if t.answer == 1:
						answer = 'same'
					elif t.answer == 2:
						answer = 'different'
					else:
						raise ValueError()
					
					if t.result == ResultEnum.ACERTO:
						t.result = 'Correct'
						quantity_right_answers += 1
						total_quantity_right_answers += 1

					
					elif t.result == ResultEnum.ERRO:
						t.result = 'Incorrect'
						quantity_wrong_answers += 1
						total_quantity_wrong_answers += 1
					
					else:
						raise ValueError()
				
					writer.writerow([t.id, t.numberOfNotes, ' '.join(note.name for note in t.note_group), t.nBack, answer, t.result])
				writer.writerow(['', '', '', '', '', '', quantity_right_answers, quantity_wrong_answers, total_quantity_right_answers, total_quantity_wrong_answers])


		try:
			f = FileUtils.createfile(playerName, "nback")
		
		except PermissionError:
			print("Permission denied for creating the result file. Try running the program as administrator or putting it in the folder.")
			buffer = io.StringIO()
			writer = csv.writer(buffer, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
			write_content_to_csv(writer, testCaseList_list)
			print("Here's the content that would have been written to the file:\n", buffer.getvalue())
			buffer.close()

		else:
			with f:
				# create the csv writer
				f.write('sep=,\n')
				writer = csv.writer(f, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
				write_content_to_csv(writer, testCaseList_list)

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

class TonalDiscriminationTaskTestCase:
	def __init__(self, layout:QtWidgets.QLayout, id:int, notesQuantity:int, bpm:float=DEFAULT_BPM, instrument:str=DEFAULT_INSTRUMENT, is_sequence_mismatch=None) -> None:
		self.layout = layout
		self.id: int = id
		sequence, sequence_mismatch = self.get_random_sequence(notesQuantity)
		self.note_group1 = self.get_note_group_from_sequence(bpm, instrument, sequence)
		self.is_sequence_mismatch = is_sequence_mismatch
		if is_sequence_mismatch == True:
			self.note_group2 = self.get_note_group_from_sequence(bpm, instrument, sequence_mismatch)
		elif is_sequence_mismatch == False:
			self.note_group2 = self.note_group1
		else:
			raise ValueError(f"is_sequence_mismatch should be either True or False. Got {is_sequence_mismatch} instead.")
	
	def get_note_group_from_sequence(self, bpm:float, instrument:str, sequence:list[str]) -> notes.Note_group:
		note_group = notes.Note_group([notes.get_note_from_note_name(intensity='mf', note_name=note_str, bpm=bpm, instrument=instrument) for note_str in sequence])
		return note_group

	def get_random_sequence(self, notesQuantity:int):
		sequence_index = random.randint(0, len(TONAL_DISCRIMINATION_TASK_SEQUENCES) - 1)
		sequence = TONAL_DISCRIMINATION_TASK_SEQUENCES[sequence_index]
		sequence_mismatch = TONAL_DISCRIMINATION_TASK_SEQUENCES_MISMATCH[sequence_index]
		sliced_sequence = self.slice_sequence(sequence, notesQuantity)
		sliced_sequence_mismatch = self.slice_sequence(sequence_mismatch, notesQuantity)
		return sliced_sequence, sliced_sequence_mismatch
	
	def slice_sequence(self, sequence, notesQuantity):
		return sequence[:notesQuantity]
	
	def validateAnswer(self, answer) -> None:

		if self.is_sequence_mismatch:
			if answer == 'same':
				self.result = ResultEnum.ERRO
			elif answer == 'different':
				self.result = ResultEnum.ACERTO
			else:
				raise Exception("Unexpected value caused by bad handling of unexpected values. Ask the developers to fix this.")
		else:
			if answer == 'different':
				self.result = ResultEnum.ERRO
			elif answer == 'same':
				self.result = ResultEnum.ACERTO
			else:
				raise Exception("Unexpected value caused by bad handling of unexpected values. Ask the developers to fix this.")
		
		self.answer = answer
	
	@staticmethod
	def saveResults(testCaseList:list, playerName:str) -> None: #TODO: make it not overwrite the file with the same name
		def write_content_to_csv(writer, testCaseList):
			writer.writerow(['id', '1st sequence', '2nd sequence','answer', 'result'])
			for t in testCaseList:
				writer.writerow([t.id, ' '.join(note.name for note in t.note_group1), ' '.join(note.name for note in t.note_group2), t.answer, t.result]) #FIXME: add 1st and 2nd sequence

		try:
			f = FileUtils.createfile(playerName, "tonal_discrimination_task")
		
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
				f.write('sep=,\n')
				writer = csv.writer(f, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
				write_content_to_csv(writer, testCaseList)

			f.close()

if __name__ == "__main__":
	note_group = get_note_group_from_config()
	filtered_notes = []
	for note in note_group:
		print(note.name)
		if not "#" in note.name and not "b" in note.name:
			filtered_notes.append(note)
	filtered_note_group = notes.Note_group(filtered_notes)