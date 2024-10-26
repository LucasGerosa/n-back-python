from PyQt6 import QtGui, QtCore
import sys, os, typing
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from utils import general_utils


EMPTY_ERROR_MSG = "Please enter something."

TranslateCallable = typing.Callable[[str], str]
IsValidErrorMessage = tuple[bool, str]
SimpleValidateCallable = typing.Callable[[TranslateCallable, str], IsValidErrorMessage]

class FractionValidator(QtGui.QDoubleValidator):
	def __init__(self, bottom:float, top:float, decimals:int, translate:TranslateCallable = lambda x:x, parent=None):
		super().__init__(bottom, top, decimals, parent)
		self.translate = translate

	'''Validation for floats and fractions as defined by fractions.Fraction'''
	def validate(self, input_str: str, pos: int) -> tuple[QtGui.QValidator.State, str, int]:
		if " " in input_str:
			return (QtGui.QValidator.State.Invalid, input_str, pos)
		
		if not input_str:
			self.error_message = self.translate(EMPTY_ERROR_MSG)
			return (QtGui.QValidator.State.Intermediate, input_str, pos)
		
		if input_str == '-' and self.bottom() < 0:
			self.error_message = self.translate("Please enter a number.")
			return (QtGui.QValidator.State.Intermediate, input_str, pos)
		# Allow intermediate fractions like "3/"
		if '/' in input_str:
			try:
				numerator, denominator = input_str.split('/')
				if numerator.isdigit() and denominator == "":
					self.error_message = self.translate("Please enter a valid fraction.")
					return (QtGui.QValidator.State.Intermediate, input_str, pos)
				if numerator.isdigit() and denominator.isdigit() and int(denominator) != 0:
					if int(numerator) / int(denominator) > self.bottom():
						return (QtGui.QValidator.State.Acceptable, input_str, pos)
			except ValueError:
				return (QtGui.QValidator.State.Invalid, input_str, pos)
		
		# Validate as a float and ensure it adheres to range and decimal restrictions
		fraction_float = general_utils.is_float_or_fraction(input_str)
		if fraction_float is not None:
			if fraction_float >= self.bottom() and fraction_float <= self.top():
				# Ensure valid number of decimals
				if '.' in input_str:
					decimal_part = input_str.split('.')[1]
					if len(decimal_part) > self.decimals():
						return (QtGui.QValidator.State.Invalid, input_str, pos)
				return (QtGui.QValidator.State.Acceptable, input_str, pos)
		return (QtGui.QValidator.State.Invalid, input_str, pos)

class StrictIntValidator(QtGui.QIntValidator):
	def __init__(self, bottom:int, top:int, translate:TranslateCallable = lambda x:x, parent=None):
		super().__init__(bottom, top, parent)
		self.translate = translate
	
	def validate(self, input_str: str, pos: int) -> tuple[QtGui.QValidator.State, str, int]:
		# Allow intermediate empty state
		if not input_str:
			self.error_message = self.translate(EMPTY_ERROR_MSG)
			return (QtGui.QValidator.State.Intermediate, input_str, pos)
		
		# Check if the input is a valid integer
		if input_str.isdigit():
			value = int(input_str)
			# Ensure the value is within bounds
			if not (value < self.bottom() or value > self.top()):
				return (QtGui.QValidator.State.Acceptable, input_str, pos)
		# If input is neither empty nor a valid integer, return Invalid
		return (QtGui.QValidator.State.Invalid, input_str, pos)
	
class MultipleOptionsValidator(QtGui.QValidator):
	def __init__(self, option_name:str, valid_options, translate:TranslateCallable = lambda x:x, parent=None):
		super().__init__(parent)
		self.valid_options = valid_options
		self.translate = translate
		self.option_name = option_name

	def validate(self, input_str: str, pos: int) -> tuple[QtGui.QValidator.State, str, int]:
		if not input_str:
			self.error_message = EMPTY_ERROR_MSG
			return (QtGui.QValidator.State.Intermediate, input_str, pos)
		
		if input_str in self.valid_options:
			return (QtGui.QValidator.State.Acceptable, input_str, pos)
		
		for option in self.valid_options:
			if input_str in option:
				self.error_message = self.translate("Please enter a valid {} {}.").format(self.option_name, self.valid_options)
				return (QtGui.QValidator.State.Intermediate, input_str, pos)
		
		return (QtGui.QValidator.State.Invalid, input_str, pos)

class RegularExpressionValidator(QtGui.QRegularExpressionValidator):
	def __init__(self, pattern:str, translate:TranslateCallable = lambda x:x, parent=None):
		super().__init__(QtCore.QRegularExpression(pattern), parent)
		self.translate = translate