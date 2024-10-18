import csv
import string
from enum import Enum
from typing import List
from xmlrpc.client import Boolean
import sys; import os
import random
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from utils.defaults import *
from utils import notes_config, note_str_utils, FileUtils
from notes import notes, scales
import numpy as np
from fractions import Fraction
from PyQt6 import QtCore, QtGui, QtWidgets
from utils import PyQt6_utils, IOUtils
import io

'''This file coordinates the logic of each test, as well as validating and saving user responses. When creating new tests, this file should be the first to be modified.
'''
setting_not_exist_msg = "Setting does not exist. The settings.ini file is corrupted or something is wrong with the program."

class AnswerType(Enum):
	SAME = 'same'
	DIFFERENT = 'different'

class ResultType(Enum):
	CORRECT = 'correct'
	INCORRECT = 'incorrect'

def get_settings():
	note_str = notes_config.get_notes_setting()
	intensity_str = notes_config.get_intensity_setting()
	note_value_str = notes_config.get_setting(notes_config.NOTE_VALUE_SETTING)
	try:
		note_value = float(Fraction(note_value_str))
	
	except ValueError:
		raise ValueError(f"The setting '{notes_config.NOTE_VALUE_SETTING}' needs to be a number. Got {note_value_str} instead. Reset your settings or contact the developers.")
	return note_str, intensity_str, note_value

def get_note_group_from_config(bpm=DEFAULT_BPM, instrument=DEFAULT_INSTRUMENT) -> notes.Note_group:
	note_str, intensity_str, note_value = get_settings()
	if note_str == notes_config.ALL_NOTES:
		note_group = IOUtils.getNotes(intensity=intensity_str, instrument=instrument, audio_folder='', will_create_sound=False, bpm=bpm, note_value=note_value)
		return note_group

	note_str_list = note_str_utils.get_final_list_notes(note_str)
	return notes.Note_group.get_note_group_from_note_names(note_str_list, intensity_str, bpm, note_value=note_value)

class TestCase:
	
	def __init__(self, config_note_group:notes.Note_group, id_num:int, numberOfNotes:int, bpm:float=DEFAULT_BPM, instrument:str=DEFAULT_INSTRUMENT, scale:None|scales.Scale = None) -> None:
		self._id_num: int = id_num
		if scale == None:
			self._scale = scales.Scale.get_parallel_mode(scales.Diatonic_Modes, 'C', 0)
		else:
			self._scale = scale
		if numberOfNotes < 1:
			raise ValueError(f"numberOfNotes should be > 0. Got {numberOfNotes} instead.")
		self._numberOfNotes: int = numberOfNotes
		self._set_random_notes_group(bpm, instrument, config_note_group)

	@property
	def id_num(self) -> int:
		return self._id_num
	
	@property
	def scale(self) -> scales.Scale:
		return self._scale
	
	@property
	def numberOfNotes(self) -> int: #TODO: create a setter function, that changes the _note_group when the number of notes, is changed?
		return self._numberOfNotes

	def _set_random_notes_group(self, bpm:float, instrument:str, config_note_group:notes.Note_group):
		if config_note_group == None:
			note_group = get_note_group_from_config(bpm=bpm, instrument=instrument)
		else:
			note_group = config_note_group
		if note_group == []:
			raise Exception("No notes were found. Check if the input folder exists and there are folders for the instruments with mp3 files inside.")

		filtered_notes = []
		for note in note_group:
			if note.name in self.scale.notes_str_tuple:
				filtered_notes.append(note)

		notes_array = np.array(filtered_notes)
		random_notes_array = np.random.choice(notes_array, self.numberOfNotes)
		random_notes_list = random_notes_array.tolist()
		random_notes_group = notes.Note_group(random_notes_list)
		self._note_group = random_notes_group

	@property
	def note_group(self) -> notes.Note_group:
		return self._note_group
	
	def print_notes(self):
		for note in self.note_group:
			print(note.name)

