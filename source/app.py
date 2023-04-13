from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QFont, QIcon, QPixmap, QGuiApplication
from PyQt6.QtWidgets import QApplication, QLabel, QMainWindow, QFrame, QPushButton, QVBoxLayout, QHBoxLayout, QWidget, QSpacerItem, QSizePolicy, QLineEdit, QMessageBox
import sys; import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from utils.defaults import *
import run
from typing import Dict, Optional, List
from utils import notes_config
from TestCase import TestCase
import asyncio
from collections.abc import Iterable

class MyGUI(QWidget):
	FONT = QFont('Arial', 18)
	button_size = 80
	OFFSET_X = 8
	OFFSET_Y = 0

	def __init__(self):
		super().__init__()
		self.primary_screen =  QGuiApplication.primaryScreen()
		self.setWindowTitle(PROJECT_NAME)
		self.setGeometry(0, 0, 1200, 600)
		self.showMaximized()
		self.back_arrow = QIcon("static/back_button.png")
		self.settings_image = QIcon("static/settings.png")
		self.play_image = QIcon("static/play_button.png")
		self.debug_image = QIcon("static/debug.png")

		self.setup_main_menu()
		self.setup_settings()
		self.setup_play_menu()
		self.setup_debug_menu()
		self.setup_test1_menu()

		self.states = [self.main_menu]
		self.current_frame = self.main_menu
		self.settings.hide()
		self.main_menu.show()
		# configure the main_menu frame to make the center column expandable
		'''
		main_menu_layout = QHBoxLayout(self.main_menu)
		main_menu_layout.addStretch()
		#main_menu_layout.setStretchFactor(main_menu_layout.itemAt(0), 1)
		main_menu_layout.addStretch()'''
	

	def setup_main_menu(self): #TODO: add translations
		h_buttons = (self.get_settings_button(), self.get_play_button())
		layout_h, layout_v, self.main_menu = self.setup_menu("Main menu", h_buttons)

	def setup_settings(self):
		def create_save_function(text_box, setting_name):
			def save_function():
				notes_config.change_setting(setting_name, text_box.text())
			return save_function
		
		h_buttons = self.get_debug_button(),
		v_buttons = self.get_main_menu_button(),
		layout_h, layout_v, self.settings = self.setup_menu("Settings", widgets_h=h_buttons, widgets_v=v_buttons)
		all_settings = notes_config.get_all_settings()
		layout_v_h = QHBoxLayout()
		layout_v.addLayout(layout_v_h)
		layout_v_h.addWidget(QLabel("Setting Name:"))
		layout_v_h.addWidget(QLabel("Setting value:"))

		setting_dict:Dict[str, QLineEdit] = {}

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
		
		save_button = QPushButton("Save")
		
		def save_all():
			for setting_name in setting_dict:
				text_box = setting_dict[setting_name]
				notes_config.change_setting(setting_name, text_box.text())
			self.get_msg_box("Settings saved", "Settings have been successfully saved.").exec()
			
		save_button.clicked.connect(save_all)
		layout_v.addWidget(save_button)

		reset_button = QPushButton("Reset settings")
		def reset_settings():
			config = notes_config.reset_settings()
			for setting_name in setting_dict:
				text_box = setting_dict[setting_name]
				text_box.setText(config[setting_name])
			self.get_msg_box("Settings reset", "Settings have been successfully reset.").exec()
		reset_button.clicked.connect(reset_settings)
		layout_v.addWidget(reset_button)
	
	def setup_play_menu(self):
		h_buttons = self.get_settings_button(),
		v_buttons = self.get_main_menu_button(), self.get_test1_button()
		layout_h, layout_v, self.play_menu = self.setup_menu("Choose a test", h_buttons, v_buttons)
	
	def setup_debug_menu(self):
		v_buttons = ()
		h_buttons = ()
		layout_h, layout_v, self.debug_menu = self.setup_menu("Debug", h_buttons, v_buttons)

	def setup_test1_menu(self):

		h_buttons = (self.get_settings_button(),)

		v_buttons = ()
		layout_h, layout_v, self.test1_menu = self.setup_menu("Test1", h_buttons, v_buttons)
		player_name_q = "Player name"
		test_case_q = "How many test cases?"
		n_back_q = "n-back (int)"
		notes_quantity_q = "How many notes (int)"
		bpm_q = "How many bpm (float)"
		instrument_q = "Instrument (piano or guitar)"
		labels = (player_name_q, test_case_q, n_back_q, notes_quantity_q, bpm_q, instrument_q)
		set_text = ['' for _ in range(len(labels) - 2)] + [str(DEFAULT_BPM), DEFAULT_INSTRUMENT]
		if len(set_text) != len(labels):
			raise Exception(f"len(set_text) ({len(set_text)}) is not equal to len(labels) ({len(labels)})")
		draft_forms_dict = dict(zip(labels, set_text))
		column_labels, column_text_box = self.setup_forms(layout_v, draft_forms_dict)
		def play_test():
			def get_text(q):
				return column_text_box[labels.index(q)].text()
			player_name = get_text(player_name_q)
			test_case = get_text(test_case_q)
			n_back = get_text(n_back_q)
			notes_quantity = get_text(notes_quantity_q)
			bpm = get_text(bpm_q)
			instrument = get_text(instrument_q)
			TestCase.executeLoop(playerName=player_name, test_case_n=int(test_case), nBack=int(n_back), notesQuantity=int(notes_quantity), bpm=float(bpm), instrument=instrument)
		
		play_test_button = self.get_txt_button("Play test 1", play_test)
		layout_v.addWidget(play_test_button)
	
	def setup_forms(self, layout_v: QVBoxLayout, forms_dict:dict):
		column_labels = []
		column_text_box:list[QLineEdit] = []
		forms_dict_keys = tuple(forms_dict.keys())
		for label in forms_dict_keys:
			column_labels.append(QLabel(label))
			text_box = QLineEdit()
			column_text_box.append(text_box)
			text_box.setText(forms_dict[label])
		self.setup_columns(layout_v, column_labels, column_text_box)
		return column_labels, column_text_box

	def setup_columns(self, layout_v: QVBoxLayout, *columns: Iterable[QWidget|QLineEdit]):
		for row in zip(*columns):
			layout_v_h = QHBoxLayout()
			for widget in row:
				layout_v_h.addWidget(widget)
			layout_v.addLayout(layout_v_h)

	def setup_menu(self, title:str, widgets_h:tuple[QWidget, ...]=(), widgets_v:tuple[QWidget, ...]=()):
		frame = QFrame(self)
		layout_h = QHBoxLayout()
		layout_v = QVBoxLayout()
		layout_h.addWidget(self.get_back_button())
		for widget in widgets_h:
			layout_h.addWidget(widget)
		
		layout_v.addWidget(self.create_frame_title(title))
		for widget in widgets_v:
			layout_v.addWidget(widget)
		#layout_v.setAlignment(Qt.AlignmentFlag.AlignCenter)

		layout_h.addItem(QSpacerItem(300, 20, QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.Minimum))
		layout_h.addLayout(layout_v)
		#layout_h.addItem(QSpacerItem(300, 20, QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.Minimum))
		frame.setLayout(layout_h)
		return layout_h, layout_v, frame

	@staticmethod
	def get_center(width=0, height=0):
		x:int = width // 2
		y:int = height // 2
		return x,y

	def center_offset_widget(self, width=0, height=0):
		x,y = type(self).get_center(width, height)
		window_middle = self.primary_screen.geometry().width() // 2
		return window_middle - x, window_middle - y
	
	def center_widget_x(self, widget:QWidget, y:int, width:int, height:int):
		widget.setGeometry(self.center_offset_widget(width=widget.width())[0], y, width, height)

	def create_frame_title(self, title:str):
		label = QLabel(title)

		label.setFont(type(self).FONT)
		#self.center_widget_x(label, 0, 400, 80)
		return label

	def destroy_all_widgets(self):
		for widget in self.children():
			widget.deleteLater()

	def goto_frame(self, frame:QFrame):
		self.current_frame.hide()
		frame.show()
		self.states.append(self.current_frame)
		self.current_frame = frame
	
	def go_back(self):
		if not self.states == []:
			self.current_frame.hide()
			self.current_frame = self.states.pop()
			self.current_frame.show()

	def get_test1_button(self):
		return self.get_txt_button('Test 1', lambda: self.goto_frame(self.test1_menu)) #TODO

	def get_main_menu_button(self):
		return self.get_txt_button('Main menu', lambda: self.goto_frame(self.main_menu))

	def get_txt_button(self, txt, command):
		button = QPushButton(txt)
		button.setFont(type(self).FONT)
		button_size = button.sizeHint()
		#self.center_widget_x(button, 100, button_size.width(), button_size.height())
		button.clicked.connect(command)
		return button

	def get_back_button(self):
		return self.get_button_with_image(self.back_arrow, self.go_back)

	def get_settings_button(self):
		return self.get_button_with_image(self.settings_image, lambda: self.goto_frame(self.settings))
	
	def get_play_button(self):
		return self.get_button_with_image(self.play_image, lambda: self.goto_frame(self.play_menu))
	
	def get_debug_button(self):
		def debug():
			self.goto_frame(self.debug_menu)
			TestCase.debug()
		
		return self.get_button_with_image(self.debug_image, debug)
	
	def get_button_with_image(self,icon:QIcon, command):
		button_size = type(self).button_size
		button = QPushButton()
		button.setIcon(icon)
		#button.setGeometry(button_size * order + type(self).OFFSET_X, type(self).OFFSET_Y, button_size, button_size)
		button.resize(button_size, button_size)
		button.setIconSize(button.size())
		button.clicked.connect(command)
		return button
	
	def get_msg_box(self, title, msg):
		msg_box = QMessageBox()

		msg_box.setIcon(QMessageBox.Icon.Information)
		msg_box.setWindowTitle(title)
		msg_box.setText(msg)

		ok_button = msg_box.addButton(QMessageBox.StandardButton.Ok)
		msg_box.setDefaultButton(ok_button)
		return msg_box

def main():
	app = QApplication([])
	gui = MyGUI()
	gui.show()
	sys.exit(app.exec())
		
if __name__ == "__main__":
	main()
