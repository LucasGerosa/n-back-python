'''
This file coordinates the different threads of the audio and GUI. It serves as a middle man between the GUI and the tests in the TestCase file.
'''

from PyQt6 import QtCore
import sys; import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from TestCase import NbackTestCase, TonalDiscriminationTaskTestCase, VolumeTestCase, TestCase
import utils.general_utils as general_utils
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
				testCase = VolumeTestCase(None, 20, self.bpm, self.instrument, DEFAULT_SCALE)
				self.start_execution.emit()
				for note in testCase.note_group.notes:
					if self.stop:
						print("Thread was interrupted. Stopping now.\n")
						return
					print(note.full_name)
					note.play()

			if self.stop:
				print("Thread was interrupted. Stopping now.\n")
				return

		except KeyboardInterrupt:
			print("Ctrl+c was pressed. Stopping now.")
	
class TestThread(QtCore.QThread):
	finished = QtCore.pyqtSignal()
	pre_start_execution = QtCore.pyqtSignal()
	done_testCase = QtCore.pyqtSignal(TestCase)
	start_execution = QtCore.pyqtSignal(TestCase)
	
	def __init__(self, playerName:str, test_case_n:int, notesQuantity:int, bpm:float=DEFAULT_BPM, instrument:str=DEFAULT_INSTRUMENT):
		assert test_case_n > 0, f"test_case_n must be greater than 0. Got {test_case_n} instead."
		assert notesQuantity > 0, f"notesQuantity must be greater than 0. Got {notesQuantity} instead."
		assert bpm > 0, f"bpm must be greater than 0. Got {bpm} instead."

		self.lock = QtCore.QReadWriteLock()
		self.mutex = QtCore.QMutex()
		self.wait_condition = QtCore.QWaitCondition()
		self.stop = False
		super().__init__()
		self.playerName = playerName
		self.test_case_n = test_case_n
		self.notesQuantity = notesQuantity
		self.bpm = bpm
		self.instrument = instrument
		self.id = 0
		self.is_waiting = False
	
	def wait_for_signal(self):
		self.is_waiting = True
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
	started_trial_signal = QtCore.pyqtSignal(int)
	
	def __init__(self, trials:int, playerName:str, test_case_n:int, initial_nBack:int, notesQuantity:int, bpm:float=DEFAULT_BPM, instrument:str=DEFAULT_INSTRUMENT, scale:None|scales.Scale=None, semitones:int=1):
		assert initial_nBack > 0, f"initial_nBack must be greater than 0. Got {initial_nBack} instead."
		assert initial_nBack + trials <= notesQuantity, f"initial_nBack + trials must be less than or equal to notesQuantity. Got initial_nBack = {initial_nBack}, trials = {trials}, notesQuantity = {notesQuantity}."
		assert trials > 0, f"trials must be greater than 0. Got {trials} instead."
		self.trials = trials
		self.initial_nBack = initial_nBack
		super().__init__(playerName, test_case_n, notesQuantity, bpm, instrument)
		if scale == None:
			self.scale = DEFAULT_SCALE
			return
		self.semitones = semitones
		self.scale = scale
		self.different_trial_warning_delay_list:list[float] = []

