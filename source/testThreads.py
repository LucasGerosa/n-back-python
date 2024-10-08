from PyQt6 import QtCore, QtWidgets
import sys; import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from TestCase import NbackTestCase, TonalDiscriminationTaskTestCase, VolumeTestCase
import utils.IOUtils as IOUtils
from utils.defaults import *
import math
from notes import scales


class VolumeTestThread(QtCore.QThread):
	start_execution = QtCore.pyqtSignal()
	pre_start_execution = QtCore.pyqtSignal()

	def __init__(self, layout:QtWidgets.QLayout):
		self.lock = QtCore.QReadWriteLock()
		self.mutex = QtCore.QMutex()
		self.wait_condition = QtCore.QWaitCondition()
		self.stop = False
		super().__init__()
		self.layout = layout
	
	def run(self):
		self.executeLoop()
		self.finished.emit()

	def executeLoop(self) -> list|None:

		if self.layout == None:
			raise ValueError("Could not find layout_v. This is a bug. Please contact the developers.")
		if not isinstance(self.layout, QtWidgets.QVBoxLayout):
			raise ValueError("layout_v %(type)s is not a QVBoxLayout. This is not implemented yet, so it's a bug. Please contact the developers." % {'type': type(self.layout)})
		
		try:

			while not self.stop:
				self.pre_start_execution.emit()
				testCase = VolumeTestCase(self.layout)
				self.start_execution.emit()
				for note in testCase.note_group:
					if self.stop:
						print("Thread was interrupted. Stopping now.\n")
						return
					note.play()

			if self.stop:
				print("Thread was interrupted. Stopping now.\n")
				return

		except KeyboardInterrupt:
			print("Ctrl+c was pressed. Stopping now.")
	
class TestThread(QtCore.QThread):
	finished = QtCore.pyqtSignal()
	done_testCase = QtCore.pyqtSignal(NbackTestCase)
	start_execution = QtCore.pyqtSignal()
	pre_start_execution = QtCore.pyqtSignal()
	started_trial_signal = QtCore.pyqtSignal(int)
	
	def __init__(self, layout:QtWidgets.QLayout, trials:int, playerName:str, test_case_n:int, nBack:int, notesQuantity:int, bpm:float=DEFAULT_BPM, instrument:str=DEFAULT_INSTRUMENT):
		self.lock = QtCore.QReadWriteLock()
		self.mutex = QtCore.QMutex()
		self.wait_condition = QtCore.QWaitCondition()
		self.stop = False
		super().__init__()
		self.layout = layout
		self.playerName = playerName
		self.test_case_n = test_case_n
		self.nBack = nBack
		self.notesQuantity = notesQuantity
		self.bpm = bpm
		self.instrument = instrument
		self.trials = trials
		self.id = 0
	
	def wait_for_signal(self):
		self.mutex.lock()
		self.wait_condition.wait(self.mutex)
		self.mutex.unlock()

	def signal(self):
		self.mutex.lock()
		self.wait_condition.wakeAll()
		self.mutex.unlock()
	
	def run(self): #this is the main function that is going to be called when the thread is start()
		self.executeLoop()
		self.finished.emit()
	
	def executeLoop(self):
		pass

class NbackTestThread(TestThread):
	def __init__(self, layout:QtWidgets.QLayout, trials:int, playerName:str, test_case_n:int, nBack:int, notesQuantity:int, bpm:float=DEFAULT_BPM, instrument:str=DEFAULT_INSTRUMENT, scale:str=None):

		super().__init__(layout, trials, playerName, test_case_n, nBack, notesQuantity, bpm, instrument)
		if scale == None:
			self.scale = scales.MajorScale()
			return
		self.scale = scale

