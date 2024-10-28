from PyQt6 import QtCore, QtWidgets, QtGui
import typing

from source.parent_GUI import parent_GUI
from utils import PyQt6_utils
from source.TestCase import TestCase, TonalDiscriminationTaskTestCase, AnswerType
from source.testThreads import TestThread

class Page(QtWidgets.QFrame):
	
	def __init__(self, parent:parent_GUI, title:str="", widgets_h:tuple[QtWidgets.QWidget, ...]=(), widgets_v:tuple[QtWidgets.QWidget, ...]=()):
		super().__init__(parent)
		self.app = parent
		self.layout_v = QtWidgets.QVBoxLayout(self)
		self.layout_v.setAlignment(QtCore.Qt.AlignmentFlag.AlignTop)

		self.layout_v_h0 = QtWidgets.QHBoxLayout()
		self.layout_v.addLayout(self.layout_v_h0)
		self.layout_v_h0.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeft)
		for widget in widgets_h:
			self.layout_v_h0.addWidget(widget)

		self.layout_v_h1 = QtWidgets.QHBoxLayout()
		self.layout_v.addLayout(self.layout_v_h1)
		if title:
			title = parent.translate(title)
		self.layout_v_h1.addWidget(PyQt6_utils.create_frame_title(title), alignment=QtCore.Qt.AlignmentFlag.AlignCenter)

		self.layout_v_h2 = QtWidgets.QHBoxLayout()
		self.layout_v.addLayout(self.layout_v_h2)

		self.layout_v_h2_v = QtWidgets.QVBoxLayout()
		self.layout_v_h2.addLayout(self.layout_v_h2_v)
		self.layout_v_h2_v.setContentsMargins(50, 20, 50, 0)
		for widget in widgets_v:
			self.layout_v_h2_v.addWidget(widget)
		self.layout_v_h2_v.setAlignment(QtCore.Qt.AlignmentFlag.AlignHCenter)
		#return self.layout_v_h2, self.layout_v_h2_v, frame

	def create_question(self, question_text:str, testCase:TestCase|TonalDiscriminationTaskTestCase) -> None:
			answers, question, layout_v_h, destroy_yes_no = PyQt6_utils.create_question(self.layout_v_h2_v, question_text, self.app.translate("Yes"), self.app.translate("No"))
			yes_button, no_button = answers
			yes_button.setStyleSheet("background-color: green; font-size: 50px;")
			no_button.setStyleSheet("background-color: red; font-size: 50px;")
			
			def yes():
				testCase.validateAnswer(answer=AnswerType.SAME)
				destroy_yes_no()
				self.notes_thread.wait_condition.wakeOne()

			def no():
				testCase.validateAnswer(answer=AnswerType.DIFFERENT)
				destroy_yes_no()
				self.notes_thread.wait_condition.wakeOne()

			yes_button.clicked.connect(yes)
			no_button.clicked.connect(no)

	def countdown(self):
		seconds_remaining = 3
		timer = QtCore.QTimer() #is self.app here necessary?
		label = QtWidgets.QLabel('3') #is self.app here necessary?
		label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
		label.setStyleSheet("font-size: 200px;")
		self.layout_v_h2_v.addWidget(label)

		def update_countdown():
			nonlocal seconds_remaining
			seconds_remaining -= 1
			label.setText(str(seconds_remaining))

			if seconds_remaining == 0:
				timer.stop()
				label.deleteLater()
				self.notes_thread.wait_condition.wakeOne()

		timer.timeout.connect(update_countdown)
		timer.start(1000)

	def ask_continue_test(self):
		self.loading_label.deleteLater()
		answers, question, layout_v_h, destroy_question = PyQt6_utils.create_question(self.layout_v_h2_v, self.app.translate("Ready for the next trial?"), self.app.translate("Yes"))
		yes_button = answers[0]
		yes_button.setStyleSheet("background-color: green; font-size: 50px;")
		def continue_test():
			destroy_question()
			self.countdown()
		yes_button.clicked.connect(continue_test)

PlayTestThreadFunc = typing.Callable[[Page], None]
PostInitFunc = typing.Callable[[None], PlayTestThreadFunc]

