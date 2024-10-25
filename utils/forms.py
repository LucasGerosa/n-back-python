import typing, sys, os
from PyQt6 import QtCore, QtGui, QtWidgets
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from utils.defaults import *
from utils import PyQt6_utils, general_utils


TranslateCallable = typing.Callable[[str], str]
IsValidErrorMessage = tuple[bool, str]
SimpleValidateCallable = typing.Callable[[TranslateCallable, str], IsValidErrorMessage]


class FractionValidator(QtGui.QDoubleValidator):
	'''Validation for floats and fractions as defined by fractions.Fraction'''
	def validate(self, input_str: str, pos: int) -> tuple[QtGui.QValidator.State, str, int]:
		if not input_str or (input_str == '-' and self.bottom() < 0):
			return (QtGui.QValidator.State.Intermediate, input_str, pos)
		# Allow intermediate fractions like "3/"
		if '/' in input_str:
			try:
				numerator, denominator = input_str.split('/')
				if numerator.isdigit() and denominator == "":
					return (QtGui.QValidator.State.Intermediate, input_str, pos)
				if numerator.isdigit() and denominator.isdigit() and int(denominator) != 0:
					if int(numerator) / int(denominator) > self.bottom():
						return (QtGui.QValidator.State.Acceptable, input_str, pos)
			except ValueError:
				return (QtGui.QValidator.State.Invalid, input_str, pos)
		
		# Validate as a float and ensure it adheres to range and decimal restrictions
		fraction_float = general_utils.is_float_or_fraction(input_str)
		if fraction_float is not None:
			if fraction_float > self.bottom() and fraction_float <= self.top():
				# Ensure valid number of decimals
				if '.' in input_str:
					decimal_part = input_str.split('.')[1]
					if len(decimal_part) > self.decimals():
						return (QtGui.QValidator.State.Invalid, input_str, pos)
				return (QtGui.QValidator.State.Acceptable, input_str, pos)
			else:
				return (QtGui.QValidator.State.Invalid, input_str, pos)

		return (QtGui.QValidator.State.Invalid, input_str, pos)

class StrictIntValidator(QtGui.QIntValidator):
	def validate(self, input_str: str, pos: int) -> tuple[QtGui.QValidator.State, str, int]:
		# Allow intermediate empty state
		if not input_str:
			return (QtGui.QValidator.State.Intermediate, input_str, pos)
		
		# Check if the input is a valid integer
		if input_str.isdigit():
			value = int(input_str)
			# Ensure the value is within bounds
			if not (value < self.bottom() or value > self.top()):
				return (QtGui.QValidator.State.Acceptable, input_str, pos)
		# If input is neither empty nor a valid integer, return Invalid
		return (QtGui.QValidator.State.Invalid, input_str, pos)


class FormField:

	positive_int_validator = StrictIntValidator(1, 99999)
	positive_fraction_validator = FractionValidator(1, 99999, 2)

	def __init__(self, layout_v: QtWidgets.QVBoxLayout, label:str, default_txt:str = "", validate_func:SimpleValidateCallable=lambda *_: (True, ""), translate:TranslateCallable = lambda txt:txt, placeHolderText:str = "", on_returnPressed:typing.Callable=lambda:None, validator:QtGui.QValidator|None=None):
		self.label = QtWidgets.QLabel(label)
		self.text_box = QtWidgets.QLineEdit()
		self.text_box.setPlaceholderText(placeHolderText)
		self.text_box.returnPressed.connect(on_returnPressed)
		if validator:
			self.text_box.setValidator(validator)
		self.validate_field = lambda:validate_func(translate, self.text_box.text())
		self.multiple_validate_field_list:list[MultipleFormValidator] = []
		self.text_box.textChanged.connect(self.run_real_time_validation)
		self.default_txt = default_txt
		self.reset()

		layout_v_h = QtWidgets.QHBoxLayout()
		layout_v_h.addWidget(self.label)
		layout_v_h.addWidget(self.text_box)
		layout_v.addLayout(layout_v_h)

	
	def reset(self):
		self.text_box.setText(self.default_txt)
		self.run_real_time_validation()

	def reset_border_and_tooltip(self):
		self.text_box.setStyleSheet("border: 1px solid transparent;  border-bottom: 1px solid #aaa;")
		self.text_box.setToolTip("") 
	
	def set_border_and_tooltip_red(self, error_message:str):
		self.text_box.setStyleSheet("border: 1px solid red")
		self.text_box.setToolTip(error_message)

	def run_real_time_validation(self):
		valid, error_message = self.validate_field()

		if not valid:
			self.set_border_and_tooltip_red(error_message)
		else:
			if not self.multiple_validate_field_list:
				self.reset_border_and_tooltip()
				return
		
		for validate_field in self.multiple_validate_field_list:
			validate_field()
	
	@staticmethod
	def is_valid_instrument(translate:TranslateCallable, text:str) -> IsValidErrorMessage:
		if text not in INSTRUMENTS:
			VALID_INSTRUMENTS_STR = ', '.join(INSTRUMENTS)
			return False, translate('Please enter a valid instrument ({VALID_INSTRUMENTS_STR}), not "{text}".').format(VALID_INSTRUMENTS_STR=VALID_INSTRUMENTS_STR, text=text) 
		return True, ""
	
	@staticmethod
	def is_non_empty(translate:TranslateCallable, text:str) -> IsValidErrorMessage:
		if text == "":
			return False, translate("Please enter something.")
		return True, ""

