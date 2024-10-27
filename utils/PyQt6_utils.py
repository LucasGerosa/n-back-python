'''Contains utilities for the GUI. Basically shortcuts for creating widgets and layouts for not having to repeat code in the source files.'''

from PyQt6.QtGui import QFont, QIcon
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
	button.setFont(QFont(FONT, font_size))
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


def get_button_with_image(icon:QIcon, command):
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
	label.setFont(QFont(FONT, 30))
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


if __name__ == "__main__":
	pass
