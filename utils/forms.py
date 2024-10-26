import typing, sys, os, re
from PyQt6 import QtCore, QtGui, QtWidgets
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from utils.defaults import *
from utils import PyQt6_utils, validators, note_str_utils


NOTE_PATTERN = r"[A-Ga-g][b#]?[0-7]" #TODO:only allow validation of notes that are in the available notes list
SEPARATOR_PATTERN = f"[{''.join(map(re.escape, note_str_utils.DEFAULT_RANGE_SEPARATORS))}]"
SIMPLE_RANGE_OR_SINGLE_PATTERN = rf"({NOTE_PATTERN})({SEPARATOR_PATTERN}({NOTE_PATTERN}))?|({NOTE_PATTERN})"
COMPLEX_PATTERN = rf"({SIMPLE_RANGE_OR_SINGLE_PATTERN})(\s?(;\s?)?({SIMPLE_RANGE_OR_SINGLE_PATTERN}))*"

class FormField:

	def __init__(self, layout_v: QtWidgets.QVBoxLayout, label:str, default_txt:str = "", validate_func:validators.SimpleValidateCallable=lambda *_: (True, ""), translate:validators.TranslateCallable = lambda txt:txt, placeHolderText:str = "", on_returnPressed:typing.Callable=lambda:None, validator:QtGui.QValidator|None=None):
		self.translate = translate
		self.label = QtWidgets.QLabel(label)
		self.text_box = QtWidgets.QLineEdit()
		self.text_box.setPlaceholderText(placeHolderText)
		self.text_box.returnPressed.connect(on_returnPressed)
		if validator:
			self.text_box.setValidator(validator)

		self.validate_field = lambda:validate_func(translate, self.text_box.text())
		self.multiple_validate_field_list:list[MultipleFormValidator] = []
		self.text_box.textChanged.connect(self.run_real_time_validation)
		self.run_real_time_validation()
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
	
	def get_is_validator_acceptable_state(self) -> validators.IsValidErrorMessage:
		validator = self.text_box.validator()
		if validator is None:
			return True, ""
		current_text = self.text_box.text()
		validator_state, _, _ = validator.validate(current_text, len(current_text))
		if validator_state == QtGui.QValidator.State.Acceptable:
			return True, ""
		if hasattr(validator, "error_message"):
			return False, validator.error_message
		return False, self.translate("Invalid field")
		
	def run_real_time_validation(self):
		valid, error_message = self.validate_field()
		if not valid:
			self.is_valid = False
			self.set_border_and_tooltip_red(error_message)
		else:
			self.is_valid = self.get_is_validator_acceptable_state()[0]
			
			if self.is_valid and not self.multiple_validate_field_list:
				self.reset_border_and_tooltip()
				return
		
		for validate_field in self.multiple_validate_field_list:
			validate_field()
	
	@staticmethod
	def is_non_empty(translate:validators.TranslateCallable, text:str) -> validators.IsValidErrorMessage:
		if text == "":
			return False, translate("Please enter something.")
		return True, ""

class MultipleFormValidator:
	'''This is a class for dealing with multiple fields that need validation that depend on the values of ther fields on top of their individual validation. If any of the involved fields are individually invalid, the validation will not be performed.'''

	def __init__(self, validate_field:typing.Callable[[str], validators.IsValidErrorMessage], *fields: FormField):
		self.validate_field = validate_field
		self.fields = fields
		self._is_valid = True
		for field in fields:
			field.multiple_validate_field_list.append(self)
	
	@property
	def is_valid(self):
		return self._is_valid
	
	def __call__(self) -> validators.IsValidErrorMessage:
		for field in self.fields: #This validation only works if all individual fields are valid by themselves.
			if not field.is_valid:
				break
		
		else:
			result, error_message = self.validate_field(*[field.text_box.text() for field in self.fields])
			self._is_valid = result
			
			if not self.is_valid:
				
				for field in self.fields:
					field.set_border_and_tooltip_red(error_message)
				return result, error_message

			for field in self.fields:
				for multipleFormValidator in field.multiple_validate_field_list: #checks if there are any other invalid validators for the field
					if not multipleFormValidator.is_valid:
						break
				else:
					field.reset_border_and_tooltip()
			return True, ""
		
		self._is_valid = True
		for field in self.fields:
			
			if not field.is_valid:
				continue
			
			for multipleFormValidator in field.multiple_validate_field_list: #checks if there are any other invalid validators for the field
				if not multipleFormValidator.is_valid:
					break
			else:
				field.reset_border_and_tooltip()
		return True, ""

