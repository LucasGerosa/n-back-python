'''Contains the GUI for the main tests for the application.'''

import time, sys, os, typing
from source.parent_GUI import parent_GUI
from source.testThreads import VolumeTestThread, TonalDiscriminationTaskTestThread, TestThread, VisuoTonalNbackTestThread, TonalNbackTestThread
from PyQt6 import QtCore, QtWidgets, QtGui
from utils import PyQt6_utils, forms, validators, note_str_utils, notes_config
from utils.defaults import *
from notes import scales
from source.TestCase import NbackTestCase, TonalDiscriminationTaskTestCase, AnswerType, TestCase
from fractions import Fraction
from source.abstract_pages import TestPage, MenuPage, TestMenuPage, NbackTestMenuPage, PlayTestThreadFunc


class SettingsMenuPage(MenuPage):
	def __init__(self, parent:parent_GUI):
		super().__init__(parent, "Settings")

		layout_v_h2_v_h = QtWidgets.QHBoxLayout()
		layout_v_h2_v_h.setContentsMargins(0, 20, 0, 20)
		self.layout_v_h2_v.addLayout(layout_v_h2_v_h)
		layout_v_h2_v_h.addWidget(QtWidgets.QLabel(self.app.translate("Setting Name:")))
		layout_v_h2_v_h.addWidget(QtWidgets.QLabel(self.app.translate("Setting value:")))

		form = forms.FormPresets(self.layout_v_h2_v, self.app.translate)
		def create_field(setting:str, validate_func:validators.SimpleValidateCallable=lambda *_: (True, ""), validator:typing.Optional[QtGui.QValidator]=None) -> None:
			field = form.create_field(self.app.translate(setting).capitalize(), notes_config.get_setting(setting), validate_func, validator=validator)
			field.setting_name = setting #type: ignore
		
		def validate_note_range(translate, note_range:str) -> validators.IsValidErrorMessage:
			if not note_str_utils.get_final_list_notes(note_range): #TODO: not allow notes that don't exist in the input folder
				return False, translate("Invalid note range")
			return True, ""
		
		create_field(notes_config.NOTES_SETTING, validate_note_range, validator=form.get_notes_str_validator())
		create_field(notes_config.NOTE_INTENSITY_SETTING, validator=validators.MultipleOptionsValidator(notes_config.NOTE_INTENSITY_SETTING, VALID_INTENSITIES, self.app.translate)) #TODO: replace with a dropdown menu
		create_field(notes_config.NOTE_VALUE_SETTING, validator=form.get_FractionValidator(bottom=0.0000000001, top=100))
		create_field(notes_config.LANGUAGE_SETTING, validator=validators.MultipleOptionsValidator(notes_config.LANGUAGE_SETTING, notes_config.LEGAL_LANGUAGES)) #TODO: replace with a dropdown menu

		form.summon_reset_button()

		save_button = QtWidgets.QPushButton(self.app.translate("Save"))

		def save_all():

			for field in form.fields:
				notes_config.change_setting(field.setting_name, field.text_box.text())
				
			PyQt6_utils.get_msg_box(self.app.translate("Settings saved"), self.app.translate("Settings have been successfully saved.")).exec()
		form.summon_validate_all_button(save_button, save_all)
		
		reset_button = QtWidgets.QPushButton(self.app.translate("Reset to default"))
		def reset_settings():

			config = notes_config.reset_settings()
			for field in form.fields:
				field.text_box.setText(config[field.setting_name])
			PyQt6_utils.get_msg_box(self.app.translate("Settings reset"), self.app.translate("Settings have been successfully reset.")).exec()

		reset_button.clicked.connect(reset_settings)
		self.layout_v_h2_v.addWidget(reset_button)
		self.layout_v_h2_v.addWidget(self.get_main_menu_button())

	def get_main_menu_button(self):
		return PyQt6_utils.get_txt_button(self.app.translate('Main menu'), lambda: self.app.goto_frame(self.app.tests_menu))

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
		
		def play_test_thread(test_page:TestPage) -> None:
			
			test_page.notes_thread = VolumeTestThread()
			test_page.notes_thread.start_execution.connect(lambda: test_page.loading_label.deleteLater())
			stop_button = self.get_stop_button(test_page.notes_thread)
			test_page.layout_v_h2.addWidget(stop_button)
		
		return play_test_thread