class TonalNbackTestThread(NbackTestThread):
	def executeLoop(self):
		try:
			testCaseList_list = []
			nback = self.initial_nBack
			series_id = 0
			while series_id < self.trials and not self.stop:
				self.started_trial_signal.emit(nback)
				boolean_list = general_utils.repeat_values_to_size(self.test_case_n, True, False)
				random.shuffle(boolean_list) #list for which sequences are going to be same or different
				quantity_of_true = len([x for x in boolean_list if x == True])
				up_or_down_list = general_utils.repeat_values_to_size(quantity_of_true, 1, -1) #list for which sequences are different are going to be up a semitone
				random.shuffle(up_or_down_list)
				print(f"Nback: {nback}; Is last note different: " + str(boolean_list),'Semitones: ' + str(up_or_down_list))
				up_or_down_list_id = 0
				testCaseList = []
				testCaseId = 0
				self.wait_for_signal()

				while testCaseId < self.test_case_n and not self.stop:
						self.pre_start_execution.emit()
						isLastNoteDifferent = boolean_list[testCaseId]
						print()
						if isLastNoteDifferent == True:
							semitones = up_or_down_list[up_or_down_list_id] * self.semitones
							up_or_down_list_id += 1
							print("Last note is different.")
						else:
							semitones = self.semitones
							print("Last note is equal.")
						testCase = NbackTestCase(None, self.id, nback, self.notesQuantity, self.bpm, self.instrument, scale=self.scale, isLastNoteDifferent=isLastNoteDifferent, semitones=semitones)
						testCaseList.append(testCase)
						try:
							self.start_execution.emit(testCase)
							self.wait_for_signal()
							for note in testCase.note_group.notes:
								print(note.full_name)
								note.play()
								if self.stop:
									print("Thread was interrupted. Stopping now.\n")
									return
							
							self.done_testCase.emit(testCase)
							self.wait_for_signal()
							testCase.print_result()
							NbackTestCase.saveResults(testCaseList_list, self.playerName, self.different_trial_warning_delay_list, folder = "temporary")
							testCaseId += 1
							self.id += 1
					
						except Exception as e:
							testCaseList_list.append(testCaseList)
							raise e
						
				series_id += 1
				testCaseId = 0
				nback += 1
				testCaseList_list.append(testCaseList)

			if self.stop:
				print("Thread was interrupted. Stopping now.\n")
				return
			NbackTestCase.saveResults(testCaseList_list, self.playerName, self.different_trial_warning_delay_list)

			return testCaseList
		except KeyboardInterrupt:
			print("Ctrl+c was pressed. Stopping now.")
		
		except Exception as e:
			import logging
			logging.basicConfig(
				filename='nback.log',  # Change this to None for console logging
				level=logging.ERROR,
				format='%(asctime)s - %(levelname)s - %(message)s'
			)
			print(testCaseList_list)
			NbackTestCase.saveResults(testCaseList_list, self.playerName, self.different_trial_warning_delay_list)
			logging.error("An error occurred", exc_info=True)
			raise e


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
				testCase = NbackTestCase(self.trials, self.id, self.initial_nBack + self.id, self.notesQuantity, self.bpm, self.instrument, self.scale)
				testCaseList.append(testCase)
				self.start_execution.emit(testCase)
				self.wait_for_signal()
				self.test_started_signal.emit()
				
				i = 1
				note_group_length = len(testCase.note_group)
				for note in testCase.note_group:
					self.print_note_signal.emit(note.name)
					if i < note_group_length - 1:
						self.print_hint_signal.emit(testCase.note_group[i].name)
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
	between_note_groups = QtCore.pyqtSignal()
	
	def __init__(self, playerName:str, number_of_trials:int, notesQuantity:int, bpm:float=DEFAULT_BPM, instrument:str=DEFAULT_INSTRUMENT):
		assert number_of_trials <= AVAILABLE_NUMBER_OF_TRIALS, f"Since just {AVAILABLE_NUMBER_OF_TRIALS} sequences exist for the TDT test for now, number_of_trials must be less than or equal to {AVAILABLE_NUMBER_OF_TRIALS}. Got {number_of_trials} instead."
		super().__init__(playerName, number_of_trials, notesQuantity, bpm, instrument)


	def executeLoop(self):
		
		try:
			testCaseList = []
			self.id = 0
			#boolean_list = IOUtils.repeat_values_to_size(self.test_case_n) #list for which trials are going to be same or different
			while self.id < self.test_case_n and not self.stop:
				self.pre_start_execution.emit()
				testCase = TonalDiscriminationTaskTestCase(self.notesQuantity, self.bpm, self.instrument, self.id)
				testCaseList.append(testCase)
				self.start_execution.emit(testCase)
				self.wait_for_signal()
				
				for note in testCase.note_group1.notes:
					print(note.full_name)
					note.play()
					if self.stop:
						print("Thread was interrupted. Stopping now.\n")
						return
					
				self.between_note_groups.emit()
				self.wait_for_signal()

				for note in testCase.note_group2.notes:
					print(note.full_name)
					note.play()
					if self.stop:
						print("Thread was interrupted. Stopping now.\n")
						return
				
				self.done_testCase.emit(testCase)
				self.wait_for_signal()
				testCase.print_result()
				TonalDiscriminationTaskTestCase.saveResults(testCaseList, self.playerName, folder = "temporary")
				self.id += 1

			if self.stop:
				print("Thread was interrupted. Stopping now.\n")
				return
			TonalDiscriminationTaskTestCase.saveResults(testCaseList, self.playerName)

			return testCaseList

		except KeyboardInterrupt:
			print("Ctrl+c was pressed. Stopping now.")
		
		except Exception as e:
			import logging
			logging.basicConfig(
				filename='tdt.log',  # Change this to None for console logging
				level=logging.ERROR,
				format='%(asctime)s - %(levelname)s - %(message)s'
			)
			TonalDiscriminationTaskTestCase.saveResults(testCaseList[:-1], self.playerName)
			logging.error("An error occurred", exc_info=True)
			raise e

			