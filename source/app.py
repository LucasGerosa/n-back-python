# n-back program
#
# Copyright (C) 2024 Lucas Figueireiredo Gerosa
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.
#
# Refer to README.md and LICENSE files for more information.
# Link to the github repository: https://github.com/LucasGerosa/n-back-python
# lucasfgerosa@gmail.com

'''This file is the main file that should be run to run the program. It ties together all the elements of the GUI and calls functions that deal with the tests (in testThreads.py and TestCase.py)'''

import warnings, sys, os
warnings.filterwarnings("ignore", message="Couldn't find ffmpeg or avconv", category=RuntimeWarning)
from PyQt6 import QtWidgets, QtCore, QtGui
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from utils.defaults import *
from utils import PyQt6_utils, forms, notes_config, note_str_utils, validators
from source.testThreads import TonalNbackTestThread, VisuoTonalNbackTestThread, TestThread
from typing import Dict, Optional, List
from fractions import Fraction
from source import TestGUI

	
class MyGUI(TestGUI.VolumeTestGUI, TestGUI.TonalNbackTestGUI, TestGUI.TonalDiscriminationTaskGUI, TestGUI.VisuotonalNbackTestGUI):
	'''Ties in all the tests together and creates the main GUI for the program.'''
	
	def __init__(self):
		super().__init__()

		self.setup_main_menu()
		self.setup_settings()
		self.setup_play_menu()
		#self.setup_debug_menu()

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

	def setup_settings(self) -> None:

		h_buttons = ()#self.get_debug_button(),
		v_buttons = self.get_main_menu_button(),
		layout_h, layout_v, self.settings = self.setup_menu(self.translate("Settings"), widgets_h=h_buttons, widgets_v=v_buttons)

		layout_v_h = QtWidgets.QHBoxLayout()
		layout_v.addLayout(layout_v_h)
		layout_v_h.addWidget(QtWidgets.QLabel(self.translate("Setting Name:")))
		layout_v_h.addWidget(QtWidgets.QLabel(self.translate("Setting value:")))

		form = forms.FormPresets(layout_v, self.translate)
		def create_field(setting:str, validate_func:validators.SimpleValidateCallable=lambda *_: (True, ""), validator:Optional[QtGui.QValidator]=None) -> None:
			field = form.create_field(self.translate(setting).capitalize(), notes_config.get_setting(setting), validate_func, validator=validator)
			field.setting_name = setting #type: ignore
		
		def validate_note_range(translate, note_range:str) -> validators.IsValidErrorMessage:
			if not note_str_utils.get_final_list_notes(note_range): #TODO: not allow notes that don't exist in the input folder
				return False, translate("Invalid note range")
			return True, ""
		
		create_field(notes_config.NOTES_SETTING, validate_note_range, validator=form.get_notes_str_validator())
		create_field(notes_config.NOTE_INTENSITY_SETTING, validator=validators.MultipleOptionsValidator(notes_config.NOTE_INTENSITY_SETTING, VALID_INTENSITIES, self.translate)) #TODO: replace with a dropdown menu
		create_field(notes_config.NOTE_VALUE_SETTING, validator=form.get_FractionValidator(bottom=0.0000000001, top=100))
		create_field(notes_config.LANGUAGE_SETTING, validator=validators.MultipleOptionsValidator(notes_config.LANGUAGE_SETTING, notes_config.LEGAL_LANGUAGES)) #TODO: replace with a dropdown menu

		form.summon_reset_button()

		save_button = QtWidgets.QPushButton(self.translate("Save"))

		def save_all():

			for field in form.fields:
				notes_config.change_setting(field.setting_name, field.text_box.text())
				
			PyQt6_utils.get_msg_box(self.translate("Settings saved"), self.translate("Settings have been successfully saved.")).exec()
		form.summon_validate_all_button(save_button, save_all)
		
		reset_button = QtWidgets.QPushButton(self.translate("Reset to default"))
		def reset_settings():

			config = notes_config.reset_settings()
			for field in form.fields:
				field.text_box.setText(config[field.setting_name])
			PyQt6_utils.get_msg_box(self.translate("Settings reset"), self.translate("Settings have been successfully reset.")).exec()

		reset_button.clicked.connect(reset_settings)
		layout_v.addWidget(reset_button)
	
	def setup_play_menu(self):
		h_buttons = self.get_settings_button(),
		v_buttons = self.get_main_menu_button(), self.get_volume_test_button(), self.get_tonal_nback_test_button(), self.get_TDT_button()
		layout_h, layout_v, self.play_menu = self.setup_menu(self.translate("Choose a test"), h_buttons, v_buttons)
	
	# def setup_debug_menu(self): #The current debug functionality does not work.
	# 	v_buttons = ()
	# 	h_buttons = ()
	# 	layout_h, layout_v, self.debug_menu = self.setup_menu(self.translate("Debug"), h_buttons, v_buttons)
	
	def get_main_menu_button(self):
		return PyQt6_utils.get_txt_button(self.translate('Main menu'), lambda: self.goto_frame(self.main_menu))

	def get_play_button(self):
		return PyQt6_utils.get_button_with_image(self.play_image, lambda: self.goto_frame(self.play_menu))

	# def get_debug_button(self):
	# 	def debug():
	# 		self.goto_frame(self.debug_menu)
			
	# 		NbackTestCase.debug() #FIXME: The current debug functionality should probably be removed
		
	# 	return PyQt6_utils.get_button_with_image(self.debug_image, debug)

	# def get_exit_button(self):
	# 	return PyQt6_utils.get_txt_button(self.translate('Exit'), self.close)

def main():
	app = QtWidgets.QApplication([])
	gui = MyGUI()
	gui.show()
	sys.exit(app.exec())
		
if __name__ == "__main__":
	main()
