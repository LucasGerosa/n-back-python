from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QFont, QIcon, QPixmap, QGuiApplication
from PyQt6.QtWidgets import QApplication, QLabel, QMainWindow, QFrame, QPushButton, QVBoxLayout, QHBoxLayout, QWidget, QSpacerItem, QSizePolicy, QLineEdit
import sys; import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from utils.defaults import *
import run
from typing import Dict, Optional
from utils import notes_config


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
		self.back_arrow = QIcon("static/back_button.png")#.scaledToWidth(20))
		self.settings_image = QIcon("static/settings.png")#.scaledToWidth(20))
		self.play_image = QIcon("static/play_button.png")

		self.setup_main_menu()
		self.setup_settings()
		self.setup_play_menu()

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
		self.main_menu = QFrame(self)
		h_buttons = (self.get_settings_button(), self.get_play_button())
		self.setup_menu(self.main_menu, "Main menu", h_buttons)

	def setup_settings(self):
		def create_save_function(text_box, setting_name):
			def save_function():
				notes_config.change_setting(setting_name, text_box.text())
			return save_function
		
		self.settings = QFrame(self)
		v_buttons = self.get_main_menu_button(),
		layout_h, layout_v = self.setup_menu(self.settings, "Settings", widgets_v=v_buttons)
		all_settings = notes_config.get_all_settings()
		layout_v_h = QHBoxLayout()
			
		layout_v_h.addWidget(QLabel("Setting Name:"))
		layout_v_h.addWidget(QLabel("Setting value:"))
		layout_v.addLayout(layout_v_h)

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
		save_button.clicked.connect(save_all)
		layout_v.addWidget(save_button)

		reset_button = QPushButton("Reset settings")
		def reset_settings():
			config = notes_config.reset_settings()
			for setting_name in setting_dict:
				text_box = setting_dict[setting_name]
				text_box.setText(config[setting_name])
		reset_button.clicked.connect(reset_settings)
		layout_v.addWidget(reset_button)
	
	def setup_play_menu(self):
		self.play_menu = QFrame(self)
		h_buttons = self.get_settings_button(),
		self.setup_menu(self.play_menu, "Choose a test", h_buttons)
	
	def setup_menu(self, frame:QFrame, title:str, widgets_h:tuple[QWidget, ...]=(), widgets_v:tuple[QWidget, ...]=()):
		layout_h = QHBoxLayout()
		layout_v = QVBoxLayout()
		layout_h.addWidget(self.get_back_button())
		for widget in widgets_h:
			layout_h.addWidget(widget)
		
		layout_v.addWidget(self.create_frame_title(title))
		for widget in widgets_v:
			layout_v.addWidget(widget)

		layout_h.addItem(QSpacerItem(300, 20, QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.Minimum))
		layout_h.addLayout(layout_v)
		#layout_h.addItem(QSpacerItem(300, 20, QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.Minimum))
		frame.setLayout(layout_h)
		return layout_h, layout_v

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

	def get_main_menu_button(self):
		button = QPushButton('Main menu')
		button.setFont(type(self).FONT)
		button_size = button.sizeHint()
		#self.center_widget_x(button, 100, button_size.width(), button_size.height())
		button.clicked.connect(lambda: self.goto_frame(self.main_menu))
		return button

	def get_back_button(self):
		return self.get_button_with_image(self.back_arrow, 0, self.go_back)

	def get_settings_button(self):
		return self.get_button_with_image(self.settings_image, 1, lambda: self.goto_frame(self.settings))
	
	def get_play_button(self):
		return self.get_button_with_image(self.play_image, 2, lambda: self.goto_frame(self.play_menu))
	
	def get_button_with_image(self,icon:QIcon, order:int, command):
		button_size = type(self).button_size
		button = QPushButton()
		button.setIcon(icon)
		#button.setGeometry(button_size * order + type(self).OFFSET_X, type(self).OFFSET_Y, button_size, button_size)
		button.resize(button_size, button_size)
		button.setIconSize(button.size())
		button.clicked.connect(command)
		return button

def main():
	app = QApplication([])
	gui = MyGUI()
	gui.show()
	sys.exit(app.exec())
		
if __name__ == "__main__":
	main()
