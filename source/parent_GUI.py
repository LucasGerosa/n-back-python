from PyQt6 import QtCore, QtWidgets, QtGui
from utils.defaults import *
from utils import PyQt6_utils, notes_config
from utils.validators import TranslateCallable
import gettext


def set_language(language_code):

	try:
		translation = gettext.translation('app', TRANSLATIONS_FOLDER, languages=[language_code])
		return translation.gettext

	except FileNotFoundError:
		return f'Could not find translation catalog for language code {language_code}; defaulting to English.'

class grandparent_GUI(QtWidgets.QMainWindow):
	'''Most basic PyQt6 window with the most essential functionality that would be used in almost any application..'''
	def __init__(self) -> None:
		super().__init__()
		self.primary_screen = QtGui.QGuiApplication.primaryScreen()
		self.setWindowTitle(PROJECT_NAME)
		self.setGeometry(0, 0, 1200, 600)
		
		self.stacked_widget = QtWidgets.QStackedWidget()
		self.setCentralWidget(self.stacked_widget)
		self.past_pages:list[QtWidgets.QWidget] = []
		
		translate:TranslateCallable|str = set_language(notes_config.get_all_settings()["language"])
		if type(translate) == str:
			PyQt6_utils.get_msg_box(translate, QtWidgets.QMessageBox.Icon.Warning)
			self.translate = lambda x: x
		else:
			self.translate:TranslateCallable = translate #type: ignore

	def keyPressEvent(self, event):
		if event.key() == QtCore.Qt.Key.Key_F11:
			if self.isFullScreen():
				self.showNormal()
				self.showMaximized()
			else:
				self.showFullScreen()
	
	def goto_frame(self, frame:QtWidgets.QFrame):
		self.past_pages.append(self.stacked_widget.currentWidget())
		self.stacked_widget.setCurrentWidget(frame)

class parent_GUI(grandparent_GUI):
	'''Contains more specific functionality for the basic GUI used by this program.'''

	def __init__(self) -> None:
		super().__init__()
		self.get_images()
		self.removed_widgets:list = []

	def get_images(self):
		self.back_arrow = QtGui.QIcon("static/back_button.png") #REMOVE later
		self.settings_image = QtGui.QIcon("static/settings.png")
		self.info_image = QtGui.QIcon("static/information_button.png")
		self.play_image = QtGui.QIcon("static/play_button.png")
		self.debug_image = QtGui.QIcon("static/debug.png")
		self.stop_image = QtGui.QIcon("static/stop_button.jpg")

	def get_loading_label(self):
		loadingLabel = QtWidgets.QLabel(self.translate("Loading")+ '...')
		loadingLabel.setStyleSheet("font-size: 50px;")
		loadingLabel.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
		return loadingLabel
	


	# def center_offset_widget(self, width=0, height=0):
	# 	x,y = PyQt6_utils.get_center(width, height)
	# 	window_middle = self.primary_screen.geometry().width() // 2
	# 	return window_middle - x, window_middle - y
	
	# def center_widget_x(self, widget:QtWidgets.QWidget, y:int, width:int, height:int):
	# 	widget.setGeometry(self.center_offset_widget(width=widget.width())[0], y, width, height)

	# def destroy_all_widgets(self):
	# 	for widget in self.children():
	# 		widget.deleteLater()
