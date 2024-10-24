import sys; import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from PyQt6 import QtWidgets, QtGui, QtCore
import pytest
from PyQt6_utils import FormField, Forms, TRANSLATE_CALLABLE


@pytest.fixture
def forms():
	layout = QtWidgets.QVBoxLayout()
	forms = Forms(layout, lambda x: x)
	forms.create_field("Test Field positive integer", "3", validate_func=FormField.is_positive_digit)
	forms.create_field("Test Field positive float", "3/4", validate_func=FormField.is_positive_float_or_fraction)
	forms.create_field("Test Field not empty", "dawik213 something", validate_func=FormField.is_non_empty)
	forms.create_field("Test Field valid instrument", "piano", validate_func=FormField.is_valid_instrument)
	return forms

def test_positive_digit_validation(qtbot, forms):
	assert not forms.validate_fields()[0], "No fields should be invalid"
	field = forms.fields[0]

	field.text_box.setText("invalid")
	result, error_message = field.validate_field()
	assert not result, f"Validation should fail for non-integer input. Got {result} instead. Error message: {error_message}"
	assert forms.validate_fields()[0] == ["Test Field positive integer"], "Field should be invalid"

	field.text_box.setText("232312")
	result, error_message = field.validate_field()
	assert result, "Validation should pass for valid integer input"
	assert not forms.validate_fields()[0], "No fields should be invalid"

def test_positive_float_or_fraction_validation(qtbot, forms):
	field = forms.fields[1]

	field.text_box.setText("invalid")
	result, error_message = field.validate_field()
	assert not result, f"Validation should fail for non-float input. Got {result} instead. Error message: {error_message}"

	field.text_box.setText("1.2")
	result, error_message = field.validate_field()
	assert result, "Validation should pass for valid float input"
	
	field.text_box.setText("1/2")
	result, error_message = field.validate_field()
	assert result, "Validation should pass for valid fraction input"

def test_non_empty_validation(qtbot, forms):
	field = forms.fields[2]

	field.text_box.setText("")
	result, error_message = field.validate_field()
	assert not result, f"Validation should fail for empty input. Got {result} instead. Error message: {error_message}"

	field.text_box.setText("valid")
	result, error_message = field.validate_field()

def test_valid_instrument_validation(qtbot, forms):
	field = forms.fields[3]

	field.text_box.setText("invalid")
	result, error_message = field.validate_field()
	assert not result, f"Validation should fail for invalid instrument. Got {result} instead. Error message: {error_message}"

	field.text_box.setText("piano")
	result, error_message = field.validate_field()
	assert result, "Validation should pass for valid instrument"

def test_placeHolderText(qtbot, forms):
	field =	forms.create_field("Test placeholder", placeHolderText="Please enter something...", validate_func=FormField.is_non_empty)
	result, error_message = field.validate_field()
	assert not result, f"Validation should fail for empty input. Got {result} instead. Error message: {error_message}. {field.text_box.text()}"

	field.text_box.setText("valid")
	result, error_message = field.validate_field()
	assert result, "Validation should pass for valid input"

@pytest.fixture
def forms2():
	layout = QtWidgets.QVBoxLayout()
	forms = Forms(layout, lambda x: x)
	forms.create_field("Test 1", "1", FormField.is_non_empty, validator=FormField.positive_int_validator)
	forms.create_field("Test 2", "2", FormField.is_non_empty, validator=FormField.positive_int_validator)
	forms.create_field("Test 3. This should be equal to 3.", "3", FormField.is_non_empty, validator=FormField.positive_int_validator)
	return forms

def test_validation_multiple_fields(qtbot, forms2):
	field1 = forms2.fields[0]
	field2 = forms2.fields[1]
	assert not forms2.validate_fields()[0], "No fields should be invalid"
	
	def check_fields_equal_3(_, field1_str, field2_str):
		if int(field1_str) + int(field2_str) == 3:
			return True, ""
		return False, "The sum of the two fields should be equal to 3."

	forms2.add_validation_multiple_fields(check_fields_equal_3, field1, field2)
	assert field1.validate_field()[0], "Field 1 should be valid"
	field2.text_box.setText("100")
	assert forms2.validate_fields()[2], "The multiple validation should be invalid"

