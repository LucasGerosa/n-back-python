'''Contains the GUI for the main tests for the application.'''

import time, sys, os, typing
from source import parent_GUI
from source.testThreads import VolumeTestThread, TonalDiscriminationTaskTestThread, TestThread, VisuoTonalNbackTestThread, TonalNbackTestThread
from PyQt6 import QtCore, QtWidgets, QtGui
from utils import PyQt6_utils, forms, validators
from utils.defaults import *
from notes import scales
from source.TestCase import NbackTestCase, TonalDiscriminationTaskTestCase, AnswerType, TestCase
from fractions import Fraction

class Page(QtWidgets.QFrame):
	
	def __init__(self, parent:parent_GUI.parent_GUI, title:str="", widgets_h:tuple[QtWidgets.QWidget, ...]=(), widgets_v:tuple[QtWidgets.QWidget, ...]=()):
		super().__init__(parent)
		self.app = parent
		self.layout_v = QtWidgets.QVBoxLayout(self)
		self.layout_v.setAlignment(QtCore.Qt.AlignmentFlag.AlignTop)

		self.layout_v_h0 = QtWidgets.QHBoxLayout()
		self.layout_v.addLayout(self.layout_v_h0)
		self.layout_v_h0.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeft)
		for widget in widgets_h:
			self.layout_v_h0.addWidget(widget)

		self.layout_v_h1 = QtWidgets.QHBoxLayout()
		self.layout_v.addLayout(self.layout_v_h1)
		if title:
			title = parent.translate(title)
		self.layout_v_h1.addWidget(PyQt6_utils.create_frame_title(title), alignment=QtCore.Qt.AlignmentFlag.AlignCenter)

		self.layout_v_h2 = QtWidgets.QHBoxLayout()
		self.layout_v.addLayout(self.layout_v_h2)

		self.layout_v_h2_v = QtWidgets.QVBoxLayout()
		self.layout_v_h2.addLayout(self.layout_v_h2_v)
		self.layout_v_h2_v.setContentsMargins(50, 20, 50, 0)
		for widget in widgets_v:
			self.layout_v_h2_v.addWidget(widget)
		self.layout_v_h2_v.setAlignment(QtCore.Qt.AlignmentFlag.AlignHCenter)
		#return self.layout_v_h2, self.layout_v_h2_v, frame
	
	def create_question(self, question_text:str, testCase:TestCase):
			answers, question, layout_v_h, destroy_yes_no = PyQt6_utils.create_question(self.layout_v_h2_v, question_text, self.app.translate("Yes"), self.app.translate("No"))
			yes_button, no_button = answers
			yes_button.setStyleSheet("background-color: green; font-size: 50px;")
			no_button.setStyleSheet("background-color: red; font-size: 50px;")
			
			def yes():
				testCase.validateAnswer(answer=AnswerType.SAME)
				destroy_yes_no()
				self.notes_thread.wait_condition.wakeOne()

			def no():
				testCase.validateAnswer(answer=AnswerType.DIFFERENT)
				destroy_yes_no()
				self.notes_thread.wait_condition.wakeOne()

			yes_button.clicked.connect(yes)
			no_button.clicked.connect(no)

	def countdown(self):
		seconds_remaining = 3
		timer = QtCore.QTimer() #is self.app here necessary?
		label = QtWidgets.QLabel('3') #is self.app here necessary?
		label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
		label.setStyleSheet("font-size: 200px;")
		self.layout_v_h2_v.addWidget(label)

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

	def ask_continue_test(self):
		self.loading_label.deleteLater()
		answers, question, layout_v_h, destroy_question = PyQt6_utils.create_question(self.layout_v_h2_v, self.app.translate("Ready for the next trial?"), self.app.translate("Yes"))
		yes_button = answers[0]
		yes_button.setStyleSheet("background-color: green; font-size: 50px;")
		def continue_test():
			destroy_question()
			self.countdown()
		yes_button.clicked.connect(continue_test)

PlayTestThreadFunc = typing.Callable[[Page], None]
PostInitFunc = typing.Callable[[None], PlayTestThreadFunc]