class MenuPage(Page):
	
	def __init__(self, parent:parent_GUI, title:str="", widgets_h:tuple[QtWidgets.QWidget, ...]=(), widgets_v:tuple[QtWidgets.QWidget, ...]=()):
		super().__init__(parent, title, widgets_h, widgets_v)
		self.layout_v_h0.addWidget(self.get_back_button())
	
	def get_back_button(self):
	
		def go_back():
			if not self.app.past_pages == []:
				current_frame = self.app.past_pages.pop()
				self.app.stacked_widget.setCurrentWidget(current_frame)
		
		return PyQt6_utils.get_button_with_image(self.app.back_arrow, go_back)

class NonSettingsMenuPage(MenuPage):

	def __init__(self, parent:parent_GUI, title:str="", widgets_h:tuple[QtWidgets.QWidget, ...]=(), widgets_v:tuple[QtWidgets.QWidget, ...]=()):
		super().__init__(parent, title, widgets_h, widgets_v)
		self.layout_v_h0.addWidget(self.get_settings_button())

	def get_settings_button(self):
		return PyQt6_utils.get_button_with_image(self.app.settings_image, lambda: self.app.goto_frame(self.app.settings))
class TestMenuPage(NonSettingsMenuPage):
	
	def __init__(self, parent:parent_GUI, title:str="", widgets_h:tuple[QtWidgets.QWidget, ...]=(), widgets_v:tuple[QtWidgets.QWidget, ...]=()):
		super().__init__(parent, title, widgets_h, widgets_v)
		play_test_thread = self.post_init_func()
		self.play_test_button = QtWidgets.QPushButton(parent.translate("Play") + ' ' + parent.translate(title))
		self.play_test_button.setFont(QtGui.QFont(PyQt6_utils.FONT, PyQt6_utils.STANDARD_FONT_SIZE))
		self.layout_v_h2_v.addWidget(self.play_test_button)

		def play_test():
			test_page = Page(parent)
			parent.stacked_widget.addWidget(test_page)
			parent.stacked_widget.setCurrentWidget(test_page)

			play_test_thread(test_page)

			def create_loading_label():
				test_page.loading_label = parent.get_loading_label()
				test_page.layout_v.addWidget(test_page.loading_label)
			
			@QtCore.pyqtSlot()
			def on_execute_loop_thread_finished():
				test_page.notes_thread.deleteLater()
				parent.stacked_widget.setCurrentWidget(self)
				parent.stacked_widget.removeWidget(test_page)
			
			test_page.notes_thread.pre_start_execution.connect(create_loading_label)
			test_page.notes_thread.finished.connect(on_execute_loop_thread_finished)
			test_page.notes_thread.start()

		self.play_test_button.clicked.connect(play_test)
	
	def post_init_func(self) -> PlayTestThreadFunc:
		def play_test_thread(test_page:Page) -> None:
			pass
		return play_test_thread
	
	def get_stop_button(self, thread:TestThread):
		button = QtWidgets.QPushButton()
		button.setIcon(self.app.stop_image)
		button.resize(PyQt6_utils.BUTTON_SIZE, PyQt6_utils.BUTTON_SIZE)
		button.setSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed)
		button.setIconSize(button.size())
		def stop():
			thread.stop = True
			button.deleteLater()
		button.clicked.connect(stop) 
		return button
	
	def set_info_page(self, title:str, text_body:str, img_path:str, dimensions:tuple[int, int]):
		text_body = self.app.translate(text_body)
		image = QtWidgets.QLabel()
		image.setPixmap(QtGui.QPixmap(img_path).scaled(*dimensions, QtCore.Qt.AspectRatioMode.KeepAspectRatio))
		text_label = QtWidgets.QLabel(text_body)
		self.info_page = NonSettingsMenuPage(self.app, title, widgets_v=(text_label, image))
		self.app.stacked_widget.addWidget(self.info_page)
		info_button = PyQt6_utils.get_button_with_image(self.app.info_image, lambda:self.app.goto_frame(self.info_page))
		self.layout_v_h0.addWidget(info_button)

class NbackTestMenuPage(TestMenuPage): #FIXME: fix VisuoTonalNbackTestMenuPage and put the common code in this parent class
	pass
