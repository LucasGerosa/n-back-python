from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QFont, QIcon, QPixmap, QGuiApplication
from PyQt6.QtWidgets import QApplication, QLabel, QMainWindow, QFrame, QPushButton, QVBoxLayout, QHBoxLayout, QWidget
import sys; import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from utils.defaults import *
import run

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
		self.create_frame_title("Main menu", self.main_menu)
		self.get_back_button(self.main_menu)
		self.get_settings_button(self.main_menu)
		self.get_play_button(self.main_menu)

	def setup_settings(self):
		self.settings = QFrame(self)
		self.create_frame_title("Settings", self.settings)
		self.get_main_menu_button(self.settings)
		self.get_back_button(self.settings)
	
	def setup_play_menu(self):
		self.play_menu = QFrame(self)
		self.create_frame_title("Choose a test", self.play_menu)
		self.get_back_button(self.play_menu)
		self.get_settings_button(self.play_menu)

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

	def create_frame_title(self, title:str, frame:QFrame):
		label = QLabel(title, frame)
		label.setFont(type(self).FONT)
		self.center_widget_x(label, 0, 400, 80)
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

	def get_main_menu_button(self, frame:QFrame):
		button = QPushButton('Main menu', frame)
		button.setFont(type(self).FONT)
		button_size = button.sizeHint()
		self.center_widget_x(button, 100, button_size.width(), button_size.height())
		
		button.clicked.connect(lambda: self.goto_frame(self.main_menu))
		return button

	def get_back_button(self, frame:QFrame):
		return self.get_button_with_image(frame, self.back_arrow, 0, self.go_back)

	def get_settings_button(self, frame:QFrame):
		return self.get_button_with_image(frame, self.settings_image, 1, lambda: self.goto_frame(self.settings))
	
	def get_play_button(self, frame:QFrame):
		return self.get_button_with_image(frame, self.play_image, 2, lambda: self.goto_frame(self.play_menu))
	
	def get_button_with_image(self, frame:QFrame, icon:QIcon, order:int, command):
		button_size = type(self).button_size
		button = QPushButton(frame)
		button.setIcon(icon)
		button.setGeometry(button_size * order + type(self).OFFSET_X, type(self).OFFSET_Y, button_size, button_size)
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
