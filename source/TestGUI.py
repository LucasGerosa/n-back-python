from source import parent_GUI
from source.testThreads import VolumeTestThread, TonalDiscriminationTaskTestThread, TestThread, VisuoTonalNbackTestThread, TonalNbackTestThread
from PyQt6 import QtCore, QtWidgets, QtGui
from utils import PyQt6_utils, general_utils
from utils.defaults import *
import time
from notes import scales
from TestCase import NbackTestCase, TonalDiscriminationTaskTestCase, AnswerType
from dataclasses import dataclass
import typing
from fractions import Fraction

class VolumeTestGUI(parent_GUI.parent_GUI):

	def setup_volume_test_menu(self):
		h_buttons = (self.get_settings_button(),)
		text_body = self.translate("First, let's check if you can hear all the notes. Adjust the volume as needed until you can hear all the notes well.")
		v_buttons = (QtWidgets.QLabel(text_body),)
		layout_h, layout_v, test_menu = self.setup_menu(self.translate("Volume test"), widgets_h=h_buttons, widgets_v=v_buttons)
		self.test_menus.append(test_menu)
		play_test_button = QtWidgets.QPushButton(self.translate("Play"))
		play_test_button.setFont(PyQt6_utils.FONT)
		def play_test():
			layout_h, layout_v, test = self.setup_menu(back_button=False)
			self.states.append(self.takeCentralWidget())
			self.setCentralWidget(test)
			
			@QtCore.pyqtSlot()
			def on_execute_loop_thread_finished():
				if not isinstance(self.notes_thread, VolumeTestThread):
					raise ValueError(self.translate("Notes thread is not an instance of VolumeTestThread"))
				self.notes_thread.deleteLater()
				self.setCentralWidget(self.states.pop())
			
			def create_loading_label():
				nonlocal loadingLabel
				loadingLabel = QtWidgets.QLabel(self.translate("Loading")+ '...')
				loadingLabel.setStyleSheet("font-size: 50px;")
				loadingLabel.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
				layout_v.addWidget(loadingLabel)

			loadingLabel = None

			def deleteLoadingLabel():
				nonlocal loadingLabel
				loadingLabel.deleteLater()
				
			self.notes_thread = VolumeTestThread()
			self.notes_thread.finished.connect(on_execute_loop_thread_finished)
			self.notes_thread.pre_start_execution.connect(create_loading_label)
			self.notes_thread.start_execution.connect(deleteLoadingLabel)
			self.notes_thread.start()
			stop_button = self.get_stop_button(self.notes_thread)
			layout_h.addWidget(stop_button)

		play_test_button.clicked.connect(play_test)
		layout_v.addWidget(play_test_button)

	def get_volume_test_button(self):
		return PyQt6_utils.get_txt_button(self.translate('Volume test'), lambda: self.goto_frame(self.test_menus[3]))

def create_question(layout, question_text, testCase, notes_thread, translate):
		answers, question, layout_v_h, destroy_yes_no = PyQt6_utils.create_question(layout, question_text, translate("Yes"), translate("No"))
		yes_button, no_button = answers
		yes_button.setStyleSheet("background-color: green; font-size: 50px;")
		no_button.setStyleSheet("background-color: red; font-size: 50px;")
		
		def yes():
			testCase.validateAnswer(answer=AnswerType.SAME)
			destroy_yes_no()
			notes_thread.wait_condition.wakeOne()

		def no():
			testCase.validateAnswer(answer=AnswerType.DIFFERENT)
			destroy_yes_no()
			notes_thread.wait_condition.wakeOne()

		yes_button.clicked.connect(yes)
		no_button.clicked.connect(no)

