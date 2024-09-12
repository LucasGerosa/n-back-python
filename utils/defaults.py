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

#The TONAL_DISCRIMINATION_TASK_SEQUENCES samples are not actually used by the main program. They are used for created randomly ordered sequences that are actually used by the program. Running this file will shuffle the sequences and their corresponding mismatch sequences and print them to the console.
TONAL_DISCRIMINATION_TASK_SEQUENCES4_SAMPLE = [
	["F4", "G4", "A4", "G4"],
	["B4", "A4", "G4", "A4"],
	["D4", "F4", "A4", "G4"],
	["E4", "C4", "D4", "F4"],
	["F4", "E4", "F4", "G4"],

	["B4", "D5", "A4", "G4"],
	["F4", "G4", "F4", "D4"],
	["E4", "C4", "F4", "D4"],
	["D4", "A4", "G4", "F4"],
	["C5", "G4", "A4", "G4"]
]

TONAL_DISCRIMINATION_TASK_SEQUENCES4_MISMATCH_SAMPLE = [
	["F4", "G4", "A4", "G4"],
	["B4", "A4", "G4", "A4"],
	["D4", "F4", "A4", "G4"],
	["E4", "C4", "D4", "F4"],
	["F4", "E4", "F4", "G4"],

	["C5", "D5", "A4", "G4"],
	["E4", "G4", "F4", "D4"],
	["E4", "C4", "E4", "D4"],
	["D4", "A4", "G4", "E4"],
	["B4", "G4", "A4", "G4"]
]

TONAL_DISCRIMINATION_TASK_SEQUENCES6_SAMPLE = [
	["B4", "D5", "A4", "C5", "B4", "G4"], 
	["F4", "E4", "F4", "G4", "A4", "G4"], 
	["D4", "A4", "G4", "E4", "B4", "C5"], 
	["C5", "A4", "B4", "A4", "G4", "E4"], 
	["A4", "D4", "F4", "G4", "F4", "D4"],
 	#these sequences are mirrored in the mismatch sequencess

	["E4", "D4", "A4", "G4", "F4", "E4"], 
	["G4", "A4", "C5", "A4", "G4", "A4"], 
	["D4", "F4", "A4", "G4", "E4", "G4"], 
	["C4", "D4", "E4", "G4", "A4", "C5"], 
	["C5", "D5", "B4", "G4", "A4", "E4"]
]

TONAL_DISCRIMINATION_TASK_SEQUENCES6_MISMATCH_SAMPLE = [
	["B4", "D5", "A4", "C5", "B4", "G4"], 
	["F4", "E4", "F4", "G4", "A4", "G4"], 
	["D4", "A4", "G4", "E4", "B4", "C5"], 
	["C5", "A4", "B4", "A4", "G4", "E4"], 
	["A4", "D4", "F4", "G4", "F4", "D4"],

	["F4", "D4", "A4", "G4", "F4", "E4"], 
	["G4", "A4", "B4", "A4", "G4", "A4"], 
	["D4", "E4", "A4", "G4", "E4", "G4"], 
	["C4", "D4", "F4", "G4", "A4", "C5"], 
	["C5", "D5", "C5", "G4", "A4", "E4"]	
]

TONAL_DISCRIMINATION_TASK_SEQUENCES8_SAMPLE = [
	["F4", "G4", "D4", "E4", "F4", "A4", "G4", "E4"],
	["C4", "D4", "E4", "C4", "F4", "E4", "D4", "C4"],
	["A4", "D5", "A4", "F4", "E4", "G4", "B4", "A4"],
	["G4", "E4", "C5", "A4", "E4", "F4", "A4", "E4"],
	["C4", "F4", "E4", "B4", "A4", "C5", "D5", "A4"],

	["D4", "E4", "G4", "A4", "C5", "A4", "F4", "G4"],
	["B4", "D5", "C5", "B4", "A4", "E4", "B4", "C5"],
	["F4", "G4", "E4", "D4", "C4", "D4", "G4", "E4"],
	["C4", "D4", "E4", "G4", "C5", "B4", "A4", "G4"],
	["E4", "G4", "D4", "C4", "D4", "A4", "G4", "E4"]
]

TONAL_DISCRIMINATION_TASK_SEQUENCES8_MISMATCH_SAMPLE = [
	["F4", "G4", "D4", "E4", "F4", "A4", "G4", "E4"],
	["C4", "D4", "E4", "C4", "F4", "E4", "D4", "C4"],
	["A4", "D5", "A4", "F4", "E4", "G4", "B4", "A4"],
	["G4", "E4", "C5", "A4", "E4", "F4", "A4", "E4"],
	["C4", "F4", "E4", "B4", "A4", "C5", "D5", "A4"],

	["D4", "F4", "G4", "A4", "C5", "A4", "F4", "G4"],
	["B4", "D5", "C5", "B4", "A4", "F4", "B4", "C5"],
	["F4", "G4", "E4", "D4", "C4", "D4", "G4", "F4"],
	["C4", "D4", "F4", "G4", "C5", "B4", "A4", "G4"],
	["F4", "G4", "D4", "C4", "D4", "A4", "G4", "E4"]
]

