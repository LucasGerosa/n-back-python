from PyQt6 import QtCore
import sys; import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from TestCase import NbackTestCase, TonalDiscriminationTaskTestCase, VolumeTestCase, get_note_group_from_config
import utils.IOUtils as IOUtils
from utils.defaults import *
import math
import random
from notes import scales

DEFAULT_SCALE = scales.Scale.get_parallel_mode(scales.Diatonic_Modes, 'C', 0)


class VolumeTestThread(QtCore.QThread):
	start_execution = QtCore.pyqtSignal()
	pre_start_execution = QtCore.pyqtSignal()

	def __init__(self, bpm:float=DEFAULT_BPM, instrument:str=DEFAULT_INSTRUMENT):
		self.lock = QtCore.QReadWriteLock()
		self.mutex = QtCore.QMutex()
		self.wait_condition = QtCore.QWaitCondition()
		self.stop = False
		super().__init__()
		self.bpm = bpm
		self.instrument = instrument
	
	def run(self):
		self.executeLoop()
		self.finished.emit()

	def executeLoop(self):
		
		try:

			while not self.stop:
				self.pre_start_execution.emit()
				testCase = VolumeTestCase(get_note_group_from_config(self.bpm, self.instrument), 5, self.bpm, self.instrument, DEFAULT_SCALE) #TODO: there should be a way to change the scale, maybe as a new setting.
				self.start_execution.emit()
				for note in testCase.note_group:
					if self.stop:
						print("Thread was interrupted. Stopping now.\n")
						return
					note.play()
				self.stop = True
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
	
	def __init__(self, trials:int, playerName:str, test_case_n:int, nBack:int, notesQuantity:int, bpm:float=DEFAULT_BPM, instrument:str=DEFAULT_INSTRUMENT):
		self.lock = QtCore.QReadWriteLock()
		self.mutex = QtCore.QMutex()
		self.wait_condition = QtCore.QWaitCondition()
		self.stop = False
		super().__init__()
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
	def __init__(self, trials:int, playerName:str, test_case_n:int, nBack:int, notesQuantity:int, bpm:float=DEFAULT_BPM, instrument:str=DEFAULT_INSTRUMENT, scale:str=None, semitones:int=1):

		super().__init__(trials, playerName, test_case_n, nBack, notesQuantity, bpm, instrument)
		if scale == None:
			self.scale = scales.MajorScale() #FIXME
			return
		self.semitones = semitones
		self.scale = scale

class TonalNbackTestThread(NbackTestThread):
	def executeLoop(self):
		try:
			testCaseList_list = []
			nback = self.nBack
			series_id = 0
			while series_id < self.trials and not self.stop:
				self.started_trial_signal.emit(nback)
				boolean_list = random.shuffle(IOUtils.repeat_values_to_size(self.test_case_n, True, False)) #list for which sequences are going to be same or different
				quantity_of_true = len([x for x in boolean_list if x == True])
				up_or_down_list = random.shuffle(IOUtils.repeat_values_to_size(quantity_of_true, 1, -1)) #list for which sequences are different are going to be up a semitone
				print("Is last note different: " + str(boolean_list),'Is note up: ' + str(up_or_down_list))
				up_or_down_list_id = 0
				testCaseList = []
				testCaseId = 0
				self.wait_for_signal()

				while testCaseId < self.test_case_n and not self.stop:
					self.pre_start_execution.emit()
					isLastNoteDifferent = boolean_list[testCaseId]
					if isLastNoteDifferent == True:
						semitones = up_or_down_list[up_or_down_list_id] * self.semitones
						up_or_down_list_id += 1
					else:
						semitones = None
					testCase = NbackTestCase(self.id, nback, self.notesQuantity, self.bpm, self.instrument, scale=self.scale, isLastNoteDifferent=isLastNoteDifferent, semitones=semitones)
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

class VisuoTonalNbackTestThread(NbackTestThread): #needs to be updated like the test 1 in order to work
	print_note_signal = QtCore.pyqtSignal(str)
	print_hint_signal = QtCore.pyqtSignal(str)
	delete_note_signal = QtCore.pyqtSignal()
	delete_hint_signal = QtCore.pyqtSignal()
	test_started_signal = QtCore.pyqtSignal()

	def __init__():
		raise NotImplementedError("This class is not implemented yet. Please contact the developers.")

	def executeLoop(self):
		try:
			testCaseList = []
			self.id = 0
			while self.id < self.test_case_n and not self.stop:
				self.pre_start_execution.emit()
				testCase = NbackTestCase(self.trials, self.id, self.nBack + self.id, self.notesQuantity, self.bpm, self.instrument, self.scale)
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

class TonalDiscriminationTaskTestThread(TestThread):
	done_testCase = QtCore.pyqtSignal(TonalDiscriminationTaskTestCase)
	between_note_groups = QtCore.pyqtSignal()
	def executeLoop(self):
		
		try:
			testCaseList = []
			self.id = 0
			#boolean_list = IOUtils.repeat_values_to_size(self.test_case_n) #list for which trials are going to be same or different
			while self.id < self.test_case_n and not self.stop:
				self.pre_start_execution.emit()
				testCase = TonalDiscriminationTaskTestCase(self.id, self.notesQuantity, self.bpm, self.instrument, self.id)
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