class MenuPage(Page):
	
	def __init__(self, parent:parent_GUI.parent_GUI, title:str="", widgets_h:tuple[QtWidgets.QWidget, ...]=(), widgets_v:tuple[QtWidgets.QWidget, ...]=()):
		additional_widgets = (parent.get_back_button(),)
		super().__init__(parent, title, additional_widgets + widgets_h, widgets_v)

class TestMenuPage(MenuPage):
	
	def __init__(self, parent:parent_GUI.parent_GUI, title:str="", widgets_h:tuple[QtWidgets.QWidget, ...]=(), widgets_v:tuple[QtWidgets.QWidget, ...]=()):
		additional_widgets = (parent.get_settings_button(),)
		super().__init__(parent, title, additional_widgets + widgets_h, widgets_v)
		play_test_thread = self.post_init_func()
		self.play_test_button = QtWidgets.QPushButton(parent.translate("Play") + ' ' + parent.translate(title))
		self.play_test_button.setFont(QtGui.QFont(PyQt6_utils.FONT, PyQt6_utils.STANDARD_FONT_SIZE))
		self.layout_v_h2_v.addWidget(self.play_test_button)

		def play_test():
			test_page = Page(parent)
			parent.stacked_widget.addWidget(test_page)
			parent.stacked_widget.setCurrentWidget(test_page)

			play_test_thread(test_page)

			def create_loading_label():
				test_page.loading_label = parent.get_loading_label()
				test_page.layout_v.addWidget(test_page.loading_label)
			
			@QtCore.pyqtSlot()
			def on_execute_loop_thread_finished():
				test_page.notes_thread.deleteLater()
				parent.stacked_widget.setCurrentWidget(self)
				parent.stacked_widget.removeWidget(test_page)
			
			test_page.notes_thread.pre_start_execution.connect(create_loading_label)
			test_page.notes_thread.finished.connect(on_execute_loop_thread_finished)
			test_page.notes_thread.start()

		self.play_test_button.clicked.connect(play_test)
	
	def post_init_func(self) -> PlayTestThreadFunc:
		def play_test_thread(test_page:Page) -> None:
			pass
		return play_test_thread

class VolumeTestMenuPage(TestMenuPage):
	
	def __init__(self, parent):
		text_body = parent.translate("First, let's check if you can hear all the notes. Adjust the volume as needed until you can hear all the notes well.")
		
		text_body_label = QtWidgets.QLabel(text_body)
		text_body_label.setFont(QtGui.QFont(PyQt6_utils.FONT, 15))
		text_body_label.setWordWrap(True)
		text_body_label.setSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Preferred)
		text_body_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
		text_body_label.setContentsMargins(0, 0, 0, 20)
		v_buttons = (text_body_label,)

		super().__init__(parent, title="Volume test", widgets_v=v_buttons)

	def post_init_func(self) -> PlayTestThreadFunc:
		
		def play_test_thread(test_page:Page) -> None:
			
			test_page.notes_thread = VolumeTestThread()
			test_page.notes_thread.start_execution.connect(lambda: test_page.loading_label.deleteLater())
			stop_button = self.app.get_stop_button(test_page.notes_thread)
			test_page.layout_v_h2.addWidget(stop_button)
		
		return play_test_thread
