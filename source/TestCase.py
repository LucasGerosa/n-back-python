'''This file coordinates the logic of each test, as well as validating and saving user responses. When creating new tests, this file should be the first to be modified.
'''
from enum import Enum
from typing import List, Tuple, Optional
from xmlrpc.client import Boolean
import sys, os, random, csv, io, stat
import numpy as np
from fractions import Fraction
from PyQt6 import QtCore, QtGui, QtWidgets
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from utils.defaults import *
from utils import general_utils, notes_config, note_str_utils, FileUtils
from notes import notes, scales
from utils import PyQt6_utils


setting_not_exist_msg = "Setting does not exist. The settings.ini file is corrupted or something is wrong with the program."

class AnswerType:
	SAME = 'same'
	DIFFERENT = 'different'

class ResultType:
	CORRECT = 'correct'
	INCORRECT = 'incorrect'

def get_settings(instrument=DEFAULT_INSTRUMENT, extension=notes.DEFAULT_NOTE_EXTENSION) -> tuple[list[str], str, float]: #type: ignore
	
	def get_final_notes_str_from_note_str(note_config_str:str, intensity:str, instrument:str, extension:str) -> list[str]:
		if note_config_str == notes_config.ALL_NOTES:
			notes_str_list = notes.getAllNotesStr(intensity=intensity, instrument=instrument, extension=extension, audio_folder='')

		else:
			notes_str_list = note_str_utils.get_final_list_notes(note_config_str)

		return notes_str_list
	
	intensity = notes_config.get_intensity_setting()
	note_str_list = get_final_notes_str_from_note_str(notes_config.get_notes_setting(), intensity, instrument, extension)
	note_value_str = notes_config.get_setting(notes_config.NOTE_VALUE_SETTING)
	try:
		note_value:float = float(Fraction(note_value_str))
	
	except ValueError:
		raise ValueError(f"The setting '{notes_config.NOTE_VALUE_SETTING}' needs to be a number. Got {note_value_str} instead. Reset your settings or contact the developers.")
	return note_str_list, intensity, note_value