TONAL_DISCRIMINATION_TASK_SEQUENCES10_SAMPLE = [
	["F4", "G4", "C5", "B4", "A4", "B4", "D5", "C5", "A4", "G4"],
	["D5", "C5", "D5", "B4", "G4", "A4", "C4", "B4", "G4", "A4"],
	["E4", "G4", "A4", "G4", "B4", "D5", "C5", "D5", "B4", "A4"],
	["C5", "G4", "A4", "B4", "A4", "C5", "D5", "B4", "A4", "G4"],
	["D4", "E4", "F4", "A4", "G4", "E4", "B4", "D5", "B4", "C5"],

	["B4", "D5", "C5", "B4", "A4", "C5", "A4", "G4", "A4", "E4"],
	["C4", "E4", "D4", "F4", "A4", "G4", "B4", "D5", "C5", "B4"],
	["A4", "B4", "D5", "C5", "A4", "G4", "B4", "A4", "D5", "C5"],
	["D4", "F4", "A4", "B4", "A4", "B4", "D5", "C5", "G4", "A4"],
	["C4", "D4", "E4", "G4", "A4", "G4", "C5", "D5", "A4", "G4"]
]

TONAL_DISCRIMINATION_TASK_SEQUENCES10_MISMATCH_SAMPLE = [
	["F4", "G4", "C5", "B4", "A4", "B4", "D5", "C5", "A4", "G4"],
	["D5", "C5", "D5", "B4", "G4", "A4", "C4", "B4", "G4", "A4"],
	["E4", "G4", "A4", "G4", "B4", "D5", "C5", "D5", "B4", "A4"],
	["C5", "G4", "A4", "B4", "A4", "C5", "D5", "B4", "A4", "G4"],
	["D4", "E4", "F4", "A4", "G4", "E4", "B4", "D5", "B4", "C5"],

	["B4", "D5", "C5", "B4", "A4", "B4", "A4", "G4", "A4", "E4"],
	["C4", "E4", "D4", "F4", "A4", "G4", "C5", "D5", "C5", "B4"],
	["A4", "B4", "D5", "C5", "A4", "G4", "B4", "A4", "D5", "B4"],
	["D4", "E4", "A4", "B4", "A4", "B4", "D5", "C5", "G4", "A4"],
	["C4", "D4", "E4", "G4", "A4", "G4", "B4", "D5", "A4", "G4"]
]

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

        
def shuffle_lists(list1, list2):

	import random
	# Ensure both lists are the same length
	if len(list1) != len(list2):
			print("Both lists must have the same length.")
			raise ValueError("Both lists must have the same length.")

	# Create a list of indices
	indices = list(range(len(list1)))

	# Shuffle the indices randomly
	random.shuffle(indices)

	# Shuffle both lists according to the shuffled indices
	shuffled_list1 = [list1[i] for i in indices]
	shuffled_list2 = [list2[i] for i in indices]

	return shuffled_list1, shuffled_list2

def format_list(input_list):
	# Iterate over each sublist
	formatted_string = "[\n"
	for sublist in input_list:
		# Convert each sublist to a string and add new lines
		formatted_string += "\t" + str(sublist) + ",\n"
	formatted_string += "]"
	return formatted_string

if __name__ == '__main__':
	sequences, sequences_m = shuffle_lists(TONAL_DISCRIMINATION_TASK_SEQUENCES4_SAMPLE, TONAL_DISCRIMINATION_TASK_SEQUENCES4_MISMATCH_SAMPLE)
	print(format_list(sequences), format_list(sequences_m), sep='\nxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx\n')
	print("\n\n----------------------------------------\n\n")
	sequences, sequences_m = shuffle_lists(TONAL_DISCRIMINATION_TASK_SEQUENCES6_SAMPLE, TONAL_DISCRIMINATION_TASK_SEQUENCES6_MISMATCH_SAMPLE)
	print(format_list(sequences), format_list(sequences_m), sep='\nxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx\n')
	print("\n\n----------------------------------------\n\n")
	sequences, sequences_m = shuffle_lists(TONAL_DISCRIMINATION_TASK_SEQUENCES8_SAMPLE, TONAL_DISCRIMINATION_TASK_SEQUENCES8_MISMATCH_SAMPLE)
	print(format_list(sequences), format_list(sequences_m), sep='\nxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx\n')
	print("\n\n----------------------------------------\n\n")
      
	sequences, sequences_m = shuffle_lists(TONAL_DISCRIMINATION_TASK_SEQUENCES10_SAMPLE, TONAL_DISCRIMINATION_TASK_SEQUENCES10_MISMATCH_SAMPLE)	
	print(format_list(sequences), format_list(sequences_m), sep='\nxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx\n')