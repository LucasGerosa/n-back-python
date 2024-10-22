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
TRANSLATE_CALLABLE = typing.Callable[[str], str]
VALIDATE_CALLABLE = typing.Callable[[str, TRANSLATE_CALLABLE], tuple[bool, str]]
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

	def __init__(self, layout_v: QtWidgets.QVBoxLayout, label:str, default_txt:str = "", validate_func:VALIDATE_CALLABLE=lambda *_: (True, ""), translate:TRANSLATE_CALLABLE = lambda txt:txt):
		self.label = QtWidgets.QLabel(label)
		self.default_txt = default_txt
		self.text_box = QtWidgets.QLineEdit()
		self.reset()
		self.validate_field = lambda:validate_func(self.text_box.text(), translate)
		self.text_box.editingFinished.connect(lambda: self.run_real_time_validation(validate_func, translate))
		layout_v_h = QtWidgets.QHBoxLayout()
		layout_v_h.addWidget(self.label)
		layout_v_h.addWidget(self.text_box)
		layout_v.addLayout(layout_v_h)

	def reset(self):
		self.text_box.setText(self.default_txt)

	def run_real_time_validation(self, validate_func:VALIDATE_CALLABLE, translate:TRANSLATE_CALLABLE) -> None:
		"""Run validation and summon message box if necessary after editing is finished."""
		result, error_message = validate_func(self.text_box.text(), translate)
		if not result:
			self.summon_msgbox(error_message, translate)
		
	@staticmethod
	def summon_msgbox(message_text:str, translate:TRANSLATE_CALLABLE) -> None:
		get_msg_box(translate("Incorrect input"), message_text, QtWidgets.QMessageBox.Icon.Warning).exec()

	@staticmethod
	def is_positive_digit(text:str, translate:TRANSLATE_CALLABLE) -> tuple[bool, str]:
		result, error_message = FormField.is_non_empty(text, translate)
		if not result:
			return False, error_message
		if not (text.isdigit() and int(text) > 0):
			return False, translate('Please enter an integer bigger than 0, not "{}".').format(text)
		return True, ""
	
	@staticmethod
	def is_positive_float_or_fraction(text:str, translate:TRANSLATE_CALLABLE) -> tuple[bool, str]:
		num = general_utils.is_float_or_fraction(text)
		if not num or num <= 0:
			return False, translate('Please enter a fraction or a decimal bigger than 0, not "{}".').format(text)
		return True, ""
	
	@staticmethod
	def is_valid_instrument(text:str, translate:TRANSLATE_CALLABLE) -> tuple[bool, str]:
		if text not in INSTRUMENTS:
			VALID_INSTRUMENTS_STR = ', '.join(INSTRUMENTS)
			return False, translate('Please enter a valid instrument ({VALID_INSTRUMENTS_STR}), not "{text}".').format(VALID_INSTRUMENTS_STR=VALID_INSTRUMENTS_STR, text=text) 
		return True, ""
	
	@staticmethod
	def is_non_empty(text:str, translate:TRANSLATE_CALLABLE) -> tuple[bool, str]:
		if text == "":
			return False, translate("Please enter something.")
		return True, ""


class Forms:
	
	def __init__(self, layout_v: QtWidgets.QVBoxLayout, translate:TRANSLATE_CALLABLE = lambda x:x, fields:list[FormField]|None = None):
		if fields is None:
			fields = []
		self.fields = fields
		self.translate = translate
		self.layout_v = layout_v
	
	def create_field(self, label, default_txt = "", validate_func:VALIDATE_CALLABLE=lambda *_: (True, "")):
		field = FormField(self.layout_v, label, default_txt, validate_func, self.translate)
		self.fields.append(field)
		return field
	
	def validate_fields(self) -> tuple[list, list]:
		incorrect_fields:list[str] = []
		error_messages:list[str] = []
		for field in self.fields:
			result, error_message = field.validate_field()
			if not result:
				incorrect_fields.append(field.label.text())
				error_messages.append(error_message)
			
		return incorrect_fields, error_messages
	
	def summon_incorrect_fields_msgbox(self, incorrect_fields:list[str], error_messages:list[str]) -> None:
		formatted_errors = [f"{field}: {message}" for field, message in zip(incorrect_fields, error_messages)]
		get_msg_box(self.translate("Incorrect input"), self.translate("The following fields are incorrect or incomplete:")+ "\n\n" + '\n'.join(formatted_errors) + "\n\n" + self.translate("Correct them and try again."), QtWidgets.QMessageBox.Icon.Warning).exec()
	
	def create_player_ID_field(self):
		return self.create_field(self.translate("Participant ID"), "123456", FormField.is_positive_digit)
	
	def create_instrument_field(self):
		return self.create_field(self.translate("Instrument (piano or guitar)"), DEFAULT_INSTRUMENT, FormField.is_valid_instrument)
	
	def create_bpm_field(self):
		return self.create_field(self.translate("BPM (beats per minute)"), str(DEFAULT_BPM), FormField.is_positive_float_or_fraction)
	
	def create_number_of_notes_field(self, number_of_notes:str, is_number_of_notes_valid:typing.Callable = FormField.is_positive_digit):
		return self.create_field(self.translate("Number of notes"), number_of_notes, is_number_of_notes_valid)

	def create_number_of_trials_field(self, number_of_trials:str, is_number_of_trials_valid:typing.Callable = FormField.is_positive_digit):
		return self.create_field(self.translate("Number of trials"), number_of_trials, is_number_of_trials_valid)
	
	def summon_reset_button(self):
		reset_button = QtWidgets.QPushButton(self.translate("Reset"))
		self.layout_v.addWidget(reset_button)
		def reset():
			for field in self.fields:
				field.reset()
		reset_button.clicked.connect(reset)

if __name__ == "__main__":
	field = FormField(QtWidgets.QVBoxLayout(), "Test", "1", FormField.is_positive_digit, lambda x: x)
	field.text_box.setText("this should not work")
	print(field.validate_field())
