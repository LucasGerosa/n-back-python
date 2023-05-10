from PyQt6.QtCore import Qt, QSize, QRegularExpression, QCoreApplication,  QThread, QObject, pyqtSignal
from PyQt6.QtGui import QFont, QIcon, QPixmap, QGuiApplication, QIntValidator, QDoubleValidator, QRegularExpressionValidator, QPalette, QColor
from PyQt6 import QtWidgets, QtCore, QtGui
from PyQt6.QtWidgets import QApplication, QLabel, QMainWindow, QFrame, QPushButton, QVBoxLayout, QHBoxLayout, QWidget, QSpacerItem, QSizePolicy, QLineEdit, QMessageBox
import sys; import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import notes
from utils.defaults import *
from utils import PyQt6_utils
import run
from typing import Dict, Optional, List
from utils import notes_config
from TestCase import TestCase
import asyncio
from collections.abc import Iterable
import re
import gettext

# Specify the translation domain and path to the translations directory
print(os.path.dirname(__file__),"\n")

class ExecuteLoopThread(QtCore.QThread):
	finished = QtCore.pyqtSignal()
	done_testCase = QtCore.pyqtSignal(TestCase)
	
	def __init__(self, layout:QtWidgets.QLayout, playerName:str, test_case_n:int, nBack:int, notesQuantity:int, bpm:float=DEFAULT_BPM, instrument:str=DEFAULT_INSTRUMENT):
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
		
	def run(self):
		self.executeLoop()
		self.finished.emit()
	
	def executeLoop(self) -> list|None:

		if self.layout == None:
			raise ValueError(_("Could not find layout_v. This is a bug. Please contact the developers."))
		if not isinstance(self.layout, QtWidgets.QVBoxLayout):
			raise ValueError(_("layout_v %(type)s is not a QVBoxLayout. This is not implemented yet, so it's a bug. Please contact the developers.") % {'type': type(self.layout)})
		
		try:
			testCaseList = []
			
			id = 0
			while id < self.test_case_n and not self.stop:
				
				testCase = TestCase(self.layout, id, self.nBack, self.notesQuantity, self.bpm, self.instrument)
				testCase.note_group.play()
				if self.stop:
					print(_(" was interrupted. Stopping now."))
					return
				testCaseList.append(testCase)
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
	
	def wait_for_signal(self):
		self.mutex.lock()
		self.wait_condition.wait(self.mutex)
		self.mutex.unlock()

	def signal(self):
		self.mutex.lock()
		self.wait_condition.wakeAll()
		self.mutex.unlock()

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
		self.play_image = QIcon("static/play_button.png")
		self.debug_image = QIcon("static/debug.png")
		self.stop_image = QIcon("static/stop_button.jpg")

		self.setup_main_menu()
		self.setup_settings()
		self.setup_play_menu()
		self.setup_debug_menu()
		self.setup_test1_menu()

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

			setting_name_label = QLabel(setting_name)
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
		v_buttons = self.get_main_menu_button(), self.get_test1_button()
		layout_h, layout_v, self.play_menu = self.setup_menu(_("Choose a test"), h_buttons, v_buttons)

	def setup_debug_menu(self):
		v_buttons = ()
		h_buttons = ()
		layout_h, layout_v, self.debug_menu = self.setup_menu(_("Debug"), h_buttons, v_buttons)

	def setup_test1_menu(self):

		h_buttons = (self.get_settings_button(),)

		v_buttons = ()
		layout_h, layout_v, self.test1_menu = self.setup_menu(_("Test1"), h_buttons, v_buttons)
		player_name_q = _("Player name")
		test_case_q = _("How many test cases?")
		n_back_q = _("n-back (int)")
		notes_quantity_q = _("How many notes (int)")
		bpm_q = _("How many bpm (float)")
		instrument_q = _("Instrument (piano or guitar)")
		labels = (player_name_q, test_case_q, n_back_q, notes_quantity_q, bpm_q, instrument_q)
		set_text = tuple(["Gerosa", '2', '2', '3', str(DEFAULT_BPM), DEFAULT_INSTRUMENT])
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

		def is_q1_greater_than_q2(q1, q2):
			text_box1 = column_text_box[labels.index(q1)]
			text_box2 = column_text_box[labels.index(q2)]
			text1 = text_box1.text()
			text2 = text_box2.text()
			return int(text1) > int(text2), text1, text2

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

		def connect(q, func):
			column_text_box[labels.index(q)].editingFinished.connect(lambda:func(q))

		connect(test_case_q, msgbox_if_digit)
		connect(n_back_q, msgbox_if_digit)
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
		play_test_button = QPushButton(_("Play test 1"))
		play_test_button.setFont(PyQt6_utils.FONT)
		button_size = play_test_button.sizeHint()
		def play_test():
			
			def get_text(q):
				return column_text_box[labels.index(q)].text()
			
			incorrect_fields:list[str] = []
			player_name = get_text(player_name_q)
			if player_name == "":
				incorrect_fields.append(player_name_q)
			for q in (test_case_q, n_back_q, notes_quantity_q):
				if not check_isdigit(q)[0]:
					incorrect_fields.append(q)
			if not check_isfloat(bpm_q)[0]:
				incorrect_fields.append(bpm_q)
			if not check_isinstrument(instrument_q)[0]:
				incorrect_fields.append(instrument_q)
			
			if incorrect_fields != []:
				PyQt6_utils.get_msg_box(_("Incorrect input"), _("The following fields are incorrect or incomplete:\n\n")+ '\n'.join(incorrect_fields)+_(".\n\n Correct them and try again"), QMessageBox.Icon.Warning).exec()
				return
			
			if not is_q1_greater_than_q2(notes_quantity_q, n_back_q)[0]:
				PyQt6_utils.get_msg_box(_("Incorrect input"), _("The quantity of notes needs to be greater than nback"), QMessageBox.Icon.Warning).exec()
				return
			
			@QtCore.pyqtSlot()
			def on_execute_loop_thread_finished():
				if not isinstance(self.notes_thread, ExecuteLoopThread):
					raise ValueError(_("Notes thread is not an instance of ExecuteLoopThread"))
				self.notes_thread.deleteLater()
				play_test_button.setEnabled(True)
			
			test_case = int(get_text(test_case_q))
			n_back = int(get_text(n_back_q))
			notes_quantity = int(get_text(notes_quantity_q))
			bpm = float(get_text(bpm_q))
			instrument = get_text(instrument_q)
			play_test_button.setEnabled(False)
			self.notes_thread = ExecuteLoopThread(layout_v, player_name, test_case, n_back, notes_quantity, bpm, instrument)
			self.notes_thread.done_testCase.connect(lambda testCase:self.create_question(layout_v, testCase))
			self.notes_thread.finished.connect(on_execute_loop_thread_finished)
			self.notes_thread.start()
			stop_button = self.get_stop_button(self.notes_thread)
			layout_h.insertWidget(2, stop_button)
		
		def countdown():
			play_test_button.setEnabled(False)
			seconds_remaining = 3
			timer = QtCore.QTimer(self)
			label = QLabel('3', self)
			label.setAlignment(Qt.AlignmentFlag.AlignCenter)
			label.setStyleSheet("font-size: 24px;")
			#nonlocal layout_h
			layout_h.addWidget(label)
			
			def update_countdown():
				nonlocal seconds_remaining 
				#nonlocal timer
				seconds_remaining -= 1
				label.setText(str(seconds_remaining))

				if seconds_remaining == 0:
					timer.stop()
					label.deleteLater()
						
					play_test()
			timer.timeout.connect(update_countdown)
			timer.start(1000)

		#self.center_widget_x(button, 100, button_size.width(), button_size.height())
		play_test_button.clicked.connect(countdown)
		layout_v.addWidget(play_test_button)
	
	def setup_menu(self, title:str, widgets_h:tuple[QWidget, ...]=(), widgets_v:tuple[QWidget, ...]=()):
		frame = QFrame(self)
		layout_h = QHBoxLayout()
		layout_v = QVBoxLayout()
		layout_h.addWidget(self.get_back_button())
		for widget in widgets_h:
			layout_h.addWidget(widget)
		
		layout_v.addWidget(PyQt6_utils.create_frame_title(title))
		for widget in widgets_v:
			layout_v.addWidget(widget)
		#layout_v.setAlignment(Qt.AlignmentFlag.AlignCenter)

		#layout_h.addItem(QSpacerItem(300, 20, QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.Minimum))
		layout_h.addLayout(layout_v)
		#layout_h.addItem(QSpacerItem(300, 20, QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.Minimum))
		frame.setLayout(layout_h)
		layout_h.setAlignment(Qt.AlignmentFlag.AlignCenter)
		return layout_h, layout_v, frame

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
		return PyQt6_utils.get_txt_button(_('Test 1'), lambda: self.goto_frame(self.test1_menu))

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

	def get_stop_button(self, thread:ExecuteLoopThread):
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

	@QtCore.pyqtSlot(QVBoxLayout, TestCase)
	def create_question(self, layout, testCase:TestCase):
		if not isinstance(self.notes_thread, ExecuteLoopThread):
			raise ValueError(_("Notes thread is not an instance of ExecuteLoopThread"))
		question = QLabel(_("Is the last played note the same as the note {} notes ago?").format(testCase.nBack))
		layout.addWidget(question)
		yes_button = QPushButton(_("Yes"))
		no_button = QPushButton(_("No"))
		layout_v_h = QHBoxLayout()
		layout.addLayout(layout_v_h)
		layout_v_h.addWidget(yes_button)
		layout_v_h.addWidget(no_button)

		'''	def confirm():
			answer = 1 if yes_button.isChecked() else 2
			self.validateAnswer(answer=answer)'''
		def yes():
			testCase.validateAnswer(answer=1)
			destroy_question()
			self.notes_thread.wait_condition.wakeOne()

		def no():
			testCase.validateAnswer(answer=2)
			destroy_question()
			self.notes_thread.wait_condition.wakeOne()
		
		def destroy_question():
			layout_v_h.deleteLater()
			yes_button.deleteLater()
			no_button.deleteLater()
			question.deleteLater()

		yes_button.clicked.connect(yes)
		no_button.clicked.connect(no)	

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
