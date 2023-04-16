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

	def __init__(self, layout:QtWidgets.QLayout, id:int, nBack:int, numberOfNotes:int, bpm:float=DEFAULT_BPM, instrument=DEFAULT_INSTRUMENT) -> None:
		self.layout = layout
		self.id: int = id
		self.nBack: int = nBack
		self.numberOfNotes: int = numberOfNotes
		self.note_group = self.get_random_notes(bpm, instrument, numberOfNotes)
		assert self.isValidTestCase(), f"numberOfNotes should be > nBack. Got numberOfNotes = {self.numberOfNotes} and nBack = {self.nBack} instead."        
		self.result: ResultEnum = ResultEnum.ERRO

	def __str__(self):
		return f"id: {self.id}, nBack is {self.nBack}, numberOfNotes is {self.numberOfNotes}"
	
	def get_random_notes(self, bpm:float, instrument:str, numberOfNotes:int) -> notes.Note_group:
		note_group = get_note_group_from_config(bpm=bpm, instrument=instrument)
		random_notes_list = np.random.choice(note_group.notes, numberOfNotes)
		random_notes_group = notes.Note_group(random_notes_list)
		return random_notes_group

	def execute(self, layout:QtWidgets.QBoxLayout, stop_button_func) -> None:
		#stop_button = stop_button_func(self)
		#layout.addWidget(stop_button)
		self.note_group.play()
		
		self.doQuestion()

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

	def doQuestion(self):
		layout_v = PyQt6_utils.find_child_layout(self.layout)
		if layout_v == None:
			raise ValueError("Could not find layout_v. This is a bug. Please contact the developers.")
		if not isinstance(layout_v, QtWidgets.QVBoxLayout):
			raise ValueError("layout_v is not a QVBoxLayout. This is not implemented yet, so it's a bug. Please contact the developers.")
		question = QtWidgets.QLabel(f"A última nota tocada é igual à {self.nBack} nota anterior?")
		layout_v.addWidget(question)
		yes_button = QtWidgets.QPushButton("Sim")
		no_button = QtWidgets.QPushButton("Não")
		layout_v_h = QtWidgets.QHBoxLayout()
		layout_v.addLayout(layout_v_h)
		layout_v_h.addWidget(yes_button)
		layout_v_h.addWidget(no_button)
		'''	def confirm():
			answer = 1 if yes_button.isChecked() else 2
			self.validateAnswer(answer=answer)'''
		def yes():
			self.validateAnswer(answer=1)
			destroy_question()

		def no():
			self.validateAnswer(answer=2)
			destroy_question()
		
		def destroy_question():
			layout_v_h.deleteLater()
			yes_button.deleteLater()
			no_button.deleteLater()
			question.deleteLater()

		yes_button.clicked.connect(yes)
		no_button.clicked.connect(no)
		

	def isValidTestCase(self) -> Boolean:
		return self.numberOfNotes > self.nBack
	
	@staticmethod
	def saveResults(testCaseList:list, playerName:str) -> None:
		with FileUtils.createfile(playerName) as f:
			# create the csv writer
			writer = csv.writer(f, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
			i = 0
			writer.writerow(['id', 'numberOfNotes', 'notesExecuted', 'nBack', 'answer', 'result'])
			while i < len(testCaseList):
				t: TestCase = testCaseList[i]

				# write a row to the csv file
				writer.writerow(
					[t.id, t.numberOfNotes, ' '.join(note.name for note in t.note_group), t.nBack, t.answer, t.result])
				i += 1

		f.close()

	@staticmethod
	def executeFromFile(playerName:str, bpm:float=DEFAULT_BPM, instrument:str=DEFAULT_INSTRUMENT) -> list:
		p = FileUtils.readFromFile(bpm=bpm, instrument=instrument)
		testCaseList:List[TestCase] = p.testCaseList
		for testCase in testCaseList:
			testCase.execute()
		return testCaseList

	@staticmethod
	def executeLoop(layout:QtWidgets.QLayout, stop_button_func, playerName:str, test_case_n:int, nBack:int, notesQuantity:int, bpm:float=DEFAULT_BPM, instrument:str=DEFAULT_INSTRUMENT) -> list|None:
		if not isinstance(layout, QtWidgets.QBoxLayout):
			raise ValueError("layout is not a QBoxLayout. This is not implemented yet, so it's a bug. Please contact the developers.")
		try:
			testCaseList = []
			
			id = 0
			while id < test_case_n:
				while True:
					try:
						t = TestCase(layout, id, nBack, notesQuantity, bpm, instrument)
						testCaseList.append(t)
						t.execute(layout, stop_button_func)
						break
					except Exception:
						import traceback
						print(traceback.format_exc())
				id += 1

			#FIXME TestCase.saveResults(testCaseList, playerName)

			return testCaseList
		except KeyboardInterrupt:
			print("Ctrl+c was pressed. Stopping now.")
	
	def stop(self) -> None:
		self.note_group.stop_flag = True
	
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
