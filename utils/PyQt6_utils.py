'''Contains utilities for the GUI. Basically shortcuts for creating widgets and layouts for not having to repeat code in the source files.'''

from PyQt6 import QtGui, QtCore
from PyQt6.QtWidgets import QLabel, QPushButton, QHBoxLayout, QMessageBox
from PyQt6 import QtWidgets
import sys, os, typing
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from utils.defaults import *


FONT = 'Arial'
STANDARD_FONT_SIZE = 20
BUTTON_SIZE = 80

#OFFSET_X = 8
#OFFSET_Y = 0


# def get_center(width=0, height=0):
# 	x:int = width // 2
# 	y:int = height // 2
# 	return x, y

def get_txt_button(txt:str, command:typing.Callable, font_size:int=STANDARD_FONT_SIZE):
	button = QPushButton(txt)
	button.setFont(QtGui.QFont(FONT, font_size))
	#button_size = button.sizeHint()
	#self.center_widget_x(button, 100, button_size.width(), button_size.height())
	button.clicked.connect(command)
	return button


def get_msg_box(title, msg, icon=QMessageBox.Icon.Information):
	msg_box = QMessageBox()

	msg_box.setIcon(icon)
	msg_box.setWindowTitle(title)
	msg_box.setText(msg)

	ok_button = msg_box.addButton(QMessageBox.StandardButton.Ok)
	msg_box.setDefaultButton(ok_button)
	return msg_box


def get_button_with_image(icon:QtGui.QIcon, command):
	button = QPushButton()
	button.setIcon(icon)
	#button.setGeometry(button_size * order + type(self).OFFSET_X, type(self).OFFSET_Y, button_size, button_size)
	button.resize(BUTTON_SIZE, BUTTON_SIZE)
	button.setIconSize(button.size())
	button.setSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed)
	button.clicked.connect(command)
	return button


def create_frame_title(title:str):
	label = QLabel(title)
	label.setFont(QtGui.QFont(FONT, 30))
	#self.center_widget_x(label, 0, 400, 80)
	return label


def find_child_layout(parent_layout:QtWidgets.QLayout):

	for i in range(parent_layout.count()):
		item = parent_layout.itemAt(i)
		if isinstance(item, QtWidgets.QLayout):
			child_layout = item.layout()
			return child_layout
	# No child layout found
	return None


def create_question(layout, question_str:str, *answer_str):
	if not answer_str:
		raise ValueError("No answers were given")
	question = QLabel(question_str)
	question.setStyleSheet("font-size: 50px;")
	layout.addWidget(question)
	layout_v_h = QHBoxLayout()
	layout.addLayout(layout_v_h)
	answers = []
	for s in answer_str:
		answer = QPushButton(s)
		answer.setStyleSheet("font-size: 50px;")
		layout_v_h.addWidget(answer)
		answers.append(answer)
		
	layout_v_h.setSpacing(300)
	if answers == []:
		raise ValueError("No answers were added")
	
	def destroy_all():
		question.deleteLater()
		for answer in answers:
			answer.deleteLater()
		layout_v_h.deleteLater()

	return answers, question, layout_v_h, destroy_all

class ScalableLabel(QLabel):
	
	def __init__(self):
		super().__init__(None)
		self.setSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Preferred)

	def resizeEvent(self, event):
		super().resizeEvent(event)
		self.update_pixmap()

class TextLabelWithLineSpacing(ScalableLabel):
	def __init__(self, text, font = QtGui.QFont(FONT, 13), line_spacing=1.5):
		super().__init__()

		# Initialize text and document with custom line spacing and word wrap
		self.text = text
		self.line_spacing = line_spacing
		self.document = QtGui.QTextDocument()
		self.document.setPlainText(self.text)
		self.document.setDefaultFont(font)

		# Configure text wrapping
		text_option = QtGui.QTextOption()
		text_option.setWrapMode(QtGui.QTextOption.WrapMode.WordWrap)
		self.document.setDefaultTextOption(text_option)

		# Apply line spacing
		cursor = QtGui.QTextCursor(self.document)
		block_format = QtGui.QTextBlockFormat()
		block_format.setLineHeight(self.line_spacing * 100, QtGui.QTextBlockFormat.LineHeightTypes.ProportionalHeight.value)
		cursor.select(QtGui.QTextCursor.SelectionType.Document)
		cursor.mergeBlockFormat(block_format)

		# Initial render and set dynamic minimum size
		self.update_pixmap()
		self.setMinimumSize(int(self.document.idealWidth()), int(self.document.size().height()))

	def update_pixmap(self):
		"""Render the document as a pixmap with the current width."""
		# Set wrapping width to the current widget width
		self.document.setTextWidth(self.width())

		# Render the QTextDocument into a QLabel's pixmap with dynamic size
		image = QtGui.QImage(self.width(), int(self.document.size().height()), QtGui.QImage.Format.Format_ARGB32)
		image.fill(QtCore.Qt.GlobalColor.transparent)
		
		painter = QtGui.QPainter(image)
		self.document.drawContents(painter)
		painter.end()

		# Set the rendered document as a pixmap on the label
		self.setPixmap(QtGui.QPixmap.fromImage(image))

class ScalableImageLabel(ScalableLabel):
	def __init__(self, image_path):
		super().__init__()
		self.image_path = image_path
		self.pixmap = QtGui.QPixmap(image_path)
		self.update_pixmap()

	def update_pixmap(self):
		scaled_pixmap = self.pixmap.scaled(self.size(), QtCore.Qt.AspectRatioMode.KeepAspectRatio, QtCore.Qt.TransformationMode.SmoothTransformation)
		self.setPixmap(scaled_pixmap)


if __name__ == "__main__":
	pass