class TestCase:
	
	@classmethod
	def create_csv_file(cls, f, testCaseList, *write_content_to_csv_args) -> None:
		with f:
			# create the csv writer
			f.write('sep=,\n')
			writer = csv.writer(f, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
			cls.write_content_to_csv(writer, testCaseList, *write_content_to_csv_args)
		file_path = f.name
		f.close()
		os.chmod(file_path, stat.S_IRUSR | stat.S_IRGRP | stat.S_IROTH)

	@classmethod
	def try_create_file(cls, playerName:str, test_name:str, testCaseList:list, *write_content_to_csv_args):

		def print_csv(testCaseList):
			print("Permission denied for creating the result file. Try running the program as administrator or putting it in the folder.")
			buffer = io.StringIO()
			writer = csv.writer(buffer, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
			cls.write_content_to_csv(writer, testCaseList, *write_content_to_csv_args)
			print("Here's the content that would have been written to the file:\n", buffer.getvalue())
			buffer.close()

		try:
			f, file_name = FileUtils.createfile(playerName, test_name)
		
		except PermissionError:
			if os.name == 'nt':
				home_dir = os.path.expanduser('~')
				documents_path = os.path.join(home_dir, 'Documents')
				file_path = os.path.join(documents_path, file_name)
				try:
					f = FileUtils.createfile(playerName, test_name, file_path)
				except PermissionError:
					print_csv(testCaseList)
					return
				cls.create_csv_file(f, testCaseList, *write_content_to_csv_args)
				return
			print_csv(testCaseList)
			return
		cls.create_csv_file(f, testCaseList, *write_content_to_csv_args)
class RandomTestCase(TestCase):
	
	def __init__(self, id_num:int, numberOfNotes:int, scale:None|scales.Scale = None) -> None:
		self._id_num: int = id_num
		if scale == None:
			self._scale = scales.Scale.get_parallel_mode(scales.Diatonic_Modes, 'C', 0)
		else:
			self._scale = scale
		if numberOfNotes < 1:
			raise ValueError(f"numberOfNotes should be > 0. Got {numberOfNotes} instead.")
		self._numberOfNotes: int = numberOfNotes

	@property
	def id_num(self) -> int:
		return self._id_num
	
	@property
	def scale(self) -> scales.Scale:
		return self._scale
	
	@property
	def numberOfNotes(self) -> int:
		return self._numberOfNotes

	def get_random_notes_str(self, instrument:str, config_notes_str:None|tuple[List[str], str, float]=None, extension:str=notes.DEFAULT_NOTE_EXTENSION) -> Tuple[List[str], str, float, List[str]]:
		
		if config_notes_str == None:
			notes_str, intensity, note_value = get_settings(instrument=instrument, extension=extension)
		else:
			notes_str, intensity, note_value = config_notes_str #type:ignore
		
		assert notes_str, f"No notes were found. Check if the input folder exists and there is a folder for '{instrument}' with {extension} files inside."

		available_notes_str = []
		for note_str in notes_str:
			if note_str_utils.separate_note_name_octave(note_str)[0] in self.scale.notes_str_tuple:
				available_notes_str.append(note_str)

		notes_array = np.array(available_notes_str)
		random_notes_array = np.random.choice(notes_array, self.numberOfNotes)
		random_notes_list:list[str] = random_notes_array.tolist()
		return random_notes_list, intensity, note_value, available_notes_str #type:ignore

	@property
	def note_group(self) -> notes.Note_group:
		return self._note_group
	
	def print_notes(self):
		for note in self.note_group:
			print(note.full_name)

class NbackTestCase(RandomTestCase): #FIXME the save function does not try to create a file in the documents folder if it fails to create it in the current folder

	def __init__(self, config_notes_str:None|tuple[list, str, float], id_num:int, nBack:int, numberOfNotes:int, bpm:float=DEFAULT_BPM, instrument=DEFAULT_INSTRUMENT, scale:None|scales.Scale = None, isLastNoteDifferent:bool = True, semitones:int=1, extension=notes.DEFAULT_NOTE_EXTENSION) -> None: #TODO: I don't think id_num is a necessary parameter.
		assert nBack > 0, f"N-back should be > 0. Got {nBack} instead."
		assert numberOfNotes > 0, f"numberOfNotes should be > 0. Got {numberOfNotes} instead."
		assert numberOfNotes > nBack, f"numberOfNotes should be > nBack. Got numberOfNotes = {numberOfNotes} and nBack = {nBack} instead."
		assert semitones != 0, f"semitones should be negative or positive. Got 0 instead."
		self._nBack: int = nBack
		self._semitones = semitones
		super().__init__(id_num, numberOfNotes, scale)
		self._set_note_group(config_notes_str, bpm, instrument, isLastNoteDifferent, semitones, extension)

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
		print(f"\nParticipant's answer: {self.answer}")
		print(f"Result: {self.result}\n")

	def _set_note_group(self, config_notes_str:None|tuple[list, str, float], bpm:float, instrument:str, isLastNoteDifferent:bool, semitones:int, extension:str) -> None:

		def change_nBack_and_last_note(available_notes_str:List[str], note_str_list:list[str], isLastNoteDifferent:bool, semitones:int):
			
			self._semitone_note_str_list = note_str_utils.get_list_notes_able_up_down_semitones(available_notes_str, semitones)
			if not isLastNoteDifferent:
				self._semitone_note_str_list += note_str_utils.get_list_notes_able_up_down_semitones(available_notes_str, -semitones)
			
			assert self._semitone_note_str_list, f"No available notes for increasing {semitones} semitone from the notes {available_notes_str}."
			
			different_from_last_note = random.choice(self._semitone_note_str_list) # a random choice from notes that can either go up or down {semitones} semitones
			note_str_list[-self.nBack - 1] = different_from_last_note
			if isLastNoteDifferent:
				note_str_list[-1] = note_str_utils.shift_note_by_semitones(different_from_last_note, semitones)
				self._correct_answer = AnswerType.DIFFERENT
			else:
				note_str_list[-1] = different_from_last_note
				self._correct_answer = AnswerType.SAME

		random_notes_str, intensity, note_value, available_notes_str = self.get_random_notes_str(instrument, config_notes_str, extension)
		change_nBack_and_last_note(available_notes_str, random_notes_str, isLastNoteDifferent, semitones)
		self._note_group = notes.Note_group(random_notes_str, intensity, bpm, instrument, note_value, extension=extension)
	
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
	def write_content_to_csv(writer, testCaseList_list:List[List[RandomTestCase]], different_trial_warning_delay_list):
		writer.writerow(['id', 'Number of notes', 'Notes executed', 'N-Back', 'Correct answer', 'User answer', 'result', 'Response delay (seconds)', 'Continue test delay (seconds)', 'Different trial warning delay (seconds)', 'Quantity of correct answers', 'Quantity of incorrect answers', 'Total quantity of correct answers', 'Total quantity of incorrect answers', 'Total quantity of answers'])
		# Note: the Response delay is the time it takes for the participant to answer the yes or no question about the n-back. 
		# The continue test delay is the time it takes for the participant to press ok after reading "Ready for the next sequence?".
		# The different trial warning delay is the time it takes for the participant to press ok after reading that the trial will have a different n-back. It's impossible to have it be less than 1s because the button is invisible for 1s.
		total_quantity_right_answers = 0
		total_quantity_wrong_answers = 0
		i = 0
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
			
				writer.writerow([t.id_num, t.numberOfNotes, ' '.join(note.full_name for note in t.note_group), t.nBack, t.correct_answer, t.answer, t.result, t.answer_delay, t.continue_test_delay])
			writer.writerow(['', '', '', '', '', '', '', '', '', different_trial_warning_delay_list[i], quantity_right_answers, quantity_wrong_answers, total_quantity_right_answers, total_quantity_wrong_answers, total_quantity_right_answers + total_quantity_wrong_answers])
		
		i += 1

	@staticmethod
	def saveResults(testCaseList_list:list, playerName:str, different_trial_warning_delay_list:list[float]) -> None: #TODO: make it not overwrite the file with the same name
		NbackTestCase.try_create_file(playerName, "nback", testCaseList_list, different_trial_warning_delay_list)
		
class VolumeTestCase(RandomTestCase):
	def __init__(self, config_notes_str:None|tuple[list, str, float]=None, numberOfNotes:int=20, bpm:float=DEFAULT_BPM, instrument=DEFAULT_INSTRUMENT, scale:None|scales.Scale=None, extension=notes.DEFAULT_NOTE_EXTENSION) -> None:
		super().__init__(0, numberOfNotes, scale)
		self._set_note_group(config_notes_str, bpm, instrument, extension)

	def _set_note_group(self, config_notes_str:None|tuple[list, str, float], bpm:float, instrument:str, extension:str) -> None:
		random_notes_str, intensity, note_value = self.get_random_notes_str(instrument, config_notes_str, extension)[:3]
		self._note_group = notes.Note_group(random_notes_str, intensity, bpm, instrument, note_value, extension=extension)
	
class TonalDiscriminationTaskTestCase(TestCase):
	def __init__(self, notesQuantity:int, bpm:float=DEFAULT_BPM, instrument:str=DEFAULT_INSTRUMENT, sequence_id:int=0, intensity=DEFAULT_INTENSITY, note_value=DEFAULT_NOTE_VALUE, extension=notes.DEFAULT_NOTE_EXTENSION) -> None:
		self.sequence_id = sequence_id
		sequence, sequence_mismatch = self.get_random_sequence(notesQuantity)
		self.note_group1 = notes.Note_group(sequence, intensity=intensity, bpm=bpm, instrument=instrument, note_value=note_value, extension=extension)
		self.note_group2 = notes.Note_group(sequence_mismatch, intensity=intensity, bpm=bpm, instrument=instrument, note_value=note_value, extension=extension)
	
	@property
	def result(self) -> ResultType:
		return self._result
	
	@property
	def answer(self) -> AnswerType:
		return self._answer

	def get_random_sequence(self, notesQuantity:int):
		match notesQuantity:
			case 4:
				sample_sequences = TONAL_DISCRIMINATION_TASK_SEQUENCES4
				sample_sequences_mismatch = TONAL_DISCRIMINATION_TASK_SEQUENCES4_MISMATCH
			case 6:
				sample_sequences = TONAL_DISCRIMINATION_TASK_SEQUENCES6
				sample_sequences_mismatch = TONAL_DISCRIMINATION_TASK_SEQUENCES6_MISMATCH
			case 8:
				sample_sequences = TONAL_DISCRIMINATION_TASK_SEQUENCES8
				sample_sequences_mismatch = TONAL_DISCRIMINATION_TASK_SEQUENCES8_MISMATCH
			case 10:
				sample_sequences = TONAL_DISCRIMINATION_TASK_SEQUENCES10
				sample_sequences_mismatch = TONAL_DISCRIMINATION_TASK_SEQUENCES10_MISMATCH
			case _:
				raise NotImplementedError(
					f"Invalid notes quantity: {notesQuantity}. The only quantities currently available are 4, 6, 8, and 10."
        )
		
		#sequence_index = random.randint(0, len(sample_sequences) - 1)

		sequence = sample_sequences[self.sequence_id] #this means the sequences are just going to be sampled in the same order always.
		sequence_mismatch = sample_sequences_mismatch[self.sequence_id]
		self.is_sequence_mismatch = sequence != sequence_mismatch
		print(f"Is sequence mismatch:  {self.is_sequence_mismatch}")
		if self.is_sequence_mismatch:
			for i in range(len(sequence)):
				if sequence[i] == sequence_mismatch[i]:
					self.mismatch_note = sequence[i]
					break
		else:
			self.mismatch_note = '-'
		print(self.mismatch_note)
		return sequence, sequence_mismatch
	
	def slice_sequence(self, sequence, notesQuantity):
		return sequence[:notesQuantity]
	
	def print_result(self):
		print(f"Participant's answer: {self.answer}")
		print(f"Result: {self.result}\n\n")
	
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
	
	@staticmethod
	def write_content_to_csv(writer, testCaseList):
		writer.writerow(['id', '1st sequence', '2nd sequence', 'Mismatch note', 'User answer', 'result', 'Response delay (seconds)', 'Continue test delay (seconds)', 'Total quantity of correct answers', 'Total quantity of incorrect answers', 'Total quantity of answers'])
		testCase_quantity_right_answers = 0
		testCase_quantity_wrong_answers = 0
		id_num = 0
		for t in testCaseList:
			if t.result == ResultType.CORRECT:
				testCase_quantity_right_answers += 1
			elif t.result == ResultType.INCORRECT:
				testCase_quantity_wrong_answers += 1
			writer.writerow([id_num, ' '.join(note.full_name for note in t.note_group1), ' '.join(note.full_name for note in t.note_group2), t.mismatch_note, t.answer, t.result, t.answer_delay, t.continue_test_delay, testCase_quantity_right_answers, testCase_quantity_wrong_answers, testCase_quantity_right_answers + testCase_quantity_wrong_answers])
			id_num += 1
	
	@staticmethod
	def saveResults(testCaseList:list, playerName:str) -> None:
		TonalDiscriminationTaskTestCase.try_create_file(playerName, "tonal_discrimination_task", testCaseList)
		

if __name__ == "__main__":
	t = VolumeTestCase()

