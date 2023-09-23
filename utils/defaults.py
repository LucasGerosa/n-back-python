INSTRUMENTS = ('piano', 'guitar')
DEFAULT_INSTRUMENT = 'piano'
DEFAULT_BPM = 60.0
DEFAULT_NOTE_VALUE = 1/4
PROJECT_NAME = "nback"
TRANSLATIONS_FOLDER = 'translations'
RANDOM_MODE = 'random'
C_MAJOR_MODE = 'c_major'

class user_input_messages:
    yes = 'y'
    no = 'n'
    yes_or_no = yes + '/' + no
    KeyboardInterrupt_message = '\nCtrl+c pressed. Canceling '
    @staticmethod
    def print_invalid_input():
        print('That is not a valid input. Try again.')

def set_language(language_code):

	try:
		translation = gettext.translation('app', TRANSLATIONS_FOLDER, languages=[language_code])
	except FileNotFoundError:
		# Fallback to default English language if the translation catalog is not found
		raise FileNotFoundError(f'Could not find translation catalog for language code {language_code}')

	#translation.install()
	global _
	_ = translation.gettext