VALID_INSTRUMENTS = ('piano', 'guitar') #TODO: make these instruments be translated
DEFAULT_INSTRUMENT = 'piano'
DEFAULT_BPM = 75.0
DEFAULT_NOTE_VALUE = 1/4
DEFAULT_INTENSITY = 'mf'
PROJECT_NAME = "nback"
TRANSLATIONS_FOLDER = 'translations'
DEFAULT_SCALE_ROOT = 'C'
LOWEST_NOTE = 'Bb0'
HIGHEST_NOTE = 'C8'
VALID_INTENSITIES = ('mf', 'ff', 'pp')

#The following sequences have been randomly shuffled from the setup/generate_TDT_sequences.py script.

AVAILABLE_TDT_NOTE_QUANTITIES = (4, 6, 8, 10)
AVAILABLE_NUMBER_OF_TRIALS = 10
TONAL_DISCRIMINATION_TASK_SEQUENCES4 = [ #The sequences of notes to be played in the tonal discrimination task
	['B4', 'D5', 'A4', 'G4'],
	['E4', 'C4', 'F4', 'D4'],
	['D4', 'A4', 'G4', 'F4'],
	['F4', 'G4', 'A4', 'G4'],
	['F4', 'E4', 'F4', 'G4'],
	['F4', 'G4', 'F4', 'D4'],
	['D4', 'F4', 'A4', 'G4'],
	['C5', 'G4', 'A4', 'G4'],
	['B4', 'A4', 'G4', 'A4'],
	['E4', 'C4', 'D4', 'F4'],
]

TONAL_DISCRIMINATION_TASK_SEQUENCES4_MISMATCH = [ #The sequences of notes to be played after the sequence in TONAL_DISCRIMINATION_TASK_SEQUENCE (corresponding to the same index)
	['C5', 'D5', 'A4', 'G4'],
	['E4', 'C4', 'E4', 'D4'],
	['D4', 'A4', 'G4', 'E4'],
	['F4', 'G4', 'A4', 'G4'],
	['F4', 'E4', 'F4', 'G4'],
	['E4', 'G4', 'F4', 'D4'],
	['D4', 'F4', 'A4', 'G4'],
	['B4', 'G4', 'A4', 'G4'],
	['B4', 'A4', 'G4', 'A4'],
	['E4', 'C4', 'D4', 'F4'],
]

TONAL_DISCRIMINATION_TASK_SEQUENCES6 = [
	['C5', 'D5', 'B4', 'G4', 'A4', 'E4'],
	['B4', 'D5', 'A4', 'C5', 'B4', 'G4'],
	['G4', 'A4', 'C5', 'A4', 'G4', 'A4'],
	['D4', 'F4', 'A4', 'G4', 'E4', 'G4'],
	['C4', 'D4', 'E4', 'G4', 'A4', 'C5'],
	['C5', 'A4', 'B4', 'A4', 'G4', 'E4'],
	['F4', 'E4', 'F4', 'G4', 'A4', 'G4'],
	['E4', 'D4', 'A4', 'G4', 'F4', 'E4'],
	['D4', 'A4', 'G4', 'E4', 'B4', 'C5'],
	['A4', 'D4', 'F4', 'G4', 'F4', 'D4'],
]

TONAL_DISCRIMINATION_TASK_SEQUENCES6_MISMATCH = [
	['C5', 'D5', 'C5', 'G4', 'A4', 'E4'],
	['B4', 'D5', 'A4', 'C5', 'B4', 'G4'],
	['G4', 'A4', 'B4', 'A4', 'G4', 'A4'],
	['D4', 'E4', 'A4', 'G4', 'E4', 'G4'],
	['C4', 'D4', 'F4', 'G4', 'A4', 'C5'],
	['C5', 'A4', 'B4', 'A4', 'G4', 'E4'],
	['F4', 'E4', 'F4', 'G4', 'A4', 'G4'],
	['F4', 'D4', 'A4', 'G4', 'F4', 'E4'],
	['D4', 'A4', 'G4', 'E4', 'B4', 'C5'],
	['A4', 'D4', 'F4', 'G4', 'F4', 'D4'],
]

