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
from utils import PyQt6_utils
from source.parent_GUI import parent_GUI
from source.app_pages import TonalDiscriminationTaskMenuPage, TonalNbackTestMenuPage, SettingsMenuPage, VolumeTestMenuPage
from source.abstract_pages import NonSettingsMenuPage, MenuPage

	
class MyGUI(parent_GUI):
	'''Ties in all the tests together and creates the main GUI for the program.'''
	
	def __init__(self):
		super().__init__()

		#self.setup_settings()
		self.setup_tests_menu()

		#self.setting_menu = SettingsMenuPage(self)

		self.volume_test_menu = VolumeTestMenuPage(self)
		self.stacked_widget.addWidget(self.volume_test_menu)

		self.tonal_nback_test_menu_frame = TonalNbackTestMenuPage(self)
		self.stacked_widget.addWidget(self.tonal_nback_test_menu_frame)

		self.tdt_test_menu = TonalDiscriminationTaskMenuPage(self)
		self.stacked_widget.addWidget(self.tdt_test_menu)

		self.goto_frame(self.tests_menu)
		self.showMaximized()
	
	def setup_tests_menu(self):
		def get_volume_test_button():
			return PyQt6_utils.get_txt_button(self.translate('Volume test'), lambda: self.goto_frame(self.volume_test_menu))
		
		def get_tonal_nback_test_button():
			return PyQt6_utils.get_txt_button(self.translate('Tonal n-back test'), lambda: self.goto_frame(self.tonal_nback_test_menu_frame))
		
		def get_TDT_button():
			return PyQt6_utils.get_txt_button(self.translate('Tonal discrimination task'), lambda: self.goto_frame(self.tdt_test_menu))

		v_buttons = get_volume_test_button(), get_tonal_nback_test_button(), get_TDT_button()
		self.tests_menu = NonSettingsMenuPage(self, "Choose a test", widgets_v = v_buttons)
		self.stacked_widget.addWidget(self.tests_menu)

	# def get_play_button(self):
	# 	return PyQt6_utils.get_button_with_image(self.play_image, lambda: self.goto_frame(self.tests_menu))

def main():
	app = QtWidgets.QApplication([])
	gui = MyGUI()
	gui.show()
	sys.exit(app.exec())
		
if __name__ == "__main__":
	main()
