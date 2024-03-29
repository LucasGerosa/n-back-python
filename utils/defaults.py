INSTRUMENTS = ('piano', 'guitar')
DEFAULT_INSTRUMENT = 'piano'
DEFAULT_BPM = 60.0
DEFAULT_NOTE_VALUE = 1/4
PROJECT_NAME = "nback"
TRANSLATIONS_FOLDER = 'translations'
RANDOM_MODE = 'random'
RANDOM_C_MAJOR_MODE = 'random_c_major'
TONAL_C_MAJOR_MODE = 'tonal_c_major'
TONAL_C_MAJOR_DEFAULT_SEQUENCES = ["G4", "F4", "E4", "E4", "D4", "E4", "F4", "G4", "C5", "C5"]
TONAL_DISCRIMINATION_TASK_SEQUENCES = [ #The sequences of notes to be played in the tonal discrimination task
	["C4", "B4", "D4"],
	["C4", "E4", "E4"]
]

TONAL_DISCRIMINATION_TASK_SEQUENCES_MISMATCH = [ #The sequences of notes to be played after the sequence in TONAL_DISCRIMINATION_TASK_SEQUENCE (corresponding to the same index)
	["C4", "C4", "D4"],
	["D4", "E4", "E4"]
]


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