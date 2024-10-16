import re
from _collections_abc import Iterable


AVAILABLE_NOTES_TUPLE = (
	'C',
	'Db',
	'D',
	'Eb',
	'E',
	'F',
	'Gb',
	'G',
	'Ab',
	'A',
	'Bb',
	'B'
)

def sort_notes(note_iterable:Iterable[str]) -> list[str]: #sorts an iterable of note names
	if not note_iterable:
		raise ValueError("The iterable is empty.")
	note_name_list = [convert_sharps_to_flats(note_str) for note_str in note_iterable]
	
	def sort_note_key(note_str: str) -> tuple:
		note_name, octave = separate_note_name_octave(note_str)
		return int(octave), AVAILABLE_NOTES_TUPLE.index(note_name)
	
	note_name_list.sort(key=sort_note_key)
	return note_name_list

def separate_note_name_octave(note_full_name:str) -> tuple[str, str]: #Ex. input: "A1" output: ("A", "1")
	NOTE_PATTERN = "([A-Ga-g][b#]*)([0-9]+)"
	match = re.fullmatch(NOTE_PATTERN, note_full_name)
	if not match:
		raise ValueError(f"{note_full_name} is not a valid note name.")
	return match.group(1), match.group(2)

def is_note_greater(note1_full_name:str, note2_full_name:str) -> bool: #Ex. input: "A1", "C2" output: False
	note1_name, note1_octave = separate_note_name_octave(note1_full_name)
	note2_name, note2_octave = separate_note_name_octave(note2_full_name)
	note1_full_name = convert_sharps_to_flats(note1_full_name)
	note2_full_name = convert_sharps_to_flats(note2_full_name)
	if note1_octave == note2_octave:
		return AVAILABLE_NOTES_TUPLE.index(note1_name) > AVAILABLE_NOTES_TUPLE.index(note2_name)

	return note1_octave > note2_octave

def get_greater_note(note1_full_name:str, note2_full_name:str) -> str: #Ex. input: "A1", "C2" output: "C2"
	if is_note_greater(note1_full_name, note2_full_name):
		return note1_full_name
	return note2_full_name

def shift_note_by_semitones(formatted_note_full_name: str, semitones: int) -> str:
	note_name, note_octave = separate_note_name_octave(formatted_note_full_name)
	note_name_index = AVAILABLE_NOTES_TUPLE.index(note_name)
	note_list_len = len(AVAILABLE_NOTES_TUPLE)
	new_note_index = (note_name_index + semitones) % note_list_len
	new_note_octave = int(note_octave) + (note_name_index + semitones) // note_list_len

	return AVAILABLE_NOTES_TUPLE[new_note_index] + str(new_note_octave)

def get_list_notes_able_up_down_semitones(available_notes_str_list:list[str], semitones:int) -> list[str]:
	final_list = []
	for note_str in available_notes_str_list:
		new_note_str = shift_note_by_semitones(note_str, semitones)
		if new_note_str in available_notes_str_list:
			final_list.append(note_str)
	return sort_notes(final_list)

def convert_sharps_to_flats(note_full_name: str) -> str:
	note_name, note_octave = separate_note_name_octave(note_full_name.capitalize())
	sharps_and_flats = note_name[1:]  # Get everything after the first character
	num_sharps = sharps_and_flats.count('#')
	num_flats = sharps_and_flats.count('b')
	increase_decrease = num_sharps - num_flats
	new_note = shift_note_by_semitones(note_name[0] + note_octave, increase_decrease)

	return new_note

def convert_flats_to_sharps(note_full_name:str) -> str: 
	new_note_full_name = convert_sharps_to_flats(note_full_name)
	note_name, note_octave = separate_note_name_octave(new_note_full_name)
	match note_name:
		case 'Db':
			return 'C#' + note_octave
		case 'Eb':
			return 'D#' + note_octave
		case 'Gb':
			return 'F#' + note_octave
		case 'Ab':
			return 'G#' + note_octave
		case 'Bb':
			return 'A#' + note_octave
		case _:
			return new_note_full_name

def notes_str_set_between_notes_str(formatted_note_str1:str, formatted_note_str2:str) -> set[str]:
	if is_note_greater(formatted_note_str1, formatted_note_str2):
		note_name1, octave1 = separate_note_name_octave(formatted_note_str2)
		note_name2, octave2 = separate_note_name_octave(formatted_note_str1)
	else:
		note_name1, octave1 = separate_note_name_octave(formatted_note_str1)
		note_name2, octave2 = separate_note_name_octave(formatted_note_str2)
	octave1_num = int(octave1)
	octave2_num = int(octave2)

	idx1 = AVAILABLE_NOTES_TUPLE.index(note_name1)
	idx2 = AVAILABLE_NOTES_TUPLE.index(note_name2)

	note_set = set()

	if octave1_num == octave2_num:
		for i in range(idx1, idx2 + 1):
			note_set.add(f"{AVAILABLE_NOTES_TUPLE[i]}{octave1_num}")
	else:
		# First add notes from note_name1 to the end of its octave
		for i in range(idx1, len(AVAILABLE_NOTES_TUPLE)):
			note_set.add(f"{AVAILABLE_NOTES_TUPLE[i]}{octave1_num}")

		# Add all notes in between octaves
		for octave in range(octave1_num + 1, octave2_num):
			for note in AVAILABLE_NOTES_TUPLE:
				note_set.add(f"{note}{octave}")

		# Finally, add notes from the beginning of the last octave to note_name2
		for i in range(idx2 + 1):
			note_set.add(f"{AVAILABLE_NOTES_TUPLE[i]}{octave2_num}")

	return note_set

def get_final_list_notes(notes_string:str, range_separators:tuple[str, ...]=('-', '–')) -> list[str]: 
	# Uses regex to get the notes from a notes_string containing single notes and a range of notes separated by the range_separators. Anything else in the notes_string is ignored.
	# Ex. input: "A1;C2D3-E3 output: ['A1', 'C2', 'D3', 'Eb3', 'E3']
	NOTE_PATTERN = "[A-Ga-g][b#]*[0-9]+"
	notes_string = notes_string.replace(' ', '')
	separator_pattern = f"[{''.join(map(re.escape, range_separators))}]"
	range_or_single_pattern = re.compile(f"({NOTE_PATTERN}){separator_pattern}({NOTE_PATTERN})|({NOTE_PATTERN})")
	single_notes = set()
	for match in range_or_single_pattern.finditer(notes_string):
		if match.group(1) and match.group(2):
			formatted_note_str1 = convert_sharps_to_flats(match.group(1))
			formatted_note_str2 = convert_sharps_to_flats(match.group(2))
			single_notes |= notes_str_set_between_notes_str(formatted_note_str1, formatted_note_str2)
		elif match.group(3):
			formatted_note_str3 = convert_sharps_to_flats(match.group(3))
			single_notes.add(formatted_note_str3)

	return sort_notes(single_notes)


if __name__ == '__main__':
	#print(get_final_list_notes('A1;C2D3-E3'))
	print(get_list_notes_able_up_down_semitones(['C4', 'D4', 'E4', 'F4', 'G4', 'A4', 'B4', 'C5'], 2))
	 