class Test1Thread(NbackTestThread):
	def executeLoop(self) -> list|None:

		if self.layout == None:
			raise ValueError("Could not find layout_v. This is a bug. Please contact the developers.")
		if not isinstance(self.layout, QtWidgets.QVBoxLayout):
			raise ValueError("layout_v %(type)s is not a QVBoxLayout. This is not implemented yet, so it's a bug. Please contact the developers.") % {'type': type(self.layout)}
		
		try:
			testCaseList_list = []
			nback = self.nBack
			series_id = 0
			while series_id < self.trials and not self.stop:
				self.started_trial_signal.emit(nback)
				boolean_list = IOUtils.create_random_boolean_list(self.test_case_n) #list for which sequences are going to be same or different
				testCaseList = []
				testCaseId = 0
				quantity_of_true = 0
				for true_or_false in boolean_list:
					if true_or_false == True: 
						quantity_of_true += 1
				boolean_list2 = IOUtils.create_random_boolean_list(quantity_of_true) #list for which sequences are different are going to be up a semitone
				print("Is last note different: " + str(boolean_list),'Is note up: ' + str(boolean_list2))
				boolean_list2_id = 0
				self.wait_for_signal()

				while testCaseId < self.test_case_n and not self.stop:
					self.pre_start_execution.emit()
					isLastNoteDifferent = boolean_list[testCaseId]
					if isLastNoteDifferent == True:
						isLastNoteUp = boolean_list2[boolean_list2_id]
						boolean_list2_id += 1
					else:
						isLastNoteUp = None
					testCase = NbackTestCase(self.layout, self.id, nback, self.notesQuantity, self.bpm, self.instrument, scale=self.scale, isLastNoteDifferent=isLastNoteDifferent, isLastNoteUp=isLastNoteUp)
					testCaseList.append(testCase)
					self.start_execution.emit()
					self.wait_for_signal()
					
					testCase.note_group.play()
					if self.stop:
						print("Thread was interrupted. Stopping now.\n")
						return
					self.done_testCase.emit(testCase)
					self.wait_for_signal()
					testCaseId += 1
					self.id += 1
				series_id += 1
				testCaseId = 0
				nback += 1
				testCaseList_list.append(testCaseList)

			if self.stop:
				print("Thread was interrupted. Stopping now.\n")
				return
			NbackTestCase.saveResults(testCaseList_list, self.playerName)

			return testCaseList
		except KeyboardInterrupt:
			print("Ctrl+c was pressed. Stopping now.")

class Test2Thread(NbackTestThread): #needs to be updated like the test 1 in order to work
	print_note_signal = QtCore.pyqtSignal(str)
	print_hint_signal = QtCore.pyqtSignal(str)
	delete_note_signal = QtCore.pyqtSignal()
	delete_hint_signal = QtCore.pyqtSignal()
	test_started_signal = QtCore.pyqtSignal()

	def __init__():
		raise NotImplementedError("This class is not implemented yet. Please contact the developers.")

	def executeLoop(self) -> list|None:
		if self.layout == None:
			raise ValueError("Could not find layout_v. This is a bug. Please contact the developers.")
		if not isinstance(self.layout, QtWidgets.QVBoxLayout):
			raise ValueError("layout_v %(type)s is not a QVBoxLayout. This is not implemented yet, so it's a bug. Please contact the developers.") % {'type': type(self.layout)}
		
		try:
			testCaseList = []
			self.id = 0
			while self.id < self.test_case_n and not self.stop:
				self.pre_start_execution.emit()
				testCase = NbackTestCase(self.layout, self.trials, self.id, self.nBack + self.id, self.notesQuantity, self.bpm, self.instrument, self.scale)
				testCaseList.append(testCase)
				self.start_execution.emit()
				self.wait_for_signal()
				self.test_started_signal.emit()
				
				i = 1
				note_group_length = len(testCase.note_group.notes)
				for note in testCase.note_group.notes:
					self.print_note_signal.emit(note.name)
					if i < note_group_length - 1:
						self.print_hint_signal.emit(testCase.note_group.notes[i].name)
					for _ in range(math.floor(note.note_value * 4)):
						if self.stop:
							print("Thread was interrupted. Stopping now.\n")
							return
						note.play()
					self.delete_note_signal.emit()
					if i < note_group_length - 1:
						self.delete_hint_signal.emit()
					i += 1
				del note_group_length
					
				if self.stop:
					print("Thread was interrupted. Stopping now.\n")
					return
				
				self.done_testCase.emit(testCase)

				self.wait_for_signal()
				self.id += 1
			if self.stop:
				print("Thread was interrupted. Stopping now.\n")
				return
			NbackTestCase.saveResults(testCaseList, self.playerName)

			return testCaseList
		except KeyboardInterrupt:
			print("Ctrl+c was pressed. Stopping now.")

class Test3Thread(TestThread):
	done_testCase = QtCore.pyqtSignal(TonalDiscriminationTaskTestCase)
	between_note_groups = QtCore.pyqtSignal()
	def executeLoop(self) -> list|None:
		
		try:
			testCaseList = []
			self.id = 0
			#boolean_list = IOUtils.create_random_boolean_list(self.test_case_n) #list for which trials are going to be same or different
			while self.id < self.test_case_n and not self.stop:
				self.pre_start_execution.emit()
				testCase = TonalDiscriminationTaskTestCase(self.layout, self.id, self.notesQuantity, self.bpm, self.instrument, self.id)
				testCaseList.append(testCase)
				self.start_execution.emit()
				self.wait_for_signal()
				
				testCase.note_group1.play()
				if self.stop:
					print("Thread was interrupted. Stopping now.\n")
					return
				
				self.between_note_groups.emit()
				self.wait_for_signal()

				testCase.note_group2.play()
				self.done_testCase.emit(testCase)
				self.wait_for_signal()

				self.id += 1
			if self.stop:
				print("Thread was interrupted. Stopping now.\n")
				return
			TonalDiscriminationTaskTestCase.saveResults(testCaseList, self.playerName)

			return testCaseList


		except KeyboardInterrupt:
			print("Ctrl+c was pressed. Stopping now.")