class TonalDiscriminationTaskGUI(parent_GUI.parent_GUI):
	
	def setup_TDT_menu(self):
		h_buttons = (self.get_settings_button(), self.get_info_button_3())
		v_buttons = ()
		test_name = self.translate("Tonal Discrimination Task")
		layout_h, layout_v, test_menu = self.setup_menu(test_name, h_buttons, v_buttons)
		self.test_menus.append(test_menu)

		def is_notes_quantity_valid(text:str) -> tuple[bool, str]:
			result, error_message = PyQt6_utils.FormField.is_positive_digit(text)
			if not result:
				return False, error_message
			if int(text) in AVAILABLE_TDT_NOTE_QUANTITIES:
				return True, ""
			return False, "Currently, the only quantity of notes available is 4, 6, 8, 10."
		
		def is_number_of_trials_valid(text:str) -> tuple[bool, str]:
			result, error_message = PyQt6_utils.FormField.is_positive_digit(text)
			if not result:
				return False, error_message
			if int(text) <= AVAILABLE_NUMBER_OF_TRIALS:
				return True, ""
			return False, f"Since just {AVAILABLE_NUMBER_OF_TRIALS} sequences exist for the TDT test for now, number_of_trials must be less than or equal to {AVAILABLE_NUMBER_OF_TRIALS}. Got {text} instead."

		forms = PyQt6_utils.Forms(layout_v, self.translate)
		player_ID_field = forms.create_player_ID_field()
		number_of_trials_field = forms.create_field(self.translate("How many trials?"), "10", is_number_of_trials_valid)
		number_of_notes_field = forms.create_field(self.translate("How many notes?"), "4", is_notes_quantity_valid)
		bpm_field = forms.create_bpm_field()
		instrument_field = forms.create_instrument_field()
		forms.summon_reset_button()

		play_test_button = QtWidgets.QPushButton(self.translate("Play") + ' ' + test_name)
		play_test_button.setFont(PyQt6_utils.FONT)
		#button_size = play_test_button.sizeHint()

		def play_test() -> None:
			incorrect_fields = forms.validate_fields()
			if incorrect_fields != []:
				forms.summon_incorrect_fields_msgbox(incorrect_fields)
				return
			
			layout_h, layout_v, test1_test = self.setup_menu(back_button=False)
			self.states.append(self.takeCentralWidget())
			self.setCentralWidget(test1_test)
			
			@QtCore.pyqtSlot()
			def on_execute_loop_thread_finished():
				if not isinstance(self.notes_thread, TestThread):
					raise ValueError(self.translate("Notes thread is not an instance of TestThread"))
				self.notes_thread.deleteLater()
				self.setCentralWidget(self.states.pop())
			
			def countdown():
				seconds_remaining = 3
				timer = QtCore.QTimer(self)
				label = QtWidgets.QLabel('3', self)
				label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
				label.setStyleSheet("font-size: 100px;")
				layout_h.addWidget(label)

				def update_countdown():
					nonlocal seconds_remaining
					seconds_remaining -= 1
					label.setText(str(seconds_remaining))

					if seconds_remaining == 0:
						timer.stop()
						label.deleteLater()
						self.notes_thread.wait_condition.wakeOne()

				timer.timeout.connect(update_countdown)
				timer.start(1000)

			def ask_continue_test():
				nonlocal loadingLabel
				loadingLabel.deleteLater()
				answers, question, layout_v_h, destroy_question = PyQt6_utils.create_question(layout_v, self.translate("Ready for the next trial?"), self.translate("Yes"))
				yes_button = answers[0]
				yes_button.setStyleSheet("background-color: green; font-size: 50px;")
				def continue_test():
					destroy_question()
					countdown()
				yes_button.clicked.connect(continue_test)
			
			def ask_continue_test_between_note_groups():
				'''
				answers, question, layout_v_h, destroy_question = PyQt6_utils.create_question(layout_v, self.translate("Ready for the next sequence?"), self.translate("Yes"))
				yes_button = answers[0]
				yes_button.setStyleSheet("background-color: green; font-size: 50px;")
				def continue_test():
					destroy_question()
					countdown()
				yes_button.clicked.connect(continue_test)'''
				time.sleep(1)
				self.notes_thread.wait_condition.wakeOne()
			
			def create_loading_label():
				nonlocal loadingLabel
				loadingLabel = QtWidgets.QLabel(self.translate("Loading")+ '...')
				loadingLabel.setStyleSheet("font-size: 50px;")
				loadingLabel.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
				layout_v.addWidget(loadingLabel)
			
			number_of_trials = int(number_of_trials_field.text_box.text())
			player_name = player_ID_field.text_box.text()
			number_of_notes = int(number_of_notes_field.text_box.text())
			bpm = float(Fraction((bpm_field.text_box.text())))
			instrument = instrument_field.text_box.text()
			#play_test_button.setEnabled(False)
			loadingLabel = None

			self.notes_thread = TonalDiscriminationTaskTestThread(player_name, number_of_trials, number_of_notes, bpm, instrument) #0  is a placeholder for nback, which is not used in this test
			self.notes_thread.finished.connect(on_execute_loop_thread_finished)
			self.notes_thread.start_execution.connect(ask_continue_test)
			self.notes_thread.between_note_groups.connect(ask_continue_test_between_note_groups)
			self.notes_thread.pre_start_execution.connect(create_loading_label)
			self.notes_thread.done_testCase.connect(lambda testCase:self.create_questions_tonal_discrimination_task(layout_v, testCase))
			#layout_v.addStretch(1)
			self.notes_thread.start()
			#stop_button = self.get_stop_button(self.notes_thread)
			#layout_h.insertWidget(2, stop_button)

		#self.center_widget_x(button, 100, button_size.width(), button_size.height())
		play_test_button.clicked.connect(play_test)
		layout_v.addWidget(play_test_button)

	def get_TDT_button(self):
		return PyQt6_utils.get_txt_button(self.translate('Tonal discrimination task'), lambda: self.goto_frame(self.test_menus[2]))

	def setup_TDT_info_frame(self):
		title = self.translate("Tonal discrimination task")
		text_body = self.translate("In this test, you will hear a sequence of notes. \nThen, there will be a 1-second pause, and you will hear another sequence of notes. \nYou will be asked if the second sequence is the same as the first one.")
		tdt_image = QtWidgets.QLabel()
		tdt_image.setPixmap(QtGui.QPixmap("static/TDT_example.png").scaled(500, 500, QtCore.Qt.AspectRatioMode.KeepAspectRatio))
		v_widgets = (QtWidgets.QLabel(text_body), tdt_image)
		layout_h, layout_v, self.info_frame3 = self.setup_menu(title, widgets_v=v_widgets)
	
	@QtCore.pyqtSlot(QtWidgets.QVBoxLayout, TonalDiscriminationTaskTestCase)
	def create_questions_tonal_discrimination_task(self, layout, testCase:TonalDiscriminationTaskTestCase):
		if not isinstance(self.notes_thread, TestThread):
			raise ValueError(self.translate("Notes thread is not an instance of TestThread"))
		
		create_question(layout, self.translate("Are both the sequences the same?"), testCase, self.notes_thread, self.translate)

