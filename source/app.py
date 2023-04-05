import IOUtils
from TestCase import TestCase
import sys; import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from utils.defaults import *
from utils import notes_config
import configparser
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QFont, QIcon, QPixmap, QGuiApplication
from PyQt6.QtWidgets import QApplication, QLabel, QMainWindow, QFrame, QPushButton, QVBoxLayout, QHBoxLayout, QWidget

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
		self.play_image = QIcon("static")

		self.main_menu = QFrame(self)

		#self.setCentralWidget(self.main_menu)

		self.settings = QFrame(self)


		self.get_back_button(self.settings)
		self.get_back_button(self.main_menu)

		self.get_main_menu_button(self.settings)
		self.get_settings_button(self.main_menu)

		self.create_frame_title("Settings", self.settings)
		self.create_frame_title("Main menu", self.main_menu)

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

	def get_back_button(self, frame:QFrame):
		back_button = QPushButton(frame)
		back_button.setIcon(self.back_arrow)
		back_button.setGeometry(type(self).OFFSET_X, type(self).OFFSET_Y, type(self).button_size, type(self).button_size)
		back_button.setIconSize(back_button.size())
		#back_button.setIconSize(QSize(20, 20))
		#back_button.setFixedSize(25, 25)
		back_button.clicked.connect(self.go_back)
		return back_button

	def get_settings_button(self, frame:QFrame):
		button_settings = QPushButton(frame)
		button_settings.setIcon(self.settings_image)
		button_settings.setGeometry(type(self).button_size + type(self).OFFSET_X, type(self).OFFSET_Y, type(self).button_size, type(self).button_size)
		button_settings.setIconSize(button_settings.size())
		#button_settings.setIconSize(QSize(20, 20))
		#button_settings.setFixedSize(50, 50)
		button_settings.clicked.connect(lambda: self.goto_frame(self.settings))
		return button_settings

	def get_main_menu_button(self, frame:QFrame):
		main_menu_button = QPushButton('Main menu', frame)
		main_menu_button.setFont(type(self).FONT)
		button_size = main_menu_button.sizeHint()
		self.center_widget_x(main_menu_button, 100, button_size.width(), button_size.height())
		
		main_menu_button.clicked.connect(lambda: self.goto_frame(self.main_menu))
		return main_menu_button

	def get_play_button(self, frame:QFrame):
		button = QPushButton(frame)
		button.setIcon(self.play_image)

''' def settings(self):
		self.root.destroy() #destroys the window itself
		self.destroy_all_widgets()
		self.get_back_button().pack()
		self.get_main_menu_button().pack()
		notes_setting_label = notes_config.get_setting(notes_config.NOTES_SETTING)

		print("Settings accessed")'''


def retrieveInfo():
		name = input("Player Name:\n")
		while True:
			bpm = input(f"Bpm (default: {DEFAULT_BPM}bpm):\n")
			if bpm == "":
				bpm = DEFAULT_BPM
				break
			elif bpm.isnumeric():
				bpm = float(bpm)
				break
			print('That is not a valid bpm number. Try again.')
		
		while True:
			instrument = input(f"Instrument ({' or '.join(INSTRUMENTS)}; {DEFAULT_INSTRUMENT } is default):\n")
			if instrument == "":
				instrument = 'piano'
				break
			elif instrument in INSTRUMENTS:
				break
			print('That is not a valid instrument; try again.')
		return name, bpm, instrument

def home() -> str:
	return input("1 -> Start\n2 -> Import from file\n0 -> Quit\nsettings -> to change the settings\nsettings_reset -> to reset all settings to default (this might fix some bugs regarding settings\n> ")
	
def settings_prompt():
	try:
		while True:
			setting = input(f"""
What setting do you want to alter? Current values:
{notes_config.NOTES_SETTING} = {notes_config.get_setting(notes_config.NOTES_SETTING)}
{notes_config.NOTE_INTENSITY_SETTING} = {notes_config.get_setting(notes_config.NOTE_INTENSITY_SETTING)}
{notes_config.NOTE_VALUE_SETTING} = {notes_config.get_setting(notes_config.NOTE_VALUE_SETTING)}
""")    
		
			if notes_config.does_setting_exist(setting):
				new_value = input("What value do you want to alter it to?\n")
				notes_config.change_setting(setting, new_value)
				print("Settings saved.")
				break
			print("Setting doesn't exist. Try again.")
	except (KeyError, configparser.ParsingError) as e:
		reset_bool = input(f"{e}\nsettings.ini file is probably corrupted. Reset it to default settings?\n ({user_input_messages.yes_or_no})")
		if reset_bool == user_input_messages.yes:
			notes_config.reset_settings()
			print("All settings have been successfully reset.\n")
		else:
			print('Cancelling operation. Fix your settings.ini file or contact the developers.\n')

def old_main() -> None:
	IOUtils.cls()
	while True:
		option = home()
		if option == "debug":
			TestCase.debug()
			input("Debugging session finished.\nPress ENTER to continue.")
			return
		if option == 'settings':
			settings_prompt()
		
		elif option == 'settings_reset':
			notes_config.reset_settings()
			print("All settings have been successfully reset.")

		elif not option.isnumeric() or not 0 <= int(option) <= 2:
			print(f"The input needs to be a number from 0 to 2. '{option}' was given. Try again.\n\n")
		
		else:

			while True:
				if option == '0':
					return
				info =  retrieveInfo()  
				if option == '2':
					TestCase.executeFromFile(*info)
						
				elif option == '1':
					TestCase.executeLoop(*info)
				
				else:
					raise TypeError(f"The input needs to be a number from 0 to 2. {option} was given.")
				
def main():
	app = QApplication([])
	gui = MyGUI()
	gui.show()
	sys.exit(app.exec())
		
if __name__ == "__main__":
	main()
