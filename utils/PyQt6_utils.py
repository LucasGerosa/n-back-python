from PyQt6.QtCore import Qt, QSize, QRegularExpression, QTimer
from PyQt6.QtGui import QFont, QIcon, QPixmap, QGuiApplication, QIntValidator, QDoubleValidator, QRegularExpressionValidator, QPalette, QColor
from PyQt6.QtWidgets import QApplication, QLabel, QMainWindow, QFrame, QPushButton, QVBoxLayout, QHBoxLayout, QWidget, QSpacerItem, QSizePolicy, QLineEdit, QMessageBox
from fractions import Fraction
from collections.abc import Iterable
from PyQt6 import QtCore, QtGui, QtWidgets

FONT = QFont('Arial', 18)
BUTTON_SIZE = 80
#OFFSET_X = 8
#OFFSET_Y = 0

def is_float_or_fraction(value:str):
	try:
		return float(value)

	except ValueError:
		try:
			return float(Fraction(value))
		except ValueError:
			return

def get_center(width=0, height=0):
	x:int = width // 2
	y:int = height // 2
	return x,y

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
