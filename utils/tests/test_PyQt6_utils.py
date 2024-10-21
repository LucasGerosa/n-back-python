import sys; import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from PyQt6_utils import FormField, Forms
from PyQt6 import QtWidgets, QtGui, QtCore
import pytest


@pytest.fixture
def forms(qtbot):
	"""Create a FormField with a simple validation function (is_positive_digit)."""
	layout = QtWidgets.QVBoxLayout()
	field = FormField(layout, "Test Field", "1", FormField.is_positive_digit, lambda x: x)
	qtbot.addWidget(field.text_box)  # Add the field to the test bot
	forms = Forms(layout, lambda x: x, [field,])
	return forms

def test_positive_digit_validation(qtbot, forms):
	"""Test real-time validation for positive digits."""
	# Set invalid text and trigger editingFinished event
	field = forms.fields[0]
	field.text_box.setText("invalid")
	#qtbot.keyClick(field.text_box, QtCore.Qt.Key.Key_Enter) 
	result, error_message = field.validate_field()
	assert not result, f"Validation should fail for non-integer input. Got {result} instead. Error message: {error_message}"
	assert forms.check_fields()
	field.text_box.setText("232312")
	result, error_message = field.validate_field()
	assert result, "Validation should pass for valid integer input"
	assert not forms.check_fields()


	# with qtbot.waitSignal(field.text_box.editingFinished):
	# 	field.text_box.editingFinished.emit()t"
