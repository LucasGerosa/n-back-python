from PyQt6.QtCore import Qt, QSize, QRegularExpression, QCoreApplication,  QThread, QObject, pyqtSignal
from PyQt6.QtGui import QFont, QIcon, QPixmap, QGuiApplication, QIntValidator, QDoubleValidator, QRegularExpressionValidator, QPalette, QColor
from PyQt6 import QtWidgets, QtCore, QtGui
from PyQt6.QtWidgets import QApplication, QLabel, QMainWindow, QFrame, QPushButton, QVBoxLayout, QHBoxLayout, QWidget, QSpacerItem, QSizePolicy, QLineEdit, QMessageBox
import sys; import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import notes
from utils.defaults import *
from utils import PyQt6_utils
from test_threads import Test1Thread, Test2Thread, TestThread, Test3Thread
import run
from typing import Dict, Optional, List
from utils import notes_config
from TestCase import TestCase, TonalDiscriminationTaskTestCase
import asyncio
from collections.abc import Iterable
import re
import gettext
import time

# Specify the translation domain and path to the translations directory
print(os.path.dirname(__file__),"\n")
	
class MyGUI(QMainWindow):

	def __init__(self):
		super().__init__()
		self.removed_widgets = []
		set_language(notes_config.get_all_settings()["language"])
		self.primary_screen = QGuiApplication.primaryScreen()
		self.setWindowTitle(PROJECT_NAME)
		self.setGeometry(0, 0, 1200, 600)
		self.showMaximized()
		self.back_arrow = QIcon("static/back_button.png")
		self.settings_image = QIcon("static/settings.png")
		self.info_image = QIcon("static/information_button.png")
		self.play_image = QIcon("static/play_button.png")
		self.debug_image = QIcon("static/debug.png")
		self.stop_image = QIcon("static/stop_button.jpg")

		self.test_menus = []
		self.setup_main_menu()
		self.setup_settings()
		self.setup_play_menu()
		self.setup_debug_menu()
		self.setup_test1_menu()
		self.setup_test2_menu()
		self.setup_test3_menu()
		self.setup_test2_frame()
		self.setup_info_frame1()
		self.setup_info_frame3()

		self.states = [self.main_menu]
		self.setCentralWidget(self.main_menu)
		#self.main_menu.show()
		self.notes_thread = None

		# configure the main_menu frame to make the center column expandable
		'''
		main_menu_layout = QHBoxLayout(self.main_menu)
		main_menu_layout.addStretch()
		#main_menu_layout.setStretchFactor(main_menu_layout.itemAt(0), 1)
		main_menu_layout.addStretch()'''

	def keyPressEvent(self, event):
		if event.key() == Qt.Key.Key_F11:
			if self.isFullScreen():
				self.showNormal()
				self.showMaximized()
			else:
				self.showFullScreen()

	def setup_main_menu(self):
		h_buttons = (self.get_settings_button(), self.get_play_button())
		layout_h, layout_v, self.main_menu = self.setup_menu(_("Main menu"), h_buttons)
	
	def setup_test2_frame(self):
		self.test2_frame = QFrame(self)
		layout_grid = QtWidgets.QGridLayout()
		self.test2_frame.setLayout(layout_grid)
		minimum_x, minimum_y = 50, 50
		spacer1_h = QWidget()
		spacer1_h.setMinimumSize(minimum_x, minimum_y)
		spacer2_h = QWidget()
		spacer2_h.setMinimumSize(minimum_x, minimum_y)
		spacer1_v = QWidget()
		spacer1_v.setMinimumSize(200, minimum_y)
		spacer2_v = QWidget()
		spacer2_v.setMinimumSize(200, minimum_y)
		layout_grid.addWidget(spacer1_h, 0, 1)
		layout_grid.addWidget(spacer2_h, 2, 1)

		layout_grid.addWidget(spacer1_v, 1, 0)
		layout_grid.addWidget(spacer2_v, 1, 2)

	def setup_settings(self):
		def create_save_function(text_box, setting_name):
			def save_function():
				notes_config.change_setting(setting_name, text_box.text())

			return save_function

		h_buttons = self.get_debug_button(),
		v_buttons = self.get_main_menu_button(),
		layout_h, layout_v, self.settings = self.setup_menu(_("Settings"), widgets_h=h_buttons, widgets_v=v_buttons)
		all_settings = notes_config.get_all_settings()
		layout_v_h = QHBoxLayout()
		layout_v.addLayout(layout_v_h)
		layout_v_h.addWidget(QLabel(_("Setting Name:")))
		layout_v_h.addWidget(QLabel(_("Setting value:")))

		setting_dict: Dict[str, QLineEdit] = {}

		for setting_name in all_settings:
			layout_v_h = QHBoxLayout()

			setting_name_label = QLabel(_(setting_name.capitalize()))
			layout_v_h.addWidget(setting_name_label)

			text_box = QLineEdit()
			setting_value = all_settings.get(setting_name)
			text_box.setText(setting_value)
			text_box.returnPressed.connect(create_save_function(text_box, setting_name))
			layout_v_h.addWidget(text_box)
			setting_dict[setting_name] = text_box

			layout_v.addLayout(layout_v_h)
		if setting_dict == {}:
			return

		save_button = QPushButton(_("Save"))

		def save_all():
			for setting_name in setting_dict:
				text_box = setting_dict[setting_name]
				user_input = text_box.text()
				if setting_name == "language":
					language_path = os.path.join(TRANSLATIONS_FOLDER, user_input)
					if not os.path.isdir(language_path):
						PyQt6_utils.get_msg_box(_("Settings failed to save"), _("Language doesn't exist; Please enter a valid language."), QMessageBox.Icon.Warning).exec()
						return
						
				notes_config.change_setting(setting_name, user_input)

				
			PyQt6_utils.get_msg_box(_("Settings saved"), _("Settings have been successfully saved.")).exec()

		save_button.clicked.connect(save_all)
		layout_v.addWidget(save_button)

		reset_button = QPushButton(_("Reset settings"))

		def reset_settings():
			config = notes_config.reset_settings()
			for setting_name in setting_dict:
				text_box = setting_dict[setting_name]
				text_box.setText(config[setting_name])
			PyQt6_utils.get_msg_box(_("Settings reset"), _("Settings have been successfully reset.")).exec()

		reset_button.clicked.connect(reset_settings)
		layout_v.addWidget(reset_button)
	
	def setup_play_menu(self):
		h_buttons = self.get_settings_button(),
		v_buttons = self.get_main_menu_button(), self.get_test1_button(), self.get_test2_button(), self.get_test3_button()
		layout_h, layout_v, self.play_menu = self.setup_menu(_("Choose a test"), h_buttons, v_buttons)
	
	def setup_info_frame1(self):
		title = _("Tonal nback test")
		text_body = _("""In this test, you will hear a sequence of notes.
After the notes are played, you will be asked if the last note in the
sequence is the same as another specific note in the sequence.
		""")
		image = QLabel()
		image.setPixmap(QPixmap("static/nback_example.png").scaled(1000, 1000, Qt.AspectRatioMode.KeepAspectRatio))
		v_widgets = (QLabel(text_body), image)
		layout_h, layout_v, self.info_frame1 = self.setup_menu(title, widgets_v=v_widgets)
	
	def setup_info_frame3(self):
		title = _("Tonal discrimination task")
		text_body = _("In this test, you will hear a sequence of notes. \nThen, there will be a 1-second pause, and you will hear another sequence of notes. \nYou will be asked if the second sequence is the same as the first one.")
		tdt_image = QLabel()
		tdt_image.setPixmap(QPixmap("static/TDT_example.png").scaled(500, 500, Qt.AspectRatioMode.KeepAspectRatio))
		v_widgets = (QLabel(text_body), tdt_image)
		layout_h, layout_v, self.info_frame3 = self.setup_menu(title, widgets_v=v_widgets)


	def setup_debug_menu(self):
		v_buttons = ()
		h_buttons = ()
		layout_h, layout_v, self.debug_menu = self.setup_menu(_("Debug"), h_buttons, v_buttons)

	def setup_test1_menu(self):
		self.setup_test_menu(1, Test1Thread, h_buttons=(self.get_info_button_1(),))

	def setup_test2_menu(self):
		self.setup_test_menu(2, Test2Thread)
	
	def setup_test3_menu(self):
		Thread = Test3Thread
		h_buttons = (self.get_settings_button(), self.get_info_button_3())
		v_buttons = ()
		test_name = _("Tonal Discrimination Task")
		layout_h, layout_v, test_menu = self.setup_menu(test_name, h_buttons, v_buttons)
		self.test_menus.append(test_menu)
		player_name_q = _("Player name")
		test_case_q = _("How many trials?")
		notes_quantity_q = _("How many notes (int)")
		bpm_q = _("How many bpm (float)")
		instrument_q = _("Instrument (piano or guitar)")
		labels = (player_name_q, test_case_q, notes_quantity_q, bpm_q, instrument_q)
		set_text = tuple(["Gerosa", '10', '4', str(DEFAULT_BPM), DEFAULT_INSTRUMENT])
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
				PyQt6_utils.get_msg_box(_("Incorrect input"), f"{_('Please enter an integer bigger than 0, not')} \"{text}\"", QMessageBox.Icon.Warning).exec()

		def msgbox_if_float(q):
			is_float, text = check_isfloat(q)
			if not is_float:
				PyQt6_utils.get_msg_box(_("Incorrect input"), f"{_('Please enter a fraction or a decimal bigger than 0, not')} \"{text}\"", QMessageBox.Icon.Warning).exec()
	
		def msgbox_if_instrument(q):
			is_instrument, text = check_isinstrument(q)
			if not is_instrument:
				PyQt6_utils.get_msg_box(_("Incorrect input"), _("Please enter a valid instrument, not \"{text}\""), QMessageBox.Icon.Warning).exec()

		def msgbox_if_empty(q):
			is_empty = check_isempty(q)
			if not is_empty:
				PyQt6_utils.get_msg_box(_("Incorrect input"), _("Please enter something."), QMessageBox.Icon.Warning).exec()

		def connect(q, func): # Tells python what to do when the user finishes typing in the msg boxes
			column_text_box[labels.index(q)].editingFinished.connect(lambda:func(q))

		connect(test_case_q, msgbox_if_digit)
		connect(notes_quantity_q, msgbox_if_digit)
		connect(bpm_q, msgbox_if_float)
		connect(instrument_q, msgbox_if_instrument)
		connect(player_name_q, msgbox_if_empty)

		reset_button = QPushButton(_("Reset"))
		layout_v.addWidget(reset_button)
		def reset():
			i = 0
			for text in set_text:
				column_text_box[i].setText(text)
				i += 1
		reset_button.clicked.connect(reset)
		play_test_button = QPushButton(_("Play") + ' ' + test_name)
		play_test_button.setFont(PyQt6_utils.FONT)
		button_size = play_test_button.sizeHint()

		test_layout = None
		def play_test():
			nonlocal test_layout
			layout_h, layout_v, test1_test = self.setup_menu(back_button=False)
			test_layout = layout_v
			self.states.append(self.takeCentralWidget())
			self.setCentralWidget(test1_test)
			def get_text(q):
				return column_text_box[labels.index(q)].text()
			
			incorrect_fields:list[str] = []
			player_name = get_text(player_name_q)
			if player_name == "":
				incorrect_fields.append(player_name_q)
			for q in (test_case_q, notes_quantity_q):
				if not check_isdigit(q)[0]:
					incorrect_fields.append(q)
			if not check_isfloat(bpm_q)[0]:
				incorrect_fields.append(bpm_q)
			if not check_isinstrument(instrument_q)[0]:
				incorrect_fields.append(instrument_q)
			
			if incorrect_fields != []:
				PyQt6_utils.get_msg_box(_("Incorrect input"), _("The following fields are incorrect or incomplete:\n\n")+ '\n'.join(incorrect_fields)+_(".\n\n Correct them and try again"), QMessageBox.Icon.Warning).exec()
				return
			
			def is_notes_quantity_valid():
				notes_quantity = column_text_box[labels.index(notes_quantity_q)].text()
				return int(notes_quantity) <= len(TONAL_DISCRIMINATION_TASK_SEQUENCES[0])

			if not is_notes_quantity_valid():
				PyQt6_utils.get_msg_box(_("Incorrect input"), _("The quantity of notes + trial - 1 needs to be greater than nback"), QMessageBox.Icon.Warning).exec()
				return
			
			@QtCore.pyqtSlot()
			def on_execute_loop_thread_finished():
				if not isinstance(self.notes_thread, TestThread):
					raise ValueError(_("Notes thread is not an instance of TestThread"))
				self.notes_thread.deleteLater()
				self.setCentralWidget(self.states.pop())
			
			def countdown():
				seconds_remaining = 3
				timer = QtCore.QTimer(self)
				label = QLabel('3', self)
				label.setAlignment(Qt.AlignmentFlag.AlignCenter)
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
				answers, question, layout_v_h, destroy_question = PyQt6_utils.create_question(layout_v, _("Ready for the next trial?"), _("Yes"))
				yes_button = answers[0]
				yes_button.setStyleSheet("background-color: green; font-size: 50px;")
				def continue_test():
					destroy_question()
					countdown()
				yes_button.clicked.connect(continue_test)
			
			def ask_continue_test_between_note_groups():
				'''
				answers, question, layout_v_h, destroy_question = PyQt6_utils.create_question(layout_v, _("Ready for the next sequence?"), _("Yes"))
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
				loadingLabel = QLabel(_("Loading")+ '...')
				loadingLabel.setStyleSheet("font-size: 50px;")
				loadingLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
				layout_v.addWidget(loadingLabel)
			
			test_case = int(get_text(test_case_q))
			notes_quantity = int(get_text(notes_quantity_q))
			bpm = float(get_text(bpm_q))
			instrument = get_text(instrument_q)
			#play_test_button.setEnabled(False)
			loadingLabel = None

			self.notes_thread = Thread(layout_v, 0, player_name, test_case, 0, notes_quantity, bpm, instrument) #0  is a placeholder for nback, which is not used in this test
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
		return test_layout

	def setup_test_menu(self, test_number:int, Thread:TestThread, h_buttons:tuple[QPushButton, ...]=()):
		h_buttons = (self.get_settings_button(),) + h_buttons
		v_buttons = ()
		if test_number == 1:
			test_name = _("Teste nback tonal")
		elif test_number == 2:
			test_name = _("Visuotonal nback test")
		else:
			raise ValueError("test_number should be 1 or 2")
		
		layout_h, layout_v, test_menu = self.setup_menu(test_name, h_buttons, v_buttons)
		self.test_menus.append(test_menu)
		player_name_q = _("Player name")
		test_case_q = _("How many sequences?")
		trials_q = _("How many trials?")
		n_back_q = _("n-back (int)")
		notes_quantity_q = _("How many notes (int)")
		bpm_q = _("How many bpm (float)")
		instrument_q = _("Instrument (piano or guitar)")
		labels = (player_name_q, test_case_q, trials_q, n_back_q, notes_quantity_q, bpm_q, instrument_q)
		set_text = tuple(["Gerosa", '10', '6', '1', '10', str(DEFAULT_BPM), DEFAULT_INSTRUMENT])
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
				PyQt6_utils.get_msg_box(_("Incorrect input"), f"{_('Please enter an integer bigger than 0, not')} \"{text}\"", QMessageBox.Icon.Warning).exec()

		def msgbox_if_float(q):
			is_float, text = check_isfloat(q)
			if not is_float:
				PyQt6_utils.get_msg_box(_("Incorrect input"), f"{_('Please enter a fraction or a decimal bigger than 0, not')} \"{text}\"", QMessageBox.Icon.Warning).exec()

		
		def msgbox_if_instrument(q):
			is_instrument, text = check_isinstrument(q)
			if not is_instrument:
				PyQt6_utils.get_msg_box(_("Incorrect input"), _("Please enter a valid instrument, not \"{text}\""), QMessageBox.Icon.Warning).exec()

		def msgbox_if_empty(q):
			is_empty = check_isempty(q)
			if not is_empty:
				PyQt6_utils.get_msg_box(_("Incorrect input"), _("Please enter something."), QMessageBox.Icon.Warning).exec()

		def connect(q, func): # Tells python what to do when the user finishes typing in the msg boxes
			column_text_box[labels.index(q)].editingFinished.connect(lambda:func(q))

		connect(test_case_q, msgbox_if_digit)
		connect(n_back_q, msgbox_if_digit)
		connect(notes_quantity_q, msgbox_if_digit)
		connect(bpm_q, msgbox_if_float)
		connect(instrument_q, msgbox_if_instrument)
		connect(player_name_q, msgbox_if_empty)
		connect(trials_q, msgbox_if_digit)

		layout_v_h = QtWidgets.QHBoxLayout()
		'''
		random_radio_button = QtWidgets.QRadioButton(_("Random"))
		random_radio_button.setFont(PyQt6_utils.FONT)
		random_radio_button.setStyleSheet("font-size: 20px;")
		random_radio_button.setChecked(True)
		layout_v_h.addWidget(random_radio_button)'''

		random_c_major_radio_button = QtWidgets.QRadioButton(_("Random C major scale"))
		random_c_major_radio_button.setFont(PyQt6_utils.FONT)
		random_c_major_radio_button.setStyleSheet("font-size: 20px;")
		random_c_major_radio_button.setChecked(True)
		layout_v_h.addWidget(random_c_major_radio_button)
		'''
		tonal_c_major_radio_button = QtWidgets.QRadioButton(_("Tonal C major scale"))
		tonal_c_major_radio_button.setFont(PyQt6_utils.FONT)
		tonal_c_major_radio_button.setStyleSheet("font-size: 20px;")
		layout_v_h.addWidget(tonal_c_major_radio_button) '''

		
		layout_v.addLayout(layout_v_h)

		reset_button = QPushButton(_("Reset"))
		layout_v.addWidget(reset_button)
		def reset():
			i = 0
			for text in set_text:
				column_text_box[i].setText(text)
				i += 1
		reset_button.clicked.connect(reset)
		play_test_button = QPushButton(_("Play") + ' ' + test_name)
		play_test_button.setFont(PyQt6_utils.FONT)
		button_size = play_test_button.sizeHint()

		test_layout = None
		def play_test():
			nonlocal test_layout
			layout_h, layout_v, test1_test = self.setup_menu(back_button=False)
			test_layout = layout_v
			self.states.append(self.takeCentralWidget())
			self.setCentralWidget(test1_test)
			def get_text(q):
				return column_text_box[labels.index(q)].text()
			
			incorrect_fields:list[str] = []
			player_name = get_text(player_name_q)
			if player_name == "":
				incorrect_fields.append(player_name_q)
			for q in (test_case_q, n_back_q, trials_q, notes_quantity_q):
				if not check_isdigit(q)[0]:
					incorrect_fields.append(q)
			if not check_isfloat(bpm_q)[0]:
				incorrect_fields.append(bpm_q)
			if not check_isinstrument(instrument_q)[0]:
				incorrect_fields.append(instrument_q)
			
			if incorrect_fields != []:
				PyQt6_utils.get_msg_box(_("Incorrect input"), _("The following fields are incorrect or incomplete:\n\n")+ '\n'.join(incorrect_fields)+_(".\n\n Correct them and try again"), QMessageBox.Icon.Warning).exec()
				return
			
			def is_notes_quantity_valid():
				notes_quantity = column_text_box[labels.index(notes_quantity_q)].text()
				n_back = column_text_box[labels.index(n_back_q)].text()
				test_case = column_text_box[labels.index(test_case_q)].text()
				return int(notes_quantity) > int(n_back) - 1

			if not is_notes_quantity_valid():
				PyQt6_utils.get_msg_box(_("Incorrect input"), _("The quantity of notes + trials - 1 needs to be greater than nback"), QMessageBox.Icon.Warning).exec()
				return
			
			@QtCore.pyqtSlot()
			def on_execute_loop_thread_finished():
				if not isinstance(self.notes_thread, TestThread):
					raise ValueError(_("Notes thread is not an instance of TestThread"))
				self.notes_thread.deleteLater()
				self.setCentralWidget(self.states.pop())
			
			def countdown():
				seconds_remaining = 3
				timer = QtCore.QTimer(self)
				label = QLabel('3', self)
				label.setAlignment(Qt.AlignmentFlag.AlignCenter)
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
				answers, question, layout_v_h, destroy_question = PyQt6_utils.create_question(layout_v, _("Ready for the next sequence?"), _("Yes"))
				yes_button = answers[0]
				yes_button.setStyleSheet("background-color: green; font-size: 50px;")
				def continue_test():
					destroy_question()
					countdown()
				yes_button.clicked.connect(continue_test)
			
			def create_loading_label():
				nonlocal loadingLabel
				loadingLabel = QLabel(_("Loading")+ '...')
				loadingLabel.setStyleSheet("font-size: 50px;")
				loadingLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
				layout_v.addWidget(loadingLabel)
			
			test_case = int(get_text(test_case_q))
			n_back = int(get_text(n_back_q))
			notes_quantity = int(get_text(notes_quantity_q))
			bpm = float(get_text(bpm_q))
			instrument = get_text(instrument_q)
			trials = int(get_text(trials_q))
			#play_test_button.setEnabled(False)
			loadingLabel = None
			if random_c_major_radio_button.isChecked():
				mode = RANDOM_C_MAJOR_MODE
			'''
			elif tonal_c_major_radio_button.isChecked():
				mode = TONAL_C_MAJOR_MODE
			else:
				mode = RANDOM_MODE '''

			self.notes_thread = Thread(layout_v, trials, player_name, test_case, n_back, notes_quantity, bpm, instrument, mode=mode)
			self.notes_thread.finished.connect(on_execute_loop_thread_finished)
			self.notes_thread.start_execution.connect(ask_continue_test)
			self.notes_thread.pre_start_execution.connect(create_loading_label)
			self.notes_thread.started_trial_signal.connect(lambda nback: self.warn_user_different_trial(layout_v, nback))

			if Thread is Test2Thread:
				note_label = None
				layout_grid = self.test2_frame.layout()
				def print_note_label(note_name):
					nonlocal note_label
					note_label = QLabel(note_name)
					note_label.setStyleSheet("font-size: 300px;")
					layout_grid.addWidget(note_label, 1, 1, Qt.AlignmentFlag.AlignTop)

				def delete_note_label():
					if note_label is None:
						raise ValueError(_("note_label should not be None. This means that you tried to delete the note without printing it to the interface first"))
					note_label.deleteLater()
				
				hint_label = None
				def print_hint_label(note_name):
					nonlocal hint_label
					hint_label = QLabel(note_name)
					hint_label.setStyleSheet("font-size: 65px;")
					#hint_label.setSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed)
					layout_grid.addWidget(hint_label, 2, 2, Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignBottom)
				
				def delete_hint_label():
					if hint_label is None:
						raise ValueError(_("hint_label should not be None. This means that you tried to delete the note without printing it to the interface first"))
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
		return test_layout

	def setup_menu(self, title:str="", widgets_h:tuple[QWidget, ...]=(), widgets_v:tuple[QWidget, ...]=(), back_button:bool=True):
		frame = QFrame(self)
		layout_h_v = QHBoxLayout()
		layout_v_h_v = QVBoxLayout()
		layout_v = QVBoxLayout(frame)
		if back_button:
			layout_h_v.addWidget(self.get_back_button())

		for widget in widgets_h:
			layout_h_v.addWidget(widget)
		#layout_h_v.addStretch()
		
		layout_v_h_v.addWidget(PyQt6_utils.create_frame_title(title))
		for widget in widgets_v:
			layout_v_h_v.addWidget(widget)
		#layout_h_v.addStretch()
		#layout_v_h_v.setAlignment(Qt.AlignmentFlag.AlignCenter)

		#layout_h_v.addItem(QSpacerItem(300, 20, QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.Minimum))
		layout_h_v.addLayout(layout_v_h_v)
		#layout_h_v.addItem(QSpacerItem(300, 20, QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.Minimum))
		layout_v.addLayout(layout_h_v)
		layout_v.addStretch()
		#frame.setLayout(layout_h_v)
		layout_h_v.setAlignment(Qt.AlignmentFlag.AlignCenter)
		return layout_h_v, layout_v_h_v, frame

	def center_offset_widget(self, width=0, height=0):
		x,y = PyQt6_utils.get_center(width, height)
		window_middle = self.primary_screen.geometry().width() // 2
		return window_middle - x, window_middle - y
	
	def center_widget_x(self, widget:QWidget, y:int, width:int, height:int):
		widget.setGeometry(self.center_offset_widget(width=widget.width())[0], y, width, height)

	def destroy_all_widgets(self):
		for widget in self.children():
			widget.deleteLater()

	def goto_frame(self, frame:QFrame):
		#self.current_frame.hide()
		#frame.show() # Remove the current central widget without deleting it
		#self.removed_widgets.append(removed_widget)
		self.states.append(self.takeCentralWidget())
		self.setCentralWidget(frame)
	
	def go_back(self):
		if not self.states == []:
			current_frame = self.states.pop()
			self.removed_widgets.append(self.takeCentralWidget())
			self.setCentralWidget(current_frame)

	def get_test1_button(self):
		return PyQt6_utils.get_txt_button(_('Tonal nback test'), lambda: self.goto_frame(self.test_menus[0]))

	def get_test2_button(self):
		return PyQt6_utils.get_txt_button(_('Visuotonal nback test'), lambda: self.goto_frame(self.test_menus[1]))
	
	def get_test3_button(self):
		return PyQt6_utils.get_txt_button(_('Tonal discrimination task'), lambda: self.goto_frame(self.test_menus[2]))
	
	def get_main_menu_button(self):
		return PyQt6_utils.get_txt_button(_('Main menu'), lambda: self.goto_frame(self.main_menu))

	def get_back_button(self):
		return PyQt6_utils.get_button_with_image(self.back_arrow, self.go_back)

	def get_settings_button(self):
		return PyQt6_utils.get_button_with_image(self.settings_image, lambda: self.goto_frame(self.settings))

	def get_play_button(self):
		return PyQt6_utils.get_button_with_image(self.play_image, lambda: self.goto_frame(self.play_menu))

	def get_debug_button(self):
		def debug():
			self.goto_frame(self.debug_menu)
			
			TestCase.debug()
		
		return PyQt6_utils.get_button_with_image(self.debug_image, debug)

	def get_exit_button(self):
		return PyQt6_utils.get_txt_button(_('Exit'), self.close)

	def get_stop_button(self, thread:Test1Thread):
		button = QPushButton()
		button.setIcon(self.stop_image)
		button.resize(PyQt6_utils.BUTTON_SIZE, PyQt6_utils.BUTTON_SIZE)
		button.setIconSize(button.size())
		def stop():
			thread.stop = True
			button.deleteLater()
			PyQt6_utils.get_msg_box(_("Test stopped"), _("The test was stopped, just wait for the notes to finish playing before playing another test."), QMessageBox.Icon.Information).exec()
		button.clicked.connect(stop) 
		return button
	
	def get_info_button_1(self):
		#summon_info_popup = lambda: PyQt6_utils.get_msg_box(_("Help"), info_text, QMessageBox.Icon.Information).exec()
		info_button = PyQt6_utils.get_button_with_image(self.info_image, lambda:self.goto_frame(self.info_frame1))
		return info_button

	def get_info_button_3(self):
		#summon_info_popup = lambda: PyQt6_utils.get_msg_box(_("Help"), info_text, QMessageBox.Icon.Information).exec()
		info_button = PyQt6_utils.get_button_with_image(self.info_image, lambda:self.goto_frame(self.info_frame3))
		return info_button

	@QtCore.pyqtSlot(QVBoxLayout, TestCase)
	def create_questions(self, layout, testCase:TestCase):
		if not isinstance(self.notes_thread, TestThread):
			raise ValueError(_("Notes thread is not an instance of TestThread"))
		nback = testCase.nBack
		if nback == 1:
			question_text = _("Is the last played note the same as the previous note?")
		elif nback == 2:
			question_text = _("Is the last played note the same as the note before the previous note?")
		elif nback == 3:
			question_text = _("Is the last played note the same as the note three places before it?")
		else:
			question_text = _("Is the last played note the same as the {}th note before the last?").format(nback)
		answers, question, layout_v_h, destroy_yes_no = PyQt6_utils.create_question(layout, question_text, _("Yes"), _("No"))
		yes_button, no_button = answers
		yes_button.setStyleSheet("background-color: green; font-size: 50px;")
		no_button.setStyleSheet("background-color: red; font-size: 50px;")
		'''	def confirm():
			answer = 1 if yes_button.isChecked() else 2
			self.validateAnswer(answer=answer)'''
		def yes():
			testCase.validateAnswer(answer=1)
			destroy_yes_no()
			self.notes_thread.wait_condition.wakeOne()

		def no():
			testCase.validateAnswer(answer=2)
			destroy_yes_no()
			self.notes_thread.wait_condition.wakeOne()

		yes_button.clicked.connect(yes)
		no_button.clicked.connect(no)
	
	@QtCore.pyqtSlot(QVBoxLayout, TonalDiscriminationTaskTestCase)
	def create_questions_tonal_discrimination_task(self, layout, testCase:TonalDiscriminationTaskTestCase):
		if not isinstance(self.notes_thread, TestThread):
			raise ValueError(_("Notes thread is not an instance of TestThread"))
		answers, question, layout_v_h, destroy_yes_no = PyQt6_utils.create_question(layout, _("Are both the sequences the same?"), _("Yes"), _("No"))
		yes_button, no_button = answers
		yes_button.setStyleSheet("background-color: green; font-size: 50px;")
		no_button.setStyleSheet("background-color: red; font-size: 50px;")
		'''	def confirm():
			answer = 1 if yes_button.isChecked() else 2
			self.validateAnswer(answer=answer)'''
		def yes():
			testCase.validateAnswer(answer="same")
			destroy_yes_no()
			self.notes_thread.wait_condition.wakeOne()

		def no():
			testCase.validateAnswer(answer="different")
			destroy_yes_no()
			self.notes_thread.wait_condition.wakeOne()

		yes_button.clicked.connect(yes)
		no_button.clicked.connect(no)	

	@QtCore.pyqtSlot(QVBoxLayout, int)
	def warn_user_different_trial(self, layout, nback:int):
		if nback == 1:
			question_text = _("The following trial will have\nyou compare the last note with the previous note.")
		elif nback == 2:
			question_text = _("The following trial\nwill have you compare the last note\nwith the note before the previous note.")
		elif nback == 3:
			question_text = _("The following trial\nwill have you compare the last note with the note\nthree places before it.")
		else:
			question_text = _("The following trial will have you\ncompare the last note with the {}th note before the last.").format(nback)
		
		question = QLabel(question_text)
		question.setStyleSheet("font-size: 50px;")
		layout.addWidget(question)
		yes_button = QPushButton(_("Ok"))
		yes_button.setStyleSheet("background-color: green; font-size: 50px;")
		question.update()
		QtCore.QTimer.singleShot(1000, lambda: layout.addWidget(yes_button))

		def yes():
			question.deleteLater()
			yes_button.deleteLater()
			self.notes_thread.wait_condition.wakeOne()
		
		yes_button.clicked.connect(yes)


def set_language(language_code):

	try:
		translation = gettext.translation('app', TRANSLATIONS_FOLDER, languages=[language_code])
	except FileNotFoundError:
		# Fallback to default English language if the translation catalog is not found
		raise FileNotFoundError(f'Could not find translation catalog for language code {language_code}')

	#translation.install()
	global _
	_ = translation.gettext

def main():
	app = QApplication([])
	gui = MyGUI()
	gui.show()
	sys.exit(app.exec())
		
if __name__ == "__main__":
	main()
