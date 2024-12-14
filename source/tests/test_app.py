import pytest, sys, os
from PyQt6 import QtWidgets, QtCore
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from app import MyGUI
from PyQt6.sip import isdeleted

@pytest.fixture
def app(qtbot):
	test_app = MyGUI()
	qtbot.addWidget(test_app)
	return test_app

def find_button_in_layout(parent: QtCore.QObject, button_name: str) -> QtWidgets.QPushButton | None:
	"""
	Recursively search for a QtWidgets.QPushButton with a specified name within a QFrame or layout.

	:param parent: The QFrame or layout widget to search within.
	:param button_name: The object name of the button to find.
	:return: The QtWidgets.QPushButton if found, otherwise None.
	"""
	# Check if parent has children (if it's a QFrame or similar container)
	for child in parent.findChildren(QtWidgets.QWidget):
		# Check if child is the button we're looking for
		if isinstance(child, QtWidgets.QPushButton) and  button_name in child.text():
			return child
		if type(child) != QtWidgets.QLayout:
			continue
		# If child has a layout, recursively search within it
		if child.layout():
			found_button = find_button_in_layout(child, button_name)
			if found_button:
				return found_button
	return None

def list_widgets_in_layout(layout):
	widgets = []
	for i in range(layout.count()):
		item = layout.itemAt(i)
		
		# Check if the item is a widget or a layout
		if isinstance(item.widget(), QtWidgets.QWidget):
			widgets.append(item.widget())
		elif isinstance(item.layout(), QtWidgets.QLayout):  # Check for nested layouts
			widgets.extend(list_widgets_in_layout(item.layout()))
			
	return widgets

def get_widgets_in_layout(layout):
	widgets = []
	for i in range(layout.count()):
		widget = layout.itemAt(i).widget()
		if widget is not None:
			widgets.append(widget)
	return widgets

def widget_in_layout(widget, layout):
	for i in range(layout.count()):
		if layout.itemAt(i).widget() is widget:
			return True
	return False


@pytest.mark.tdt
def test_TDT(qtbot, app:MyGUI):
	menu_page = app.tdt_test_menu
	for i in range(1):
		menu_page.play_test_button.click()
		test_page = menu_page.test_page
		assert not test_page.notes_thread.is_waiting
		test_page.yes_button = None
		qtbot.wait(500)
		for trial in range(test_page.number_of_trials):
			qtbot.waitUntil(lambda: test_page.yes_button != None, timeout=10000)
			qtbot.mouseClick(test_page.yes_button, QtCore.Qt.MouseButton.LeftButton)
			qtbot.waitUntil(lambda: test_page.yes_button != None, timeout=10000)
			qtbot.mouseClick(test_page.yes_button, QtCore.Qt.MouseButton.LeftButton)
			print("Run", i, "Trial", trial)
		qtbot.wait(500)		
	

@pytest.mark.nback
def test_tonal_nback_test(qtbot, app:MyGUI):

	menu_page = app.tonal_nback_test_menu_frame
	for i in range(1):
		menu_page.play_test_button.click()
		test_page = menu_page.test_page
		qtbot.wait(500)
		#test_page.yes_button = None
		
		for trial_num in range(test_page.number_of_trials):
			qtbot.waitUntil(lambda: test_page.yes_button != None, timeout=10**6)
			qtbot.mouseClick(test_page.yes_button, QtCore.Qt.MouseButton.LeftButton)
			#qtbot.wait(2000)
			for sequence_num in range(test_page.number_of_sequences):
				qtbot.waitUntil(lambda: test_page.yes_button != None, timeout=10**6)
				qtbot.mouseClick(test_page.yes_button, QtCore.Qt.MouseButton.LeftButton)
				#qtbot.wait(2000)
				qtbot.waitUntil(lambda: test_page.yes_button != None,  timeout=10**6)
				qtbot.mouseClick(test_page.yes_button, QtCore.Qt.MouseButton.LeftButton)
				#qtbot.wait(2000)
				print("run:", i, "trial num:", trial_num, "\nsequence num:", sequence_num)
		qtbot.wait(500)