class MultipleFormValidator:
	'''This is a class for dealing with multiple fields that need validation that depend on the values of ther fields on top of their individual validation. If any of the involved fields are individually invalid, the validation will not be performed.'''

	def __init__(self, validate_field:typing.Callable[[str], IsValidErrorMessage], *fields: FormField):
		self.validate_field = validate_field
		self.fields = fields
		self._is_invalid = False
	
	@property
	def is_invalid(self):
		return self._is_invalid
	
	def __call__(self) -> IsValidErrorMessage:
		for field in self.fields: #This validation only works if all individual fields are valid by themselves.
			if not field.validate_field()[0]:
				break
		else:
			result, error_message = self.validate_field(*[field.text_box.text() for field in self.fields])
			self._is_invalid = not result
			
			if self.is_invalid:
				
				for field in self.fields:
					field.set_border_and_tooltip_red(error_message)
				return result, error_message

			for field in self.fields:
				for multipleFormValidator in field.multiple_validate_field_list: #checks if there are any other invalid validators for the field
					if multipleFormValidator.is_invalid:
						break
				else:
					field.reset_border_and_tooltip()
			return True, ""
		
		self._is_invalid = False
		for field in self.fields:
			
			if not field.validate_field()[0]:
				continue
			
			for multipleFormValidator in field.multiple_validate_field_list: #checks if there are any other invalid validators for the field
				if multipleFormValidator.is_invalid:
					break
			else:
				field.reset_border_and_tooltip()
		return True, ""
	

class Forms:

	def __init__(self, layout_v: QtWidgets.QVBoxLayout, translate:TranslateCallable = lambda x:x, fields:list[FormField]|None = None):
		if fields is None:
			fields = []

		self.fields = fields
		self.translate = translate
		self.layout_v = layout_v
		self.multiple_validate_field_list:list[MultipleFormValidator] = []
	
	def summon_validate_all_button(self, validate_all_button:QtWidgets.QPushButton, post_validation_func:typing.Callable = lambda:None) -> None:
		validate_all_button.clicked.connect(lambda: self.post_validate_all(post_validation_func))
		self.layout_v.addWidget(validate_all_button)
	
	def post_validate_all(self, post_validation_func:typing.Callable):
		incorrect_fields, error_messages, incorrect_multiple_fields_error_messages = self.validate_fields()
		if incorrect_fields != [] or incorrect_multiple_fields_error_messages != []:
			self.summon_incorrect_fields_msgbox(incorrect_fields, error_messages, incorrect_multiple_fields_error_messages)
			return
		post_validation_func()

	def create_field(self, label:str, default_txt:str = "", validate_func:SimpleValidateCallable=lambda *_: (True, ""), placeHolderText:str = "", on_returnPressed:typing.Callable=lambda:None, validator:QtGui.QValidator|None=None) -> FormField:
		field = FormField(self.layout_v, label, default_txt, validate_func, self.translate, placeHolderText, on_returnPressed, validator)
		self.fields.append(field)
		return field
	
	def validate_fields(self) -> tuple[list, list, list]:
		incorrect_fields:list[str] = []
		error_messages:list[str] = []
		for field in self.fields:
			result, error_message = field.validate_field()
			if not result:
				incorrect_fields.append(field.label.text())
				error_messages.append(error_message)
		
		incorrect_multiple_fields_error_messages:list[str] = []
		for validate_field in self.multiple_validate_field_list:
			result, error_message = validate_field()
			if not result:
				incorrect_multiple_fields_error_messages.append(error_message)
		return incorrect_fields, error_messages, incorrect_multiple_fields_error_messages
	
	def add_validation_multiple_fields(self, validation_func:typing.Callable, *fields: FormField):
		"""This method will validate multiple fields together in real-time."""
		multipleFormValidator = MultipleFormValidator(lambda *fields:validation_func(self.translate, *fields), *fields)
		self.multiple_validate_field_list.append(multipleFormValidator)

		for field in fields:
			field.multiple_validate_field_list.append(multipleFormValidator)

	def summon_incorrect_fields_msgbox(self, incorrect_fields:list[str], error_messages:list[str], incorrect_multiple_fields_error_messages:list[str]) -> None:
		formatted_errors = [f"{field}: {message}" for field, message in zip(incorrect_fields, error_messages)]
		msg_str = "\n\n".join((self.translate("The following fields are incorrect or incomplete:"), *formatted_errors, *incorrect_multiple_fields_error_messages, self.translate("Correct them and try again.")))
		get_msg_box(self.translate("Incorrect input"), msg_str, QtWidgets.QMessageBox.Icon.Warning).exec()
	
	def summon_reset_button(self):
		reset_button = QtWidgets.QPushButton(self.translate("Reset"))
		self.layout_v.addWidget(reset_button)
		def reset():
			for field in self.fields:
				field.reset()
			for field in self.fields:
				field.run_real_time_validation()
		reset_button.clicked.connect(reset)
	
	def create_player_ID_field(self):
		return self.create_field(self.translate("Participant ID"), "123456", FormField.is_non_empty)
	
	def create_instrument_field(self):
		return self.create_field(self.translate("Instrument (piano or guitar)"), DEFAULT_INSTRUMENT, FormField.is_valid_instrument)
	
	def create_bpm_field(self):
		return self.create_field(self.translate("BPM (beats per minute)"), str(DEFAULT_BPM), FormField.is_non_empty, validator=FormField.positive_fraction_validator)
	
	def create_number_of_notes_field(self, number_of_notes:str, is_number_of_notes_valid:SimpleValidateCallable = FormField.is_non_empty):
		return self.create_field(self.translate("Number of notes"), number_of_notes, is_number_of_notes_valid, validator=FormField.positive_int_validator)

	def create_number_of_trials_field(self, number_of_trials:str, is_number_of_trials_valid:SimpleValidateCallable = FormField.is_non_empty):
		return self.create_field(self.translate("Number of trials"), number_of_trials, is_number_of_trials_valid, validator=FormField.positive_int_validator)