class TonalDiscriminationTaskMenuPage(TestMenuPage):

	def __init__(self, parent):
		test_name = "Tonal Discrimination Task"
		super().__init__(parent, test_name)
		self.set_info_page(test_name, "In this test, you will hear a sequence of notes. Then, there will be a 1-second pause, and you will hear another sequence of notes. You will be asked if the second sequence is the same as the first one.", "static/TDT_example.png", (500, 500))
	
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
		def play_test_thread(test_page:TestPage) -> None:
			
			def ask_continue_test_between_note_groups():
				# answers, question, layout_v_h, destroy_question = PyQt6_utils.create_question(layout_v, self.app.translate("Ready for the next sequence?"), self.app.translate("Yes"))
				# yes_button = answers[0]
				# yes_button.setStyleSheet("background-color: green; font-size: 50px;")
				# def continue_test():
				# 	destroy_question()
				# 	countdown()
				# yes_button.clicked.connect(continue_test)
				time.sleep(1)
				test_page.notes_thread.wait_condition.wakeOne()
			
			number_of_trials = int(number_of_trials_field.text_box.text())
			player_name = player_ID_field.text_box.text()
			number_of_notes = int(number_of_notes_field.text_box.text())
			bpm = float(Fraction((bpm_field.text_box.text())))
			instrument = instrument_field.text_box.text()
			@QtCore.pyqtSlot(TonalDiscriminationTaskTestCase)
			def create_questions(testCase:TonalDiscriminationTaskTestCase):
				test_page.create_question(self.app.translate("Are both the sequences the same?"), testCase)

			test_page.notes_thread = TonalDiscriminationTaskTestThread(player_name, number_of_trials, number_of_notes, bpm, instrument)
			test_page.notes_thread.start_execution.connect(lambda testCase: test_page.ask_continue_test(testCase, "Ready for the next trial?"))
			test_page.notes_thread.between_note_groups.connect(ask_continue_test_between_note_groups)
			test_page.notes_thread.done_testCase.connect(lambda testCase:create_questions(testCase))

		return play_test_thread

