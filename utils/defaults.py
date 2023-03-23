INSTRUMENTS = ('piano', 'guitar')
DEFAULT_INSTRUMENT = 'piano'
DEFAULT_BPM = 60
class user_input_messages:
    yes = 'y'
    no = 'n'
    yes_or_no = yes + '/' + no
    KeyboardInterrupt_message = '\nCtrl+c pressed. Canceling '
    @staticmethod
    def print_invalid_input():
        print('That is not a valid input. Try again.')