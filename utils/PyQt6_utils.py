'''Contains utilities for the GUI. Basically shortcuts for creating widgets and layouts for not having to repeat code in the source files.'''

from PyQt6.QtCore import Qt, QSize, QRegularExpression, QTimer
from PyQt6.QtGui import QFont, QIcon, QPixmap, QGuiApplication, QIntValidator, QDoubleValidator, QRegularExpressionValidator, QPalette, QColor
from PyQt6.QtWidgets import QApplication, QLabel, QMainWindow, QFrame, QPushButton, QVBoxLayout, QHBoxLayout, QWidget, QSpacerItem, QSizePolicy, QLineEdit, QMessageBox
from collections.abc import Iterable
from PyQt6 import QtCore, QtGui, QtWidgets
import typing
import sys; import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from utils.defaults import *
from utils import general_utils

FONT = QFont('Arial', 18)
BUTTON_SIZE = 80
#OFFSET_X = 8
#OFFSET_Y = 0


# def get_center(width=0, height=0):
# 	x:int = width // 2
# 	y:int = height // 2
# 	return x, y

def get_txt_button(txt, command):
	button = QPushButton(txt)
	button.setFont(FONT)
	button_size = button.sizeHint()
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

def setup_forms(layout_v: QVBoxLayout, forms_dict:dict):
	column_labels:list[QLabel] = []
	column_text_box:list[QLineEdit] = []
	forms_dict_keys = tuple(forms_dict.keys())
	for label in forms_dict_keys:
		column_labels.append(QLabel(label))
		text_box = QLineEdit()
		column_text_box.append(text_box)
		text_box.setText(forms_dict[label])
	setup_columns(layout_v, column_labels, column_text_box)
	return column_labels, column_text_box

def setup_columns(layout_v: QVBoxLayout, *columns: Iterable[QWidget|QLineEdit]):
	for row in zip(*columns):
		layout_v_h = QHBoxLayout()
		for widget in row:
			layout_v_h.addWidget(widget)
		layout_v.addLayout(layout_v_h)

def get_button_with_image(icon:QIcon, command):
	button = QPushButton()
	button.setIcon(icon)
	#button.setGeometry(button_size * order + type(self).OFFSET_X, type(self).OFFSET_Y, button_size, button_size)
	button.resize(BUTTON_SIZE, BUTTON_SIZE)
	button.setIconSize(button.size())
	button.clicked.connect(command)
	return button

def create_frame_title(title:str):
	label = QLabel(title)

	label.setFont(FONT)
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

class FormField:

	def __init__(self, layout_v: QtWidgets.QVBoxLayout, label:str, default_txt:str, validate_func:typing.Callable, translate:typing.Callable):
		self.label = QtWidgets.QLabel(label)
		self.default_txt = default_txt
		self.text_box = QtWidgets.QLineEdit()
		self.reset()
		self.validate_field = lambda:validate_func(self.text_box.text())
		self.text_box.editingFinished.connect(lambda: self.run_real_time_validation(validate_func, translate))
		layout_v_h = QtWidgets.QHBoxLayout()
		layout_v_h.addWidget(self.label)
		layout_v_h.addWidget(self.text_box)
		layout_v.addLayout(layout_v_h)

	def reset(self):
		self.text_box.setText(self.default_txt)

	def run_real_time_validation(self, validate_func: typing.Callable, translate: typing.Callable):
		"""Run validation and summon message box if necessary after editing is finished."""
		result, error_message = validate_func(self.text_box.text())
		if not result:
			self.summon_msgbox(translate, error_message)
		
	@staticmethod
	def summon_msgbox(translate:typing.Callable, message_text:str) -> None:
		get_msg_box(translate("Incorrect input"), translate(message_text), QtWidgets.QMessageBox.Icon.Warning).exec()

	@staticmethod
	def is_positive_digit(text: str) -> tuple[bool, str]:
		if not (text.isdigit() and int(text) > 0):
			return False, f'Please enter an integer bigger than 0, not {text}'
		return True, ""
	
	@staticmethod
	def is_positive_float_or_fraction(text: str) -> tuple[bool, str]:
		if not general_utils.is_float_or_fraction(text) or float(text) <= 0:
			return False, f'Please enter a fraction or a decimal bigger than 0, not {text}'
		return True, ""
	
	@staticmethod
	def is_valid_instrument(text: str) -> tuple[bool, str]:
		if text not in INSTRUMENTS:
			return False, f'Please enter a valid instrument, not {text}'
		return True, ""
	
	@staticmethod
	def is_non_empty(text: str) -> tuple[bool, str]:
		if text == "":
			return False, "Please enter something."
		return True, ""

class Forms:
	
	def __init__(self, fields:tuple[FormField], layout_v: QtWidgets.QVBoxLayout, translate:typing.Callable):
		
		self.fields = fields
		self.translate = translate
		reset_button = QtWidgets.QPushButton(translate("Reset"))
		layout_v.addWidget(reset_button)
		def reset():
			for field in fields:
				field.reset()
		reset_button.clicked.connect(reset)
	
	def check_fields(self) -> list:
		incorrect_fields:list[str] = []
		for field in self.fields:
			if not field.validate_field()[0]:
				incorrect_fields.append(field.label.text())
			
		return incorrect_fields
	
	def summon_incorrect_fields_msgbox(self, incorrect_fields:list[str]) -> None:
		get_msg_box(self.translate("Incorrect input"), self.translate("The following fields are incorrect or incomplete:\n\n")+ '\n'.join(incorrect_fields)+self.translate(".\n\n Correct them and try again"), QtWidgets.QMessageBox.Icon.Warning).exec()

if __name__ == "__main__":
	field = FormField(QtWidgets.QVBoxLayout(), "Test", "1", FormField.is_positive_digit, lambda x: x)
	field.text_box.setText("this should not work")
	print(field.validate_field())