class NbackTestGUI(parent_GUI.parent_GUI):
	@QtCore.pyqtSlot(QtWidgets.QVBoxLayout, NbackTestCase)
	def create_questions(self, layout, testCase:NbackTestCase):
		if not isinstance(self.notes_thread, TestThread):
			raise ValueError(self.translate("Notes thread is not an instance of TestThread"))
		nback = testCase.nBack
		if nback == 1:
			question_text = self.translate("Is the last played note the same as the previous note?")
		elif nback == 2:
			question_text = self.translate("Is the last played note the same as the note before the previous note?")
		elif nback == 3:
			question_text = self.translate("Is the last played note the same as the note three places before it?")
		else:
			question_text = self.translate("Is the last played note the same as the {}th note before the last?").format(nback)
		create_question(layout, question_text, testCase, self.notes_thread, self.translate)

	@QtCore.pyqtSlot(QtWidgets.QVBoxLayout, int)
	def warn_user_different_trial(self, layout, nback:int):
		if nback == 1:
			question_text = self.translate("The following trial will have\nyou compare the last note with the previous note.")
		elif nback == 2:
			question_text = self.translate("The following trial\nwill have you compare the last note\nwith the note before the previous note.")
		elif nback == 3:
			question_text = self.translate("The following trial\nwill have you compare the last note with the note\nthree places before it.")
		else:
			question_text = self.translate("The following trial will have you\ncompare the last note with the {}th note before the last.").format(nback)
		
		question = QtWidgets.QLabel(question_text)
		question.setStyleSheet("font-size: 50px;")
		layout.addWidget(question)
		yes_button = QtWidgets.QPushButton(self.translate("Ok"))
		yes_button.setStyleSheet("background-color: green; font-size: 50px;")
		question.update()
		QtCore.QTimer.singleShot(1000, lambda: layout.addWidget(yes_button))

		def yes():
			question.deleteLater()
			yes_button.deleteLater()
			self.notes_thread.wait_condition.wakeOne()
		
		yes_button.clicked.connect(yes)