TONAL_DISCRIMINATION_TASK_SEQUENCES8 = [
	['C4', 'F4', 'E4', 'B4', 'A4', 'C5', 'D5', 'A4'],
	['C4', 'D4', 'E4', 'G4', 'C5', 'B4', 'A4', 'G4'],
	['F4', 'G4', 'E4', 'D4', 'C4', 'D4', 'G4', 'E4'],
	['F4', 'G4', 'D4', 'E4', 'F4', 'A4', 'G4', 'E4'],
	['B4', 'D5', 'C5', 'B4', 'A4', 'E4', 'B4', 'C5'],
	['E4', 'G4', 'D4', 'C4', 'D4', 'A4', 'G4', 'E4'],
	['A4', 'D5', 'A4', 'F4', 'E4', 'G4', 'B4', 'A4'],
	['G4', 'E4', 'C5', 'A4', 'E4', 'F4', 'A4', 'E4'],
	['D4', 'E4', 'G4', 'A4', 'C5', 'A4', 'F4', 'G4'],
	['C4', 'D4', 'E4', 'C4', 'F4', 'E4', 'D4', 'C4'],
]

TONAL_DISCRIMINATION_TASK_SEQUENCES8_MISMATCH = [
	['C4', 'F4', 'E4', 'B4', 'A4', 'C5', 'D5', 'A4'],
	['C4', 'D4', 'F4', 'G4', 'C5', 'B4', 'A4', 'G4'],
	['F4', 'G4', 'E4', 'D4', 'C4', 'D4', 'G4', 'F4'],
	['F4', 'G4', 'D4', 'E4', 'F4', 'A4', 'G4', 'E4'],
	['B4', 'D5', 'C5', 'B4', 'A4', 'F4', 'B4', 'C5'],
	['F4', 'G4', 'D4', 'C4', 'D4', 'A4', 'G4', 'E4'],
	['A4', 'D5', 'A4', 'F4', 'E4', 'G4', 'B4', 'A4'],
	['G4', 'E4', 'C5', 'A4', 'E4', 'F4', 'A4', 'E4'],
	['D4', 'F4', 'G4', 'A4', 'C5', 'A4', 'F4', 'G4'],
	['C4', 'D4', 'E4', 'C4', 'F4', 'E4', 'D4', 'C4'],
]

TONAL_DISCRIMINATION_TASK_SEQUENCES10 = [
	['D4', 'E4', 'F4', 'A4', 'G4', 'E4', 'B4', 'D5', 'B4', 'C5'],
	['F4', 'G4', 'C5', 'B4', 'A4', 'B4', 'D5', 'C5', 'A4', 'G4'],
	['D5', 'C5', 'D5', 'B4', 'G4', 'A4', 'C4', 'B4', 'G4', 'A4'],
	['D4', 'F4', 'A4', 'B4', 'A4', 'B4', 'D5', 'C5', 'G4', 'A4'],
	['A4', 'B4', 'D5', 'C5', 'A4', 'G4', 'B4', 'A4', 'D5', 'C5'],
	['E4', 'G4', 'A4', 'G4', 'B4', 'D5', 'C5', 'D5', 'B4', 'A4'],
	['C5', 'G4', 'A4', 'B4', 'A4', 'C5', 'D5', 'B4', 'A4', 'G4'],
	['C4', 'E4', 'D4', 'F4', 'A4', 'G4', 'B4', 'D5', 'C5', 'B4'],
	['C4', 'D4', 'E4', 'G4', 'A4', 'G4', 'C5', 'D5', 'A4', 'G4'],
	['B4', 'D5', 'C5', 'B4', 'A4', 'C5', 'A4', 'G4', 'A4', 'E4'],
]

TONAL_DISCRIMINATION_TASK_SEQUENCES10_MISMATCH = [
	['D4', 'E4', 'F4', 'A4', 'G4', 'E4', 'B4', 'D5', 'B4', 'C5'],
	['F4', 'G4', 'C5', 'B4', 'A4', 'B4', 'D5', 'C5', 'A4', 'G4'],
	['D5', 'C5', 'D5', 'B4', 'G4', 'A4', 'C4', 'B4', 'G4', 'A4'],
	['D4', 'E4', 'A4', 'B4', 'A4', 'B4', 'D5', 'C5', 'G4', 'A4'],
	['A4', 'B4', 'D5', 'C5', 'A4', 'G4', 'B4', 'A4', 'D5', 'B4'],
	['E4', 'G4', 'A4', 'G4', 'B4', 'D5', 'C5', 'D5', 'B4', 'A4'],
	['C5', 'G4', 'A4', 'B4', 'A4', 'C5', 'D5', 'B4', 'A4', 'G4'],
	['C4', 'E4', 'D4', 'F4', 'A4', 'G4', 'C5', 'D5', 'C5', 'B4'],
	['C4', 'D4', 'E4', 'G4', 'A4', 'G4', 'B4', 'D5', 'A4', 'G4'],
	['B4', 'D5', 'C5', 'B4', 'A4', 'B4', 'A4', 'G4', 'A4', 'E4'],
]