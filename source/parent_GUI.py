from PyQt6 import QtCore, QtWidgets, QtGui
from utils.defaults import *
from utils import PyQt6_utils, notes_config
import gettext


def set_language(language_code):

	try:
		translation = gettext.translation('app', TRANSLATIONS_FOLDER, languages=[language_code])
		return translation.gettext

	except FileNotFoundError:
		# TODO: Fallback to default English language if the translation catalog is not found
		raise FileNotFoundError(f'Could not find translation catalog for language code {language_code}')

class parent_GUI(QtWidgets.QMainWindow):

	def __init__(self):
		super().__init__()
		self.removed_widgets = []
		self.primary_screen = QtGui.QGuiApplication.primaryScreen()
		self.setWindowTitle(PROJECT_NAME)
		self.setGeometry(0, 0, 1200, 600)
		self.showMaximized()
		self.states = []
		self.translate = set_language(notes_config.get_all_settings()["language"])

	def keyPressEvent(self, event):
		if event.key() == QtCore.Qt.Key.Key_F11:
			if self.isFullScreen():
				self.showNormal()
				self.showMaximized()
			else:
				self.showFullScreen()
	
	def go_back(self):
		if not self.states == []:
			current_frame = self.states.pop()
			self.removed_widgets.append(self.takeCentralWidget())
			self.setCentralWidget(current_frame)

	def goto_frame(self, frame:QtWidgets.QFrame):
		#self.current_frame.hide()
		#frame.show() # Remove the current central widget without deleting it
		#self.removed_widgets.append(removed_widget)
		self.states.append(self.takeCentralWidget())
		self.setCentralWidget(frame)

	# def center_offset_widget(self, width=0, height=0):
	# 	x,y = PyQt6_utils.get_center(width, height)
	# 	window_middle = self.primary_screen.geometry().width() // 2
	# 	return window_middle - x, window_middle - y
	
	# def center_widget_x(self, widget:QtWidgets.QWidget, y:int, width:int, height:int):
	# 	widget.setGeometry(self.center_offset_widget(width=widget.width())[0], y, width, height)

	# def destroy_all_widgets(self):
	# 	for widget in self.children():
	# 		widget.deleteLater()