class TonalNbackTestGUI(NbackTestGUI):
	
	def setup_nback_test_menu(self, test_number:int, Thread:TonalNbackTestThread|VisuoTonalNbackTestThread, h_buttons:tuple[QtWidgets.QPushButton, ...]=()): #For the nback tests 
		h_buttons = (self.get_settings_button(),) + h_buttons
		v_buttons = ()
		if test_number == 1:
			test_name = self.translate("Teste nback tonal")
		elif test_number == 2:
			test_name = self.translate("Visuotonal nback test")
		else:
			raise ValueError("test_number should be 1 or 2")
		
		layout_h, layout_v, test_menu = self.setup_menu(test_name, h_buttons, v_buttons)
		self.test_menus.append(test_menu)
		player_name_q = self.translate("Participant ID")
		sequences_q = self.translate("How many sequences?")
		trials_q = self.translate("How many trials?")
		n_back_q = self.translate("Starting n-back (int)")
		notes_quantity_q = self.translate("How many notes (int)")
		bpm_q = self.translate("How many bpm (float)")
		instrument_q = self.translate("Instrument (piano or guitar)")
		labels = (player_name_q, sequences_q, trials_q, n_back_q, notes_quantity_q, bpm_q, instrument_q)
		set_text = ("Gerosa", '10', '6', '1', '10', str(DEFAULT_BPM), DEFAULT_INSTRUMENT) #TODO: have the default fields in the settings.ini file
		if len(set_text) != len(labels):
			raise Exception(f"len(set_text) ({len(set_text)}) is not equal to len(labels) ({len(labels)})")
		draft_forms_dict = dict(zip(labels, set_text))
		column_labels, column_text_box = PyQt6_utils.setup_forms(layout_v, draft_forms_dict)

		def check_isdigit(q):
			text_box = column_text_box[labels.index(q)]
			text = text_box.text()
			return text.isdigit() and int(text) > 0, text

		def check_isfloat(q):
			text_box = column_text_box[labels.index(q)]
			text = text_box.text()
			value = PyQt6_utils.is_float_or_fraction(text)
			return not (value == None or value <= 0), text

		def check_isinstrument(q):
			text_box = column_text_box[labels.index(q)]
			text = text_box.text()
			return text in INSTRUMENTS, text

		def check_isempty(q):
			text_box = column_text_box[labels.index(q)]
			text = text_box.text()
			return text != ""

		def msgbox_if_digit(q):
			is_digit, text = check_isdigit(q)
			if not is_digit:
				PyQt6_utils.get_msg_box(self.translate("Incorrect input"), f"{self.translate('Please enter an integer bigger than 0, not')} \"{text}\"", QtWidgets.QMessageBox.Icon.Warning).exec()

		def msgbox_if_float(q):
			is_float, text = check_isfloat(q)
			if not is_float:
				PyQt6_utils.get_msg_box(self.translate("Incorrect input"), f"{self.translate('Please enter a fraction or a decimal bigger than 0, not')} \"{text}\"", QtWidgets.QMessageBox.Icon.Warning).exec()

		
		def msgbox_if_instrument(q):
			is_instrument, text = check_isinstrument(q)
			if not is_instrument:
				PyQt6_utils.get_msg_box(self.translate("Incorrect input"), self.translate("Please enter a valid instrument, not \"{text}\""), QtWidgets.QMessageBox.Icon.Warning).exec()

		def msgbox_if_empty(q):
			is_empty = check_isempty(q)
			if not is_empty:
				PyQt6_utils.get_msg_box(self.translate("Incorrect input"), self.translate("Please enter something."), QtWidgets.QMessageBox.Icon.Warning).exec()

		def connect(q, func): # Tells python what to do when the user finishes typing in the msg boxes
			column_text_box[labels.index(q)].editingFinished.connect(lambda:func(q))

		connect(sequences_q, msgbox_if_digit)
		connect(n_back_q, msgbox_if_digit)
		connect(notes_quantity_q, msgbox_if_digit)
		connect(bpm_q, msgbox_if_float)
		connect(instrument_q, msgbox_if_instrument)
		connect(player_name_q, msgbox_if_empty)
		connect(trials_q, msgbox_if_digit)

		layout_v_h = QtWidgets.QHBoxLayout()
		'''
		random_radio_button = QtWidgets.QRadioButton(self.translate("Random"))
		random_radio_button.setFont(PyQt6_utils.FONT)
		random_radio_button.setStyleSheet("font-size: 20px;")
		random_radio_button.setChecked(True)
		layout_v_h.addWidget(random_radio_button)'''

		random_c_major_radio_button = QtWidgets.QRadioButton(self.translate("Random C major scale"))
		random_c_major_radio_button.setFont(PyQt6_utils.FONT)
		random_c_major_radio_button.setStyleSheet("font-size: 20px;")
		random_c_major_radio_button.setChecked(True)
		layout_v_h.addWidget(random_c_major_radio_button)
		'''
		tonal_c_major_radio_button = QtWidgets.QRadioButton(self.translate("Tonal C major scale"))
		tonal_c_major_radio_button.setFont(PyQt6_utils.FONT)
		tonal_c_major_radio_button.setStyleSheet("font-size: 20px;")
		layout_v_h.addWidget(tonal_c_major_radio_button) '''

		
		layout_v.addLayout(layout_v_h)

		reset_button = QtWidgets.QPushButton(self.translate("Reset"))
		layout_v.addWidget(reset_button)
		def reset():
			i = 0
			for text in set_text:
				column_text_box[i].setText(text)
				i += 1
		reset_button.clicked.connect(reset)
		play_test_button = QtWidgets.QPushButton(self.translate("Play") + ' ' + test_name)
		play_test_button.setFont(PyQt6_utils.FONT)
		#button_size = play_test_button.sizeHint()

		def play_test() -> None:
			def get_text(q):
				return column_text_box[labels.index(q)].text()
			
			incorrect_fields:list[str] = []
			player_name = get_text(player_name_q)
			if player_name == "":
				incorrect_fields.append(player_name_q)
			for q in (sequences_q, n_back_q, trials_q, notes_quantity_q):
				if not check_isdigit(q)[0]:
					incorrect_fields.append(q)
			if not check_isfloat(bpm_q)[0]:
				incorrect_fields.append(bpm_q)
			if not check_isinstrument(instrument_q)[0]:
				incorrect_fields.append(instrument_q)
			
			if incorrect_fields != []:
				PyQt6_utils.get_msg_box(self.translate("Incorrect input"), self.translate("The following fields are incorrect or incomplete:\n\n")+ '\n'.join(incorrect_fields)+ ".\n\n" + self.translate("Correct them and try again"), QtWidgets.QMessageBox.Icon.Warning).exec()
				return
			
			def is_notes_quantity_valid():
				notes_quantity = column_text_box[labels.index(notes_quantity_q)].text()
				n_back = column_text_box[labels.index(n_back_q)].text()
				trials = column_text_box[labels.index(trials_q)].text()
				return int(notes_quantity) >= int(n_back) + int(trials)

			if not is_notes_quantity_valid():
				PyQt6_utils.get_msg_box(self.translate("Incorrect input"), self.translate("The quantity of notes needs to be greater than or equal to the initial n-back + quantity of trials."), QtWidgets.QMessageBox.Icon.Warning).exec()
				return
			layout_h, layout_v, test1_test = self.setup_menu(back_button=False)
			self.states.append(self.takeCentralWidget())
			self.setCentralWidget(test1_test)
			
			@QtCore.pyqtSlot()
			def on_execute_loop_thread_finished():
				if not isinstance(self.notes_thread, TestThread):
					raise ValueError(self.translate("Notes thread is not an instance of TestThread"))
				self.notes_thread.deleteLater()
				self.setCentralWidget(self.states.pop())
			
			def countdown():
				seconds_remaining = 3
				timer = QtCore.QTimer(self)
				label = QtWidgets.QLabel('3', self)
				label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
				label.setStyleSheet("font-size: 100px;")
				layout_h.addWidget(label)

				def update_countdown():
					nonlocal seconds_remaining
					seconds_remaining -= 1
					label.setText(str(seconds_remaining))

					if seconds_remaining == 0:
						timer.stop()
						label.deleteLater()
						self.notes_thread.wait_condition.wakeOne()

				timer.timeout.connect(update_countdown)
				timer.start(1000)

			def ask_continue_test():
				nonlocal loadingLabel
				loadingLabel.deleteLater()
				answers, question, layout_v_h, destroy_question = PyQt6_utils.create_question(layout_v, self.translate("Ready for the next sequence?"), self.translate("Yes"))
				yes_button = answers[0]
				yes_button.setStyleSheet("background-color: green; font-size: 50px;")
				def continue_test():
					destroy_question()
					countdown()
				yes_button.clicked.connect(continue_test)
			
			def create_loading_label():
				nonlocal loadingLabel
				loadingLabel = QtWidgets.QLabel(self.translate("Loading")+ '...')
				loadingLabel.setStyleSheet("font-size: 50px;")
				loadingLabel.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
				layout_v.addWidget(loadingLabel)
			
			test_case = int(get_text(sequences_q))
			n_back = int(get_text(n_back_q))
			notes_quantity = int(get_text(notes_quantity_q))
			bpm = float(get_text(bpm_q))
			instrument = get_text(instrument_q)
			trials = int(get_text(trials_q))
			loadingLabel = None
			if random_c_major_radio_button.isChecked():
				scale = scales.Scale.get_parallel_mode(scales.Diatonic_Modes, 'C', 0)

			self.notes_thread = Thread(trials, player_name, test_case, n_back, notes_quantity, bpm, instrument, scale=scale)
			self.notes_thread.finished.connect(on_execute_loop_thread_finished)
			self.notes_thread.start_execution.connect(ask_continue_test)
			self.notes_thread.pre_start_execution.connect(create_loading_label)
			self.notes_thread.started_trial_signal.connect(lambda nback: self.warn_user_different_trial(layout_v, nback))

			if Thread is VisuoTonalNbackTestThread:
				note_label = None
				layout_grid = self.test2_frame.layout()
				def print_note_label(note_name):
					nonlocal note_label
					note_label = QtWidgets.QLabel(note_name)
					note_label.setStyleSheet("font-size: 300px;")
					layout_grid.addWidget(note_label, 1, 1, QtCore.Qt.AlignmentFlag.AlignTop)

				def delete_note_label():
					if note_label is None:
						raise ValueError(self.translate("note_label should not be None. This means that you tried to delete the note without printing it to the interface first"))
					note_label.deleteLater()
				
				hint_label = None
				def print_hint_label(note_name):
					nonlocal hint_label
					hint_label = QtWidgets.QLabel(note_name)
					hint_label.setStyleSheet("font-size: 65px;")
					#hint_label.setSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed)
					layout_grid.addWidget(hint_label, 2, 2, QtCore.Qt.AlignmentFlag.AlignRight | QtCore.Qt.AlignmentFlag.AlignBottom)
				
				def delete_hint_label():
					if hint_label is None:
						raise ValueError(self.translate("hint_label should not be None. This means that you tried to delete the note without printing it to the interface first"))
					hint_label.deleteLater()
				self.notes_thread.test_started_signal.connect(lambda: self.goto_frame(self.test2_frame))
				self.notes_thread.print_note_signal.connect(print_note_label)
				self.notes_thread.print_hint_signal.connect(print_hint_label)
				self.notes_thread.delete_note_signal.connect(delete_note_label)
				self.notes_thread.delete_hint_signal.connect(delete_hint_label)
				def done_testCase(testCase):
					self.go_back()
					self.create_questions(layout_v, testCase)

				self.notes_thread.done_testCase.connect(lambda testCase:done_testCase(testCase))
			else:
				self.notes_thread.done_testCase.connect(lambda testCase:self.create_questions(layout_v, testCase))
			#layout_v.addStretch(1)
			self.notes_thread.start()
			#stop_button = self.get_stop_button(self.notes_thread)
			#layout_h.insertWidget(2, stop_button)

		#self.center_widget_x(button, 100, button_size.width(), button_size.height())
		play_test_button.clicked.connect(play_test)
		layout_v.addWidget(play_test_button)

	def get_tonal_nback_test_button(self):
		return PyQt6_utils.get_txt_button(self.translate('Tonal nback test'), lambda: self.goto_frame(self.test_menus[0]))

	def setup_tonal_nback_info_frame(self):
		title = self.translate("Tonal nback test")
		#font = QFont("Arial", 12)
		text_body = self.translate("In this test, you will hear a sequence of notes.\nAfter the notes are played, you will be asked if the last note in the\nsequence is the same as another specific note in the sequence.")
		image = QtWidgets.QLabel()
		image.setPixmap(QtGui.QPixmap("static/nback_example.png").scaled(1000, 1000, QtCore.Qt.AspectRatioMode.KeepAspectRatio))
		text_label = QtWidgets.QLabel(text_body)
		#text_label.setFont(font)
		v_widgets = (text_label, image)
		layout_h, layout_v, self.info_frame1 = self.setup_menu(title, widgets_v=v_widgets)


class VisuotonalNbackTestGUI(NbackTestGUI):

	def setup_visuotonal_nback_test_frame(self):
		self.test2_frame = QtWidgets.QFrame(self)
		layout_grid = QtWidgets.QGridLayout()
		self.test2_frame.setLayout(layout_grid)
		minimum_x, minimum_y = 50, 50
		spacer1_h = QtWidgets.QWidget()
		spacer1_h.setMinimumSize(minimum_x, minimum_y)
		spacer2_h = QtWidgets.QWidget()
		spacer2_h.setMinimumSize(minimum_x, minimum_y)
		spacer1_v = QtWidgets.QWidget()
		spacer1_v.setMinimumSize(200, minimum_y)
		spacer2_v = QtWidgets.QWidget()
		spacer2_v.setMinimumSize(200, minimum_y)
		layout_grid.addWidget(spacer1_h, 0, 1)
		layout_grid.addWidget(spacer2_h, 2, 1)

		layout_grid.addWidget(spacer1_v, 1, 0)
		layout_grid.addWidget(spacer2_v, 1, 2)

	def get_visuotonal_nback_button(self):
		return PyQt6_utils.get_txt_button(self.translate('Visuotonal nback test'), lambda: self.goto_frame(self.test_menus[1]))