class NbackTestCase(TestCase): #FIXME the save function does not try to create a file in the documents folder if it fails to create it in the current folder

	def __init__(self, config_note_group:notes.Note_group, id_num:int, nBack:int, numberOfNotes:int, bpm:float=DEFAULT_BPM, instrument=DEFAULT_INSTRUMENT, scale:None|scales.Scale = None, isLastNoteDifferent:bool = True, semitones:int=1) -> None:
		assert numberOfNotes > nBack, f"numberOfNotes should be > nBack. Got numberOfNotes = {numberOfNotes} and nBack = {nBack} instead."
		self._nBack: int = nBack
		assert semitones != 0, f"semitones should be negative or positive. Got 0 instead."
		self._semitones = semitones
		super().__init__(config_note_group, id_num, numberOfNotes, bpm, instrument, scale)
		self._change_nBack_and_last_note(nBack, self.note_group.notes, config_note_group.notes, isLastNoteDifferent)
		self._set_correct_answer()
		assert (isLastNoteDifferent == True and self.correct_answer == AnswerType.DIFFERENT) or (isLastNoteDifferent == False and self.correct_answer == AnswerType.SAME), f"If isLastNoteDifferent is False, the correct answer should be {AnswerType.SAME} and vice versa. Got isLastNoteDifferent = {isLastNoteDifferent} and {self.correct_answer} instead. Last note = {self.note_group[-1].full_name}, nBack note = {self.note_group[-1 - nBack].full_name}"

	@property
	def nBack(self) -> int:
		return self._nBack

	@property
	def semitones(self) -> int:
		return self._semitones

	def __str__(self):
		return f"id: {self.id_num}, nBack is {self.nBack}, numberOfNotes is {self.numberOfNotes}"
	
	def print_correct_answer(self):
		print()
		print(f"Correct answer: {self.correct_answer}")

	def print_result(self):
		print(f"Participant's answer: {self.answer}")
		print(f"Result: {self.result}\n\n")

	def _change_nBack_and_last_note(self, nBack:int, note_list:List[notes.Note], config_notes_list:List[notes.Note], isLastNoteDifferent:bool):
		self._semitone_note_list = []
		if isLastNoteDifferent:
			for note in config_notes_list:
				if note.name in self.scale.find_able_up_down_semitones(self.semitones):
					self._semitone_note_list.append(note)
		else:
			for note in config_notes_list:
				if note.name in self.scale.find_able_up_down_semitones(self.semitones) or note.name in self.scale.find_able_up_down_semitones(-self.semitones):
					self._semitone_note_list.append(note)
		
		
		assert self._semitone_note_list != [], f"No available notes for increasing {self.semitones} semitone."
		different_from_last_note = random.choice(self._semitone_note_list) # a random choice from notes that can either go up or down {semitones} semitones
		
		note_list[-nBack - 1] = different_from_last_note
		if isLastNoteDifferent:
			note_list[-1] = different_from_last_note + self.semitones
		else:
			note_list[-1] = note_list[-nBack - 1]
	
	def _set_correct_answer(self):
		lastNote: int = self.note_group[-1]
		nBackNote: int = self.note_group[-1 - self.nBack]
		if lastNote == nBackNote:
			self._correct_answer = AnswerType.SAME
		else:
			self._correct_answer = AnswerType.DIFFERENT
	
	@property
	def correct_answer(self) -> AnswerType:
		return self._correct_answer
	
	@property
	def result(self) -> ResultType:
		return self._result
	
	@property
	def answer(self) -> AnswerType:
		return self._answer
		
	def validateAnswer(self, answer):
		# Check if n-back note equals to last note
		if self.correct_answer == AnswerType.SAME:
			if answer == AnswerType.SAME:
				self._result = ResultType.CORRECT
			elif answer == AnswerType.DIFFERENT:
				self._result = ResultType.INCORRECT
			else:
				raise Exception("Unexpected value caused by bad handling of unexpected values. Ask the developers to fix this.")
		elif self.correct_answer == AnswerType.DIFFERENT:
			if answer == AnswerType.SAME:
				self._result = ResultType.INCORRECT
			elif answer == AnswerType.DIFFERENT:
				self._result = ResultType.CORRECT
			else:
				raise Exception("Unexpected value caused by bad handling of unexpected values. Ask the developers to fix this.")
		else:
			raise Exception("Unexpected value caused by bad handling of unexpected values. Ask the developers to fix this.")
		
		self._answer = answer
		return self.result
	
	@staticmethod
	def saveResults(testCaseList_list:list, playerName:str) -> None: #TODO: make it not overwrite the file with the same name
		def write_content_to_csv(writer, testCaseList_list:List[List[NbackTestCase]]):
			writer.writerow(['id', 'numberOfNotes', 'notesExecuted', 'nBack', 'Correct answer', 'User answer', 'result', 'Quantity of correct answers', 'Quantity of incorrect answers', 'Total quantity of correct answers', 'Total quantity of incorrect answers', 'Total quantity of answers'])

			total_quantity_right_answers = 0
			total_quantity_wrong_answers = 0
			for testCaseList in testCaseList_list:
				quantity_right_answers = 0
				quantity_wrong_answers = 0
				for t in testCaseList:
					if t.result == ResultType.CORRECT:
						quantity_right_answers += 1
						total_quantity_right_answers += 1

					
					elif t.result == ResultType.INCORRECT:
						quantity_wrong_answers += 1
						total_quantity_wrong_answers += 1
					
					else:
						raise ValueError()
				
					writer.writerow([t.id_num, t.numberOfNotes, ' '.join(note.name for note in t.note_group), t.nBack, t.correct_answer, t.answer, t.result])
				writer.writerow(['', '', '', '', '', '', '', quantity_right_answers, quantity_wrong_answers, total_quantity_right_answers, total_quantity_wrong_answers, total_quantity_right_answers + total_quantity_wrong_answers])

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

	@staticmethod #FIXME
	def debug() -> None:
		raise NotImplementedError("This function is not implemented yet.")
		NUMBER_OF_TESTCASES = 1
		NBACK = 4
		NUMBER_OF_NOTES = 6
		for id_num in range(NUMBER_OF_TESTCASES):
			try:
				testCase = NbackTestCase(id_num, NBACK, NUMBER_OF_NOTES, bpm = DEFAULT_BPM, instrument=DEFAULT_INSTRUMENT)
				testCase.execute()
			except Exception:
				import traceback
				print(traceback.format_exc())