class TonalNbackTestMenuPage(NbackTestMenuPage):
	
	def __init__(self, parent):
		test_name = "Tonal n-back test"
		super().__init__(parent, test_name)
		self.set_info_page(test_name, "In this test, you will hear a sequence of notes. After the notes are played, you will be asked if the last note in the sequence is the same as another specific note in the sequence.", "static/nback_example.png", (1000, 1000))

	def post_init_func(self):

		def is_number_of_trials_notes_initial_nback_valid(translate:validators.TranslateCallable, number_of_trials:str, number_of_notes:str, initial_nback:str) -> validators.IsValidErrorMessage:
			if int(number_of_notes) < int(initial_nback) + int(number_of_trials):
				return False, translate("The number of notes needs to be greater than or equal to the initial n-back + number of trials.")
			return True, ""
		
		def play_test(test_page) -> None:
			
			number_of_sequences = int(number_of_sequences_field.text_box.text())
			initial_nback = int(initial_nback_field.text_box.text())
			player_name = player_ID_field.text_box.text()
			number_of_notes = int(number_of_notes_field.text_box.text())
			bpm = float(Fraction((bpm_field.text_box.text())))
			instrument = instrument_field.text_box.text()
			number_of_trials = int(number_of_trials_field.text_box.text())
			
			if True or random_c_major_radio_button.isChecked(): #TODO add more options; this radio button is just to show that the test uses the C major scale.
				scale = scales.Scale.get_parallel_mode(scales.Diatonic_Modes, 'C', 0)
			
			@QtCore.pyqtSlot(NbackTestCase)
			def create_questions(testCase:NbackTestCase):

				match testCase.nBack:
					case 1:
						question_text = self.app.translate("Is the last played note the same as the previous note?")
					case 2:
						question_text = self.app.translate("Is the last played note the same as the note before the previous note?")
					case 3:
						question_text = self.app.translate("Is the last played note the same as the note three places before it?")
					case _:
						question_text = self.app.translate("Is the last played note the same as the {}th note before the last?").format(testCase.nBack)
				test_page.create_question(question_text, testCase)

			@QtCore.pyqtSlot(int)
			def warn_user_different_trial(nback:int):
				match nback:
					case 1:
						question_text = self.app.translate("The following trial will have\nyou compare the last note with the previous note.")
					case 2:
						question_text = self.app.translate("The following trial\nwill have you compare the last note\nwith the note before the previous note.")
					case 3:
						question_text = self.app.translate("The following trial\nwill have you compare the last note with the note\nthree places before it.")
					case _:
						question_text = self.app.translate("The following trial will have you\ncompare the last note with the {}th note before the last.").format(nback)
				
				question = QtWidgets.QLabel(question_text)
				question.setStyleSheet("font-size: 50px;")
				test_page.layout_v_h2_v.addWidget(question)
				yes_button = QtWidgets.QPushButton(self.app.translate("Ok"))
				yes_button.setStyleSheet("background-color: green; font-size: 50px;")
				question.update()
				QtCore.QTimer.singleShot(1000, lambda: test_page.layout_v_h2_v.addWidget(yes_button))
				timer = QtCore.QElapsedTimer()
				timer.start()

				def yes():
					elapsed_seconds = TestPage.get_elapsed_seconds(timer)
					test_page.notes_thread.different_trial_warning_delay_list.append(elapsed_seconds)
					question.deleteLater()
					yes_button.deleteLater()
					test_page.notes_thread.wait_condition.wakeOne()
			
				yes_button.clicked.connect(yes)

			test_page.notes_thread = TonalNbackTestThread(number_of_trials, player_name, number_of_sequences, initial_nback, number_of_notes, bpm, instrument, scale=scale)
			test_page.notes_thread.start_execution.connect(lambda testCase: test_page.ask_continue_test(testCase, "Ready for the next sequence?"))
			test_page.notes_thread.started_trial_signal.connect(lambda nback: warn_user_different_trial(nback))
			test_page.notes_thread.done_testCase.connect(lambda testCase:create_questions(testCase))
		
		form = forms.FormPresets(self.layout_v_h2_v, self.app.translate)
		player_ID_field = form.create_player_ID_field()
		number_of_trials_field = form.create_number_of_trials_field("6")
		number_of_sequences_field = form.create_field(self.app.translate("Number of sequences"), "10", forms.FormField.is_non_empty, validator=form.get_StrictIntValidator())
		number_of_notes_field = form.create_number_of_notes_field("10")
		initial_nback_field = form.create_field(self.app.translate("Starting n-back"), "1",  forms.FormField.is_non_empty, validator=form.get_StrictIntValidator())
		bpm_field = form.create_bpm_field()
		instrument_field = form.create_instrument_field()
		form.summon_reset_button()
		form.add_validation_multiple_fields(is_number_of_trials_notes_initial_nback_valid, number_of_trials_field, number_of_notes_field, initial_nback_field)

		layout_v_h = QtWidgets.QHBoxLayout()

		random_c_major_radio_button = QtWidgets.QRadioButton(self.app.translate("Random C major scale")) #TODO: add more options, such as a dropdown menu with the main scales and a field for defining a custom one.
		random_c_major_radio_button.setFont(QtGui.QFont(PyQt6_utils.FONT, PyQt6_utils.STANDARD_FONT_SIZE))
		random_c_major_radio_button.setStyleSheet("font-size: 20px;")
		random_c_major_radio_button.setChecked(True)
		layout_v_h.addWidget(random_c_major_radio_button)
		self.layout_v_h2_v.addLayout(layout_v_h)
		return play_test
		
class VisuoTonalNbackTestMenuPage(NbackTestMenuPage): #FIXME
	def __init__(self, parent):
		raise NotImplementedError("This test needs to be fixed before it can be used.")
		additional_widgets = ()
		super().__init__(parent, "Visuotonal n-back test", additional_widgets)

		note_label = None
		layout_grid = self.test2_frame.layout()
		def print_note_label(note_name):
			nonlocal note_label
			note_label = QtWidgets.QLabel(note_name)
			note_label.setStyleSheet("font-size: 300px;")
			layout_grid.addWidget(note_label, 1, 1, QtCore.Qt.AlignmentFlag.AlignTop)

		def delete_note_label():
			if note_label is None:
				raise ValueError(self.app.translate("note_label should not be None. This means that you tried to delete the note without printing it to the interface first"))
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
				raise ValueError(self.app.translate("hint_label should not be None. This means that you tried to delete the note without printing it to the interface first"))
			hint_label.deleteLater()
		test_page.notes_thread.test_started_signal.connect(lambda: self.goto_frame(self.test2_frame))
		test_page.notes_thread.print_note_signal.connect(print_note_label)
		test_page.notes_thread.print_hint_signal.connect(print_hint_label)
		test_page.notes_thread.delete_note_signal.connect(delete_note_label)
		test_page.notes_thread.delete_hint_signal.connect(delete_hint_label)
		def done_testCase(testCase):
			self.go_back()
			self.create_questions(layout_v, testCase)

		test_page.notes_thread.done_testCase.connect(lambda testCase:done_testCase(testCase))

class VisuotonalNbackTestGUI: #FIXME: deprecated

	def __init__(self):
		raise NotImplementedError
	
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