from PyQt6 import QtCore, QtWidgets
import sys; import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from TestCase import TestCase, TonalDiscriminationTaskTestCase
import IOUtils
from utils.defaults import *
import math

class TestThread(QtCore.QThread):
	finished = QtCore.pyqtSignal()
	done_testCase = QtCore.pyqtSignal(TestCase)
	start_execution = QtCore.pyqtSignal()
	pre_start_execution = QtCore.pyqtSignal()
	
	def __init__(self, layout:QtWidgets.QLayout, playerName:str, test_case_n:int, nBack:int, notesQuantity:int, bpm:float=DEFAULT_BPM, instrument:str=DEFAULT_INSTRUMENT, mode:str = RANDOM_MODE):
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
		self.mode = mode
	
	def wait_for_signal(self):
		self.mutex.lock()
		self.wait_condition.wait(self.mutex)
		self.mutex.unlock()

	def signal(self):
		self.mutex.lock()
		self.wait_condition.wakeAll()
		self.mutex.unlock()
	
	def run(self):
		self.executeLoop()
		self.finished.emit()
	
	def executeLoop(self):
		pass

class Test1Thread(TestThread):

	def executeLoop(self) -> list|None:

		if self.layout == None:
			raise ValueError(_("Could not find layout_v. This is a bug. Please contact the developers."))
		if not isinstance(self.layout, QtWidgets.QVBoxLayout):
			raise ValueError(_("layout_v %(type)s is not a QVBoxLayout. This is not implemented yet, so it's a bug. Please contact the developers.") % {'type': type(self.layout)})
		
		try:
			testCaseList = []
			id = 0
			boolean_list = IOUtils.create_random_boolean_list(self.test_case_n) #list for which trials are going to be same or different
			quantity_of_true = 0
			for true_or_false in  boolean_list:
				if true_or_false == True: 
					quantity_of_true += 1
			boolean_list2 = IOUtils.create_random_boolean_list(quantity_of_true) #list for which trials that are different are going to be up a semitone
			boolean_list2_id = 0

			while id < self.test_case_n and not self.stop:
				self.pre_start_execution.emit()
				isLastNoteDifferent = boolean_list[id]
				if isLastNoteDifferent == True:
					#print(boolean_list2_id)
					isLastNoteUp = boolean_list2[boolean_list2_id]
					boolean_list2_id += 1
				else:
					isLastNoteUp = None
				testCase = TestCase(self.layout, id, self.nBack + id, self.notesQuantity, self.bpm, self.instrument, self.mode, isLastNoteDifferent=isLastNoteDifferent, isLastNoteUp=isLastNoteUp)
				testCaseList.append(testCase)
				self.start_execution.emit()
				self.wait_for_signal()
				
				testCase.note_group.play()
				if self.stop:
					print(_("Thread was interrupted. Stopping now."))
					return
				
				self.done_testCase.emit(testCase)
				self.wait_for_signal()
				id += 1
			if self.stop:
				print(_("Thread was interrupted. Stopping now."))
				return
			TestCase.saveResults(testCaseList, self.playerName)

			return testCaseList
		except KeyboardInterrupt:
			print(_("Ctrl+c was pressed. Stopping now."))

class Test2Thread(TestThread):
	print_note_signal = QtCore.pyqtSignal(str)
	print_hint_signal = QtCore.pyqtSignal(str)
	delete_note_signal = QtCore.pyqtSignal()
	delete_hint_signal = QtCore.pyqtSignal()
	test_started_signal = QtCore.pyqtSignal()
	def executeLoop(self) -> list|None:
		if self.layout == None:
			raise ValueError(_("Could not find layout_v. This is a bug. Please contact the developers."))
		if not isinstance(self.layout, QtWidgets.QVBoxLayout):
			raise ValueError(_("layout_v %(type)s is not a QVBoxLayout. This is not implemented yet, so it's a bug. Please contact the developers.") % {'type': type(self.layout)})
		
		try:
			testCaseList = []
			id = 0
			while id < self.test_case_n and not self.stop:
				self.pre_start_execution.emit()
				testCase = TestCase(self.layout, id, self.nBack + id, self.notesQuantity, self.bpm, self.instrument, self.mode)
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
							print(_("Thread was interrupted. Stopping now."))
							return
						note.play()
					self.delete_note_signal.emit()
					if i < note_group_length - 1:
						self.delete_hint_signal.emit()
					i += 1
				del note_group_length
					
				if self.stop:
					print(_("Thread was interrupted. Stopping now."))
					return
				
				self.done_testCase.emit(testCase)

				self.wait_for_signal()
				id += 1
			if self.stop:
				print(_("Thread was interrupted. Stopping now."))
				return
			TestCase.saveResults(testCaseList, self.playerName)

			return testCaseList
		except KeyboardInterrupt:
			print(_("Ctrl+c was pressed. Stopping now."))

class Test3Thread(TestThread):
	done_testCase = QtCore.pyqtSignal(TonalDiscriminationTaskTestCase)
	between_note_groups = QtCore.pyqtSignal()
	def executeLoop(self) -> list|None:
		try:
			testCaseList = []
			id = 0
			boolean_list = IOUtils.create_random_boolean_list(self.test_case_n) #list for which trials are going to be same or different
			while id < self.test_case_n and not self.stop:
				self.pre_start_execution.emit()
				testCase = TonalDiscriminationTaskTestCase(self.layout, id, self.notesQuantity, self.bpm, self.instrument, is_sequence_mismatch=boolean_list[id])
				testCaseList.append(testCase)
				self.start_execution.emit()
				self.wait_for_signal()
				
				testCase.note_group1.play()
				if self.stop:
					print(_("Thread was interrupted. Stopping now."))
					return
				
				self.between_note_groups.emit()
				self.wait_for_signal()

				testCase.note_group2.play()
				self.done_testCase.emit(testCase)
				self.wait_for_signal()

				id += 1
			if self.stop:
				print(_("Thread was interrupted. Stopping now."))
				return
			TonalDiscriminationTaskTestCase.saveResults(testCaseList, self.playerName)

			return testCaseList


		except KeyboardInterrupt:
			print(_("Ctrl+c was pressed. Stopping now."))