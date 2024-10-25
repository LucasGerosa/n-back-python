import pytest
from PyQt6 import QtWidgets, QtGui
import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from forms import FormField, MultipleFormValidator, Forms

ILLEGAL_TEXT = "illegal"
ILLEGAL_ERROR_MSG = "This is illegal"

@pytest.fixture
def valid_form_field():
	layout = QtWidgets.QVBoxLayout()
	def dummy_func1(_, str1):
		if str1 == ILLEGAL_TEXT:
			return False, ILLEGAL_ERROR_MSG
		return True, ""

	field1 = FormField(
		layout,
		label="Field 1",
		validate_func=dummy_func1,
		placeHolderText="Enter text",
	)
	field2 = FormField(
		layout,
		label="Field 2",
		validate_func=dummy_func1,
		placeHolderText="Enter text",
	)
	field3 = FormField(
		layout,
		label="Field 3",
		validate_func=dummy_func1,
		placeHolderText="Enter text",
	)
	return (field1, field2, field3)

def test_individual_field_validation(qtbot, valid_form_field):
	"""Test that an invalid FormField displays a red border."""
	# Set invalid text (empty text)
	field1 = valid_form_field[0]
	field1.text_box.setText(ILLEGAL_TEXT)
	field1.run_real_time_validation()

	# Check if the field is red and has the appropriate tooltip
	assert "red" in field1.text_box.styleSheet()
	assert field1.text_box.toolTip() == ILLEGAL_ERROR_MSG

	# Now set a valid text
	field1.text_box.setText("Some text")
	field1.run_real_time_validation()

	# Verify that the red border is removed
	assert "red" not in field1.text_box.styleSheet()
	assert field1.text_box.toolTip() == ""

def test_multiple_field_validation(qtbot, valid_form_field):
	field1, field2, field3 = valid_form_field

	def no_field_empty(field1_str, field2_str):
		if field1_str and field2_str:
			return True, ""
		return False, "Please enter something."

	def both_fields_empty(field1_str, field2_str):
		if field1_str or field2_str:
			return False, "Please enter nothing."
		return True, ""
		
	# Multiple validator that requires both fields to be non-empty
	multiple_validator1 = MultipleFormValidator(no_field_empty, field1, field2)
	multiple_validator2 = MultipleFormValidator(both_fields_empty, field3, field2)
	# Initially set fields with invalid data
	field1.text_box.setText("Valid text")

	multiple_validator1()
	multiple_validator2()
	assert not multiple_validator1.is_valid
	assert multiple_validator2.is_valid
	assert multiple_validator1 in field1.multiple_validate_field_list
	assert multiple_validator1, multiple_validator2 in field2.multiple_validate_field_list
	assert multiple_validator2 in field3.multiple_validate_field_list
	assert "red" in field1.text_box.styleSheet()
	assert "red" in field2.text_box.styleSheet()
	assert "red" not in field3.text_box.styleSheet()
	assert field1.text_box.toolTip() == "Please enter something."
	assert field2.text_box.toolTip() == "Please enter something."


	field2.text_box.setText("Valid text")
	multiple_validator1()
	assert "red" not in field1.text_box.styleSheet()
	assert "red" in field2.text_box.styleSheet()
	assert "red" in field3.text_box.styleSheet()
