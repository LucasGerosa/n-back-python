import pytest, sys, os
from PyQt6 import QtWidgets, QtCore
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from app import MyGUI

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

def test_tonal_nback_test(qtbot, app:MyGUI):
	menu_page = app.tonal_nback_test_menu_frame
	menu_page.play_test_button.click()
	qtbot.wait(500)
	test_page = menu_page.test_page
	assert test_page.number_of_trials == 6
	assert test_page.number_of_sequences == 10

	for trial in range(test_page.number_of_trials):
		qtbot.waitUntil(lambda: test_page.layout_v_h2_v.count() == 1)
		qtbot.mouseClick(test_page.yes_button, QtCore.Qt.MouseButton.LeftButton)
		for sequence in range(test_page.number_of_sequences):
			qtbot.waitUntil(lambda: test_page.layout_v_h2_v.count() == 2)
			qtbot.mouseClick(test_page.yes_button, QtCore.Qt.MouseButton.LeftButton)
			qtbot.wait(10000)
			qtbot.waitUntil(lambda: test_page.layout_v_h2_v.count() == 2)
			qtbot.mouseClick(test_page.yes_button, QtCore.Qt.MouseButton.LeftButton)
			# qtbot.waitSignal(test_page.notes_thread.done_testCase, timeout=5000)
			# qtbot.mouseClick(test_page.yes_button, QtCore.Qt.MouseButton.LeftButton)
			# qtbot.wait(1000)


if __name__ == "__main__":
	app = QtWidgets.QApplication([])
	button = QtWidgets.QPushButton("Button")
	frame = QtWidgets.QFrame()
	layout_v = QtWidgets.QVBoxLayout(frame)
	layout_h_v = QtWidgets.QHBoxLayout()
	layout_v_h_v = QtWidgets.QVBoxLayout()
	layout_v_h_v.addWidget(button)
	layout_h_v.addLayout(layout_v_h_v)
	layout_v.addLayout(layout_h_v)
	print(find_button_in_layout(frame, "Button"))