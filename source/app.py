'''This file is the main file that should be run to run the program. It ties together all the elements of the GUI and calls functions that deal with the tests (in testThreads.py and TestCase.py)'''
import warnings
warnings.filterwarnings("ignore", message="Couldn't find ffmpeg or avconv", category=RuntimeWarning)
from PyQt6 import QtWidgets, QtCore, QtGui
import sys; import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from utils.defaults import *
from utils import PyQt6_utils, notes_config, note_str_utils
from source.testThreads import TonalNbackTestThread, VisuoTonalNbackTestThread, TestThread
from typing import Dict, Optional, List
from fractions import Fraction
import TestGUI

	
class MyGUI(TestGUI.VolumeTestGUI, TestGUI.TonalNbackTestGUI, TestGUI.TonalDiscriminationTaskGUI, TestGUI.VisuotonalNbackTestGUI):

	def __init__(self):
		super().__init__()
		self.back_arrow = QtGui.QIcon("static/back_button.png")
		self.settings_image = QtGui.QIcon("static/settings.png")
		self.info_image = QtGui.QIcon("static/information_button.png")
		self.play_image = QtGui.QIcon("static/play_button.png")
		self.debug_image = QtGui.QIcon("static/debug.png")
		self.stop_image = QtGui.QIcon("static/stop_button.jpg")

		self.test_menus = []
		self.setup_main_menu()
		self.setup_settings()
		self.setup_play_menu()
		self.setup_debug_menu()

		self.setup_tonal_nback_test_menu()
		self.setup_visuotonal_nback_menu()
		self.setup_TDT_menu()
		self.setup_volume_test_menu() #When creating new tests, put them under this line, or the test_menus will be in the wrong order and you will enter the wrong test menu when trying to enter the test menus

		self.setup_visuotonal_nback_test_frame()
		self.setup_tonal_nback_info_frame()
		self.setup_TDT_info_frame()

		self.states.append(self.main_menu)
		self.setCentralWidget(self.main_menu)
		#self.main_menu.show()
		self.notes_thread = None

		# configure the main_menu frame to make the center column expandable
		'''
		main_menu_layout = QtWidgets.QHBoxLayout(self.main_menu)
		main_menu_layout.addStretch()
		#main_menu_layout.setStretchFactor(main_menu_layout.itemAt(0), 1)
		main_menu_layout.addStretch()'''

	def setup_main_menu(self):
		h_buttons = (self.get_settings_button(), self.get_play_button())
		layout_h, layout_v, self.main_menu = self.setup_menu(self.translate("Main menu"), h_buttons)

	def setup_settings(self):
		def create_save_function(text_box, setting_name):
			def save_function():
				notes_config.change_setting(setting_name, text_box.text())

			return save_function

		h_buttons = self.get_debug_button(),
		v_buttons = self.get_main_menu_button(),
		layout_h, layout_v, self.settings = self.setup_menu(self.translate("Settings"), widgets_h=h_buttons, widgets_v=v_buttons)
		all_settings = notes_config.get_all_settings()
		layout_v_h = QtWidgets.QHBoxLayout()
		layout_v.addLayout(layout_v_h)
		layout_v_h.addWidget(QtWidgets.QLabel(self.translate("Setting Name:")))
		layout_v_h.addWidget(QtWidgets.QLabel(self.translate("Setting value:")))

		setting_dict: Dict[str, QtWidgets.QLineEdit] = {}

		for setting_name in all_settings:
			layout_v_h = QtWidgets.QHBoxLayout()

			setting_name_label = QtWidgets.QLabel(self.translate(setting_name.capitalize()))
			layout_v_h.addWidget(setting_name_label)

			text_box = QtWidgets.QLineEdit()
			setting_value = all_settings.get(setting_name)
			text_box.setText(setting_value)
			text_box.returnPressed.connect(create_save_function(text_box, setting_name))
			layout_v_h.addWidget(text_box)
			setting_dict[setting_name] = text_box
			layout_v.addLayout(layout_v_h)

		if setting_dict == {}:
			raise ValueError("There are no settings. This is a bug. Please contact the developers.")

		save_button = QtWidgets.QPushButton(self.translate("Save"))

		def save_all():
			wrong_inputs = []
			setting_value_tuple = tuple(setting_dict.values())

			note_range = setting_value_tuple[0].text()
			try:
				note_str_utils.get_final_list_notes(note_range)
			except (ValueError, TypeError):
				wrong_inputs.append(notes_config.NOTES_SETTING)

			note_intensity = setting_value_tuple[1].text()
			if note_intensity not in notes_config.LEGAL_NOTE_INTENSITIES:
				wrong_inputs.append(notes_config.NOTE_INTENSITY_SETTING)

			try:
				Fraction(setting_value_tuple[2].text())
			except (TypeError, ValueError, ZeroDivisionError):
				wrong_inputs.append(notes_config.NOTE_VALUE_SETTING)

			language = setting_value_tuple[3].text()
			if language not in notes_config.LEGAL_LANGUAGES:
				wrong_inputs.append(notes_config.LANGUAGE_SETTING)
			
			if wrong_inputs != []:
				wrong_inputs = [self.translate(setting_name) for setting_name in wrong_inputs]
				PyQt6_utils.get_msg_box(self.translate("Settings failed to save"), self.translate("The following settings are incorrect or incomplete:") + "\n\n" + '\n'.join(wrong_inputs)  + "\n\n" + self.translate("Correct them and try again."), QtWidgets.QMessageBox.Icon.Warning).exec()
				return
			
			for setting_name in setting_dict:
				text_box = setting_dict[setting_name]
				user_input = text_box.text()
				if setting_name == "language":
					language_path = os.path.join(TRANSLATIONS_FOLDER, user_input)
					if not os.path.isdir(language_path):
						PyQt6_utils.get_msg_box(self.translate("Settings failed to save"), self.translate("Language doesn't exist; Please enter a valid language."), QtWidgets.QMessageBox.Icon.Warning).exec()
						return
				
						
				notes_config.change_setting(setting_name, user_input)

				
			PyQt6_utils.get_msg_box(self.translate("Settings saved"), self.translate("Settings have been successfully saved.")).exec()

		save_button.clicked.connect(save_all)
		layout_v.addWidget(save_button)

		reset_button = QtWidgets.QPushButton(self.translate("Reset settings"))

		def reset_settings():
			config = notes_config.reset_settings()
			for setting_name in setting_dict:
				text_box = setting_dict[setting_name]
				text_box.setText(config[setting_name])
			PyQt6_utils.get_msg_box(self.translate("Settings reset"), self.translate("Settings have been successfully reset.")).exec()

		reset_button.clicked.connect(reset_settings)
		layout_v.addWidget(reset_button)
	
	def setup_play_menu(self):
		h_buttons = self.get_settings_button(),
		v_buttons = self.get_main_menu_button(), self.get_volume_test_button(), self.get_tonal_nback_test_button(), self.get_TDT_button()
		layout_h, layout_v, self.play_menu = self.setup_menu(self.translate("Choose a test"), h_buttons, v_buttons)
	
	def setup_debug_menu(self):
		v_buttons = ()
		h_buttons = ()
		layout_h, layout_v, self.debug_menu = self.setup_menu(self.translate("Debug"), h_buttons, v_buttons)

	def setup_tonal_nback_test_menu(self):
		self.setup_nback_test_menu(1, TonalNbackTestThread, h_buttons=(self.get_info_button_1(),))

	def setup_visuotonal_nback_menu(self):
		self.setup_nback_test_menu(2, VisuoTonalNbackTestThread)

	def setup_menu(self, title:str="", widgets_h:tuple[QtWidgets.QWidget, ...]=(), widgets_v:tuple[QtWidgets.QWidget, ...]=(), back_button:bool=True):
		frame = QtWidgets.QFrame(self)
		layout_h_v = QtWidgets.QHBoxLayout()
		layout_v_h_v = QtWidgets.QVBoxLayout()
		layout_v = QtWidgets.QVBoxLayout(frame)
		if back_button:
			layout_h_v.addWidget(self.get_back_button())

		for widget in widgets_h:
			layout_h_v.addWidget(widget)
		#layout_h_v.addStretch()
		
		layout_v_h_v.addWidget(PyQt6_utils.create_frame_title(title))
		for widget in widgets_v:
			layout_v_h_v.addWidget(widget)
		#layout_h_v.addStretch()
		#layout_v_h_v.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

		#layout_h_v.addItem(QSpacerItem(300, 20, QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.Minimum))
		layout_h_v.addLayout(layout_v_h_v)
		#layout_h_v.addItem(QSpacerItem(300, 20, QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.Minimum))
		layout_v.addLayout(layout_h_v)
		layout_v.addStretch()
		#frame.setLayout(layout_h_v)
		layout_h_v.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
		return layout_h_v, layout_v_h_v, frame
	
	def get_main_menu_button(self):
		return PyQt6_utils.get_txt_button(self.translate('Main menu'), lambda: self.goto_frame(self.main_menu))

	def get_back_button(self):
		return PyQt6_utils.get_button_with_image(self.back_arrow, self.go_back)

	def get_settings_button(self):
		return PyQt6_utils.get_button_with_image(self.settings_image, lambda: self.goto_frame(self.settings))

	def get_play_button(self):
		return PyQt6_utils.get_button_with_image(self.play_image, lambda: self.goto_frame(self.play_menu))

	def get_debug_button(self):
		def debug():
			self.goto_frame(self.debug_menu)
			
			NbackTestCase.debug() #FIXME: The current debug functionality should probably be removed
		
		return PyQt6_utils.get_button_with_image(self.debug_image, debug)

	def get_exit_button(self):
		return PyQt6_utils.get_txt_button(self.translate('Exit'), self.close)

	def get_stop_button(self, thread:TonalNbackTestThread):
		button = QtWidgets.QPushButton()
		button.setIcon(self.stop_image)
		button.resize(PyQt6_utils.BUTTON_SIZE, PyQt6_utils.BUTTON_SIZE)
		button.setIconSize(button.size())
		def stop():
			thread.stop = True
			button.deleteLater()
			#PyQt6_utils.get_msg_box(self.translate("Test stopped"), self.translate("The test was stopped, just wait for the notes to finish playing before playing another test."), QtWidgets.QMessageBox.Icon.Information).exec()
		button.clicked.connect(stop) 
		return button
	
	def get_info_button_1(self):
		#summon_info_popup = lambda: PyQt6_utils.get_msg_box(self.translate("Help"), info_text, QtWidgets.QMessageBox.Icon.Information).exec()
		info_button = PyQt6_utils.get_button_with_image(self.info_image, lambda:self.goto_frame(self.info_frame1))
		return info_button

	def get_info_button_3(self):
		#summon_info_popup = lambda: PyQt6_utils.get_msg_box(self.translate("Help"), info_text, QtWidgets.QMessageBox.Icon.Information).exec()
		info_button = PyQt6_utils.get_button_with_image(self.info_image, lambda:self.goto_frame(self.info_frame3))
		return info_button

def main():
	app = QtWidgets.QApplication([])
	gui = MyGUI()
	gui.show()
	sys.exit(app.exec())
		
if __name__ == "__main__":
	main()