class Forms:

	def __init__(self, layout_v: QtWidgets.QVBoxLayout, translate:validators.TranslateCallable = lambda x:x, fields:list[FormField]|None = None):
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

	def create_field(self, label:str, default_txt:str = "", validate_func:validators.SimpleValidateCallable=lambda *_: (True, ""), placeHolderText:str = "", on_returnPressed:typing.Callable=lambda:None, validator:QtGui.QValidator|None=None) -> FormField:
		field = FormField(self.layout_v, label, default_txt, validate_func, self.translate, placeHolderText, on_returnPressed, validator)
		self.fields.append(field)
		return field
	
	def validate_fields(self) -> tuple[list, list, list]:
		incorrect_fields:list[str] = []
		error_messages:list[str] = []
		for field in self.fields:
			if field.is_valid:
				continue
			
			validator_state, error_message = field.get_is_validator_acceptable_state()
			if validator_state:
				_, error_message = field.validate_field()
			
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

	def summon_incorrect_fields_msgbox(self, incorrect_fields:list[str], error_messages:list[str], incorrect_multiple_fields_error_messages:list[str]) -> None:
		formatted_errors = [f"{field}: {message}" for field, message in zip(incorrect_fields, error_messages)]
		msg_str = "\n\n".join((self.translate("The following fields are incorrect or incomplete:"), *formatted_errors, *incorrect_multiple_fields_error_messages, self.translate("Correct them and try again.")))
		PyQt6_utils.get_msg_box(self.translate("Incorrect input"), msg_str, QtWidgets.QMessageBox.Icon.Warning).exec()
	
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
		validator = validators.MultipleOptionsValidator("instrument", VALID_INSTRUMENTS, self.translate)
		return self.create_field(self.translate("Instrument (piano or guitar)"), DEFAULT_INSTRUMENT, FormField.is_non_empty, validator=validator)
	
	def create_bpm_field(self):
		validator = self.get_FractionValidator()
		return self.create_field(self.translate("BPM (beats per minute)"), str(DEFAULT_BPM), FormField.is_non_empty, validator=validator)
	
	def create_number_of_notes_field(self, number_of_notes:str, is_number_of_notes_valid:validators.SimpleValidateCallable = FormField.is_non_empty):
		validator = validators.StrictIntValidator(1, 99999, translate=self.translate)
		return self.create_field(self.translate("Number of notes"), number_of_notes, is_number_of_notes_valid, validator=validator)

	def create_number_of_trials_field(self, number_of_trials:str, is_number_of_trials_valid:validators.SimpleValidateCallable = FormField.is_non_empty):
		validator = validators.StrictIntValidator(1, 99999, translate=self.translate)
		return self.create_field(self.translate("Number of trials"), number_of_trials, is_number_of_trials_valid, validator=validator)
	
	def get_StrictIntValidator(self, bottom:int = 1, top:int = 99999) -> validators.StrictIntValidator:
		return validators.StrictIntValidator(bottom, top, translate=self.translate)
	
	def get_notes_str_validator(self):
		return validators.RegularExpressionValidator(COMPLEX_PATTERN, translate = self.translate)
	
	def get_FractionValidator(self, bottom:float = 1, top:float = 99999, decimals:int = 2) -> validators.FractionValidator:
		return validators.FractionValidator(bottom, top, decimals, translate=self.translate)

if __name__ == '__main__':
	pass