class TonalDiscriminationTaskMenuPage(TestMenuPage):

	def __init__(self, parent):
		additional_widgets = (parent.get_TDT_info_button(),)
		
		super().__init__(parent, "Tonal Discrimination Task", additional_widgets)
		#form.summon_validate_all_button(validate_all_button=self.play_test_button, post_validation_func=play_test_thread)
	
	def post_init_func(self) -> PlayTestThreadFunc:
		
		def is_number_of_notes_valid(translate:validators.TranslateCallable, text:str) -> validators.IsValidErrorMessage:
			result, error_message = forms.FormField.is_non_empty(translate, text)
			if not result:
				return False, error_message
			if int(text) in AVAILABLE_TDT_NOTE_QUANTITIES:
				return True, ""
			AVAILABLE_TDT_NOTE_QUANTITIES_STR = ', '.join(map(str, AVAILABLE_TDT_NOTE_QUANTITIES))
			return False, translate("Currently, the only number of notes available is {}.").format(AVAILABLE_TDT_NOTE_QUANTITIES_STR)
		
		def is_number_of_trials_valid(translate:validators.TranslateCallable, text:str) -> validators.IsValidErrorMessage:
			result, error_message = forms.FormField.is_non_empty(translate, text)
			if not result:
				return False, error_message
			if int(text) <= AVAILABLE_NUMBER_OF_TRIALS:
				return True, ""
			return False, translate("Since just {AVAILABLE_NUMBER_OF_TRIALS} sequences exist for the TDT test for now, number_of_trials must be less than or equal to {AVAILABLE_NUMBER_OF_TRIALS}. Got {text} instead.").format(AVAILABLE_NUMBER_OF_TRIALS=AVAILABLE_NUMBER_OF_TRIALS, text=text)

		form = forms.FormPresets(self.layout_v_h2_v, self.app.translate)
		player_ID_field = form.create_player_ID_field()
		number_of_trials_field = form.create_number_of_trials_field("10", is_number_of_trials_valid)
		number_of_notes_field = form.create_number_of_notes_field("4", is_number_of_notes_valid)
		bpm_field = form.create_bpm_field()
		instrument_field = form.create_instrument_field() #TODO: add a dropdown menu with the available instruments instead.
		form.summon_reset_button()
		def play_test_thread(test_page:Page) -> None:
			
			def ask_continue_test_between_note_groups():
				'''
				answers, question, layout_v_h, destroy_question = PyQt6_utils.create_question(layout_v, self.app.translate("Ready for the next sequence?"), self.app.translate("Yes"))
				yes_button = answers[0]
				yes_button.setStyleSheet("background-color: green; font-size: 50px;")
				def continue_test():
					destroy_question()
					countdown()
				yes_button.clicked.connect(continue_test)'''
				time.sleep(1)
				test_page.notes_thread.wait_condition.wakeOne()
			
			# def create_loading_label():
			# 	nonlocal loading_label
			# 	loading_label = QtWidgets.QLabel(self.app.translate("Loading")+ '...')
			# 	loading_label.setStyleSheet("font-size: 50px;")
			# 	loading_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
			# 	layout_v.addWidget(loading_label)
			
			number_of_trials = int(number_of_trials_field.text_box.text())
			player_name = player_ID_field.text_box.text()
			number_of_notes = int(number_of_notes_field.text_box.text())
			bpm = float(Fraction((bpm_field.text_box.text())))
			instrument = instrument_field.text_box.text()
			@QtCore.pyqtSlot(TonalDiscriminationTaskTestCase)
			def create_questions_tonal_discrimination_task(testCase:TonalDiscriminationTaskTestCase):
				test_page.create_question(self.app.translate("Are both the sequences the same?"), testCase)

			test_page.notes_thread = TonalDiscriminationTaskTestThread(player_name, number_of_trials, number_of_notes, bpm, instrument)
			test_page.notes_thread.start_execution.connect(test_page.ask_continue_test)
			test_page.notes_thread.between_note_groups.connect(ask_continue_test_between_note_groups)
			test_page.notes_thread.done_testCase.connect(lambda testCase:create_questions_tonal_discrimination_task(testCase))

		return play_test_thread

class TestGUI(parent_GUI.parent_GUI):
	
	def get_stop_button(self, thread:TonalNbackTestThread):
		button = QtWidgets.QPushButton()
		button.setIcon(self.stop_image)
		button.resize(PyQt6_utils.BUTTON_SIZE, PyQt6_utils.BUTTON_SIZE)
		button.setSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed)
		button.setIconSize(button.size())
		def stop():
			thread.stop = True
			button.deleteLater()
		button.clicked.connect(stop) 
		return button

class VolumeTestGUI(TestGUI):

	def setup_volume_test_menu(self):
		self.volume_test_menu = VolumeTestMenuPage(self)
		self.stacked_widget.addWidget(self.volume_test_menu)

	def get_volume_test_button(self):
		return PyQt6_utils.get_txt_button(self.translate('Volume test'), lambda: self.goto_frame(self.volume_test_menu))



