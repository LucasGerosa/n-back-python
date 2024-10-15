
def scroll_terminal(lines: int = 15):
    print("\n" * lines)

class user_input_messages:
	YES = 'y'
	NO = 'n'
	YES_or_NO = YES + '/' + NO
	KEYBOARDINTERRUPT_MESSAGE = '\nCtrl+c pressed. Canceling '
	ALL = 'all'
	SETTING = 'setting'
	
	@staticmethod
	def print_invalid_input():
		print('That is not a valid input. Try again.')