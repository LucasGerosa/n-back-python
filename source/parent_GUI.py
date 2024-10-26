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
		print(f'Could not find translation catalog for language code {language_code}; defaulting to English.')
		return lambda x: x

class grandparent_GUI(QtWidgets.QMainWindow):

	def __init__(self) -> None:
		super().__init__()
		self.primary_screen = QtGui.QGuiApplication.primaryScreen()
		self.setWindowTitle(PROJECT_NAME)
		self.setGeometry(0, 0, 1200, 600)
		self.showMaximized()
		self.states:list = []
		self.translate:TranslateCallable = set_language(notes_config.get_all_settings()["language"])

	def keyPressEvent(self, event):
		if event.key() == QtCore.Qt.Key.Key_F11:
			if self.isFullScreen():
				self.showNormal()
				self.showMaximized()
			else:
				self.showFullScreen()
	
	def goto_frame(self, frame:QtWidgets.QFrame):
		#self.current_frame.hide()
		#frame.show() # Remove the current central widget without deleting it
		#self.removed_widgets.append(removed_widget)
		self.states.append(self.takeCentralWidget())
		self.setCentralWidget(frame)

class parent_GUI(grandparent_GUI):

	def __init__(self) -> None:
		super().__init__()
		self.get_images()
		self.removed_widgets:list = []
		self.test_menus:list = []

	def get_images(self):
		self.back_arrow = QtGui.QIcon("static/back_button.png")
		self.settings_image = QtGui.QIcon("static/settings.png")
		self.info_image = QtGui.QIcon("static/information_button.png")
		self.play_image = QtGui.QIcon("static/play_button.png")
		self.debug_image = QtGui.QIcon("static/debug.png")
		self.stop_image = QtGui.QIcon("static/stop_button.jpg")

	def go_back(self):
		if not self.states == []:
			current_frame = self.states.pop()
			self.removed_widgets.append(self.takeCentralWidget())
			self.setCentralWidget(current_frame)

	def get_back_button(self):
		return PyQt6_utils.get_button_with_image(self.back_arrow, self.go_back)

	def get_settings_button(self):
		return PyQt6_utils.get_button_with_image(self.settings_image, lambda: self.goto_frame(self.settings))
	
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

	# def center_offset_widget(self, width=0, height=0):
	# 	x,y = PyQt6_utils.get_center(width, height)
	# 	window_middle = self.primary_screen.geometry().width() // 2
	# 	return window_middle - x, window_middle - y
	
	# def center_widget_x(self, widget:QtWidgets.QWidget, y:int, width:int, height:int):
	# 	widget.setGeometry(self.center_offset_widget(width=widget.width())[0], y, width, height)

	# def destroy_all_widgets(self):
	# 	for widget in self.children():
	# 		widget.deleteLater()