class TonalDiscriminationTaskGUI(parent_GUI.parent_GUI):
	
	def get_TDT_info_button(self):
		info_button = PyQt6_utils.get_button_with_image(self.info_image, lambda:self.goto_frame(self.info_frame3))
		return info_button
	
	def setup_TDT_menu(self):
		self.tdt_test_menu = TonalDiscriminationTaskMenuPage(self)
		self.stacked_widget.addWidget(self.tdt_test_menu)

	def get_TDT_button(self):
		return PyQt6_utils.get_txt_button(self.translate('Tonal discrimination task'), lambda: self.goto_frame(self.tdt_test_menu))

	def setup_TDT_info_frame(self):
		title = self.translate("Tonal discrimination task")
		text_body = self.translate("In this test, you will hear a sequence of notes. \nThen, there will be a 1-second pause, and you will hear another sequence of notes. \nYou will be asked if the second sequence is the same as the first one.")
		tdt_image = QtWidgets.QLabel()
		tdt_image.setPixmap(QtGui.QPixmap("static/TDT_example.png").scaled(500, 500, QtCore.Qt.AspectRatioMode.KeepAspectRatio))
		v_widgets = (QtWidgets.QLabel(text_body), tdt_image)
		layout_h, layout_v, self.info_frame3 = self.setup_menu(title, widgets_v=v_widgets)

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
	
	def setup_nback_test_menu(self, test_number:int, Thread:TonalNbackTestThread|VisuoTonalNbackTestThread, h_buttons:tuple[QtWidgets.QPushButton, ...]=()): #For the nback tests 
		h_buttons = (self.get_settings_button(),) + h_buttons
		v_buttons = ()
		if test_number == 1:
			test_name = self.translate("Tonal n-back test")
		elif test_number == 2:
			test_name = self.translate("Visuotonal n-back test")
		else:
			raise ValueError("test_number should be 1 or 2")
		
		layout_h, layout_v, test_menu = self.setup_menu(test_name, h_buttons, v_buttons)
		self.test_menus.append(test_menu)
		
		def is_number_of_trials_notes_initial_nback_valid(translate:validators.TranslateCallable, number_of_trials:str, number_of_notes:str, initial_nback:str) -> validators.IsValidErrorMessage:
			if int(number_of_notes) < int(initial_nback) + int(number_of_trials):
				return False, translate("The number of notes needs to be greater than or equal to the initial n-back + number of trials.")
			return True, ""
		
		form = forms.FormPresets(layout_v, self.translate)
		player_ID_field = form.create_player_ID_field()
		number_of_trials_field = form.create_number_of_trials_field("6")
		number_of_sequences_field = form.create_field(self.translate("Number of sequences"), "10", forms.FormField.is_non_empty, validator=form.get_StrictIntValidator())
		number_of_notes_field = form.create_number_of_notes_field("10")
		initial_nback_field = form.create_field(self.translate("Starting n-back"), "1",  forms.FormField.is_non_empty, validator=form.get_StrictIntValidator())
		bpm_field = form.create_bpm_field()
		instrument_field = form.create_instrument_field()
		form.summon_reset_button()
		form.add_validation_multiple_fields(is_number_of_trials_notes_initial_nback_valid, number_of_trials_field, number_of_notes_field, initial_nback_field)

		layout_v_h = QtWidgets.QHBoxLayout()
		'''
		random_radio_button = QtWidgets.QRadioButton(self.translate("Random"))
		random_radio_button.setFont(PyQt6_utils.FONT)
		random_radio_button.setStyleSheet("font-size: 20px;")
		random_radio_button.setChecked(True)
		layout_v_h.addWidget(random_radio_button)'''

		random_c_major_radio_button = QtWidgets.QRadioButton(self.translate("Random C major scale")) #TODO: add more options, such as a dropdown menu with the main scales and a field for defining a custom one.
		random_c_major_radio_button.setFont(QtGui.QFont(PyQt6_utils.FONT, PyQt6_utils.STANDARD_FONT_SIZE))
		random_c_major_radio_button.setStyleSheet("font-size: 20px;")
		random_c_major_radio_button.setChecked(True)
		layout_v_h.addWidget(random_c_major_radio_button)
		layout_v.addLayout(layout_v_h)
		'''
		tonal_c_major_radio_button = QtWidgets.QRadioButton(self.translate("Tonal C major scale"))
		tonal_c_major_radio_button.setFont(PyQt6_utils.FONT)
		tonal_c_major_radio_button.setStyleSheet("font-size: 20px;")
		layout_v_h.addWidget(tonal_c_major_radio_button) '''


		play_test_button = QtWidgets.QPushButton(self.translate("Play") + ' ' + test_name.lower())
		play_test_button.setFont(QtGui.QFont(PyQt6_utils.FONT, PyQt6_utils.STANDARD_FONT_SIZE))
		#button_size = play_test_button.sizeHint()

		def play_test() -> None:
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
				nonlocal loading_label
				loading_label.deleteLater()
				answers, question, layout_v_h, destroy_question = PyQt6_utils.create_question(layout_v, self.translate("Ready for the next sequence?"), self.translate("Yes"))
				yes_button = answers[0]
				yes_button.setStyleSheet("background-color: green; font-size: 50px;")
				def continue_test():
					destroy_question()
					countdown()
				yes_button.clicked.connect(continue_test)
			
			def create_loading_label():
				nonlocal loading_label
				loading_label = QtWidgets.QLabel(self.translate("Loading")+ '...')
				loading_label.setStyleSheet("font-size: 50px;")
				loading_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
				layout_v.addWidget(loading_label)
			
			number_of_sequences = int(number_of_sequences_field.text_box.text())
			initial_nback = int(initial_nback_field.text_box.text())
			player_name = player_ID_field.text_box.text()
			number_of_notes = int(number_of_notes_field.text_box.text())
			bpm = float(Fraction((bpm_field.text_box.text())))
			instrument = instrument_field.text_box.text()
			number_of_trials = int(number_of_trials_field.text_box.text())
			loading_label = None
			if random_c_major_radio_button.isChecked():
				scale = scales.Scale.get_parallel_mode(scales.Diatonic_Modes, 'C', 0)

			self.notes_thread = Thread(number_of_trials, player_name, number_of_sequences, initial_nback, number_of_notes, bpm, instrument, scale=scale)
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
		form.summon_validate_all_button(validate_all_button=play_test_button, post_validation_func=play_test)
		layout_v.addWidget(play_test_button)