class VolumeTestCase(TestCase):
	def __init__(self, config_note_group:notes.Note_group, numberOfNotes:int=20, bpm:float=DEFAULT_BPM, instrument=DEFAULT_INSTRUMENT, scale:None|scales.Scale=None) -> None:
		super().__init__(config_note_group, 0, numberOfNotes, bpm, instrument, scale)

class TonalDiscriminationTaskTestCase:
	def __init__(self, id_num:int, notesQuantity:int, bpm:float=DEFAULT_BPM, instrument:str=DEFAULT_INSTRUMENT, sequence_id=0) -> None:
		self.id_num: int = id_num
		self.sequence_id = sequence_id
		sequence, sequence_mismatch = self.get_random_sequence(notesQuantity)
		self.note_group1 = self.get_note_group_from_sequence(bpm, instrument, sequence)
		self.note_group2 = self.get_note_group_from_sequence(bpm, instrument, sequence_mismatch)
	
	@property
	def result(self) -> ResultType:
		return self._result
	
	@property
	def answer(self) -> AnswerType:
		return self._answer
	
	def get_note_group_from_sequence(self, bpm:float, instrument:str, sequence:list[str]) -> notes.Note_group:
		note_group = notes.Note_group([notes.Note.get_note_from_note_name(intensity='mf', note_name=note_str, bpm=bpm, instrument=instrument) for note_str in sequence])
		return note_group

	def get_random_sequence(self, notesQuantity:int):
		if notesQuantity == 4:
			sample_sequences = TONAL_DISCRIMINATION_TASK_SEQUENCES4
			sample_sequences_mismatch = TONAL_DISCRIMINATION_TASK_SEQUENCES4_MISMATCH
		elif notesQuantity == 6:
			sample_sequences = TONAL_DISCRIMINATION_TASK_SEQUENCES6
			sample_sequences_mismatch = TONAL_DISCRIMINATION_TASK_SEQUENCES6_MISMATCH
		elif notesQuantity == 8:
			sample_sequences = TONAL_DISCRIMINATION_TASK_SEQUENCES8
			sample_sequences_mismatch = TONAL_DISCRIMINATION_TASK_SEQUENCES8_MISMATCH
		elif notesQuantity == 10:
			sample_sequences = TONAL_DISCRIMINATION_TASK_SEQUENCES10
			sample_sequences_mismatch = TONAL_DISCRIMINATION_TASK_SEQUENCES10_MISMATCH
		else:
			raise ValueError(f"Invalid notes quantity: {notesQuantity}. The only quantities currently available are 4, 6, 8 and 10.")
		
		#sequence_index = random.randint(0, len(sample_sequences) - 1)

		sequence = sample_sequences[self.sequence_id] #this means the sequences are just going to be sampled in the same order always.
		sequence_mismatch = sample_sequences_mismatch[self.sequence_id]
		#sliced_sequence = self.slice_sequence(sequence, notesQuantity)
		#sliced_sequence_mismatch = self.slice_sequence(sequence_mismatch, notesQuantity)
		#return sliced_sequence, sliced_sequence_mismatch
		self.is_sequence_mismatch = sequence != sequence_mismatch
		print(f"Is sequence mismatch:  {self.is_sequence_mismatch}")
		return sequence, sequence_mismatch
	
	def slice_sequence(self, sequence, notesQuantity):
		return sequence[:notesQuantity]
	
	def validateAnswer(self, answer:AnswerType) -> None:

		if self.is_sequence_mismatch:
			if answer == AnswerType.SAME:
				self._result = ResultType.INCORRECT
			elif answer == AnswerType.DIFFERENT:
				self._result = ResultType.CORRECT
			else:
				raise ValueError("Unexpected value caused by bad handling of unexpected values. Ask the developers to fix this.")
		else:
			if answer == AnswerType.DIFFERENT:
				self._result = ResultType.INCORRECT
			elif answer == AnswerType.SAME:
				self._result = ResultType.CORRECT
			else:
				raise ValueError("Unexpected value caused by bad handling of unexpected values. Ask the developers to fix this.")
		
		self._answer = answer
		print(f"Participant's answer: {answer}")
		print(f"Result: {self.result}\n\n")
	
	@staticmethod
	def saveResults(testCaseList:list, playerName:str) -> None: #TODO: make it not overwrite the file with the same name
		def write_content_to_csv(writer, testCaseList):
			writer.writerow(['id', '1st sequence', '2nd sequence','answer', 'result', 'Total quantity of correct answers', 'Total quantity of incorrect answers', 'Total quantity of answers'])
			testCase_quantity_right_answers = 0
			testCase_quantity_wrong_answers = 0
			for t in testCaseList:
				if t.result == ResultType.CORRECT:
					testCase_quantity_right_answers += 1
				elif t.result == ResultType.INCORRECT:
					testCase_quantity_wrong_answers += 1
				writer.writerow([t.id_num, ' '.join(note.name for note in t.note_group1), ' '.join(note.name for note in t.note_group2), t.answer, t.result, testCase_quantity_right_answers, testCase_quantity_wrong_answers, testCase_quantity_right_answers + testCase_quantity_wrong_answers])
		
		def create_csv_file(f, testCaseList):
			with f:
				# create the csv writer
				f.write('sep=,\n')
				writer = csv.writer(f, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
				write_content_to_csv(writer, testCaseList)

			f.close()
		
		def print_csv(testCaseList):
			print("Permission denied for creating the result file. Try running the program as administrator or putting it in the folder.")
			buffer = io.StringIO()
			writer = csv.writer(buffer, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
			write_content_to_csv(writer, testCaseList)
			print("Here's the content that would have been written to the file:\n", buffer.getvalue())
			buffer.close()

		try:
			f = FileUtils.createfile(playerName, "tonal_discrimination_task")
		
		except PermissionError:
			if os.name == 'nt':
				home_dir = os.path.expanduser('~')
				documents_path = os.path.join(home_dir, 'Documents')
				file_path = os.path.join(documents_path, 'myfile.txt')
				try:
					f = FileUtils.createfile(playerName, "tonal_discrimination_task", file_path)
				except PermissionError:
					print_csv(testCaseList)
				else:
					create_csv_file(f, testCaseList)
					return
			print_csv(testCaseList)

		else:
			create_csv_file(f, testCaseList)


if __name__ == "__main__":
	note_group = get_note_group_from_config()
	filtered_notes = []
	for note in note_group:
		print(note.name)
		if not "#" in note.name and not "b" in note.name:
			filtered_notes.append(note)
	filtered_note_group = notes.Note_group(filtered_notes)

#!DELETE LATER
# def create_TestCase_from_config(TestCaseClass:TestCase, scale:scales.Scale, id_num:int, numberOfNotes:int, bpm:float=DEFAULT_BPM, instrument:str=DEFAULT_INSTRUMENT, *args, **kwargs):
# 	config_note_group = get_note_group_from_config(bpm, instrument)
# 	return TestCaseClass(config_note_group, id_num, numberOfNotes, bpm, instrument, scale, *args, **kwargs)


if __name__ == '__main__':
	pass