class TonalNbackTestGUI(NbackTestGUI):

	def get_tonal_nback_test_button(self):
		return PyQt6_utils.get_txt_button(self.translate('Tonal n-back test'), lambda: self.goto_frame(self.test_menus[0]))

	def setup_tonal_nback_info_frame(self):
		title = self.translate("Tonal n-back test")
		#font = QFont("Arial", 12)
		text_body = self.translate("In this test, you will hear a sequence of notes.\nAfter the notes are played, you will be asked if the last note in the\nsequence is the same as another specific note in the sequence.")
		image = QtWidgets.QLabel()
		image.setPixmap(QtGui.QPixmap("static/nback_example.png").scaled(1000, 1000, QtCore.Qt.AspectRatioMode.KeepAspectRatio))
		text_label = QtWidgets.QLabel(text_body)
		#text_label.setFont(font)
		v_widgets = (text_label, image)
		layout_h, layout_v, self.tonal_nback_info_frame = self.setup_menu(title, widgets_v=v_widgets)

	def get_tonal_nback_info_frame(self):
		#summon_info_popup = lambda: PyQt6_utils.get_msg_box(self.translate("Help"), info_text, QtWidgets.QMessageBox.Icon.Information).exec()
		info_button = PyQt6_utils.get_button_with_image(self.info_image, lambda:self.goto_frame(self.tonal_nback_info_frame))
		return info_button
	
	def setup_tonal_nback_test_menu(self):
		self.setup_nback_test_menu(1, TonalNbackTestThread, h_buttons=(self.get_tonal_nback_info_frame(),))
		
class VisuotonalNbackTestGUI(NbackTestGUI):

	def setup_visuotonal_nback_menu(self):
		self.setup_nback_test_menu(2, VisuoTonalNbackTestThread)

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
		return PyQt6_utils.get_txt_button(self.translate('Visuotonal n-back test'), lambda: self.goto_frame(self.test_menus[1]))