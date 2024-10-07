import re
from _collections_abc import Iterable

notes = "[A-G|a-g][b|#]*[0-9]"
note_range_pattern = re.compile(f"{notes}[-|–]{notes}")
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

#re.search(pattern, string) #only gets the first occurence
#re,findall(pattern, string) #like re.search but gets all occurences
#re.fullmatch(pattern, string)
#[^c] #all characters different than c 
#^[c] #string needs to start with 
#A group is a part of a regex pattern enclosed in parentheses () metacharacter

def sort_notes(note_iterable:Iterable[str]) -> list[str]: #sorts an iterable of note names
	if not note_iterable:
		raise ValueError("The iterable is empty.")
	
	note_name_list = []
	for note_str in note_iterable:
		note_name_list.append(convert_sharps_to_flats(note_str))
	
	def sort_note_num(note_str:str) -> int:
		return int(note_str[-1])

	def sort_note_char(note_str:str) -> int:
		return AVAILABLE_NOTES_TUPLE.index(note_str[:-1])
	
	note_name_list.sort(key=sort_note_char)
	note_name_list.sort(key=sort_note_num)
	return note_name_list

def separate_note_name_octave(note_full_name:str) -> tuple[str, str]: #Ex. input: "A1" output: ("A", "1")
	note_name = note_full_name[:-1]
	note_octave = note_full_name[-1]
	return note_name, note_octave


def is_note_greater(note1_full_name:str, note2_full_name:str) -> bool: #Ex. input: "A1", "C2" output: False
	note1_name, note1_octave = separate_note_name_octave(note1_full_name)
	note2_name, note2_octave = separate_note_name_octave(note2_full_name)
	note1_full_name = convert_sharps_to_flats(note1_full_name)
	note2_full_name = convert_sharps_to_flats(note2_full_name)
	if note1_octave == note2_octave:
		note1_name = note1_full_name[:-1]
		note2_name = note2_full_name[:-1]
		return AVAILABLE_NOTES_TUPLE.index(note1_name) > AVAILABLE_NOTES_TUPLE.index(note2_name)

	return note1_octave > note2_octave

def convert_sharps_to_flats(note_full_name:str) -> str: #Ex. input: "ab#bb3" output: "G3"
	note_name, note_octave = separate_note_name_octave(note_full_name)
	sharps_and_flats = note_name[1:]
	note_char0 = note_full_name[0].upper()
	note_char0_num = AVAILABLE_NOTES_TUPLE.index(note_char0)
	num_sharps = 0
	num_flats = 0
	note_list_len = len(AVAILABLE_NOTES_TUPLE)
	for sharp_or_flat in sharps_and_flats:
		if sharp_or_flat == '#':
			num_sharps += 1
		elif sharp_or_flat == 'b':
			num_flats += 1
		else:
			raise ValueError(f"Expected only flats (b) and sharps (#), but got {sharps_and_flats} instead. If you're the end user and is seeing this error, something is wrong with the program itself.")
	increase_decrease = num_sharps - num_flats
	new_note_char0_num = note_char0_num + increase_decrease
	new_note_char0 = AVAILABLE_NOTES_TUPLE[new_note_char0_num % note_list_len]
	
	i = increase_decrease
	if increase_decrease < 0:
		if new_note_char0_num < 0:
			new_note_octave = int(note_octave)
			while i < 0: #this is in case the decrease is more than 1. For example, if the increase_decrease is -20, the note should be 2 octaves lower
				new_note_octave -= 1
				i += note_list_len
			return new_note_char0 + str(new_note_octave)
	
	elif increase_decrease > 0:
		if new_note_char0_num >= note_list_len:
			new_note_octave = int(note_octave)
			while i > 0:
				new_note_octave += 1
				i -= note_list_len

			return new_note_char0 + str(new_note_octave)

	return new_note_char0 + note_octave
	
def get_final_list_notes(notes_string:str) -> list[str]: #Ex. input: "A1;C2" output: ["A1", "C2"]
	
	def get_set_notes_from_range(range_notes:str) -> set[str]:
		
		def get_range_pattern(separator:str, range_notes:str):
			note_range_pattern = re.compile(f"{notes}{separator}{notes}")
			if re.fullmatch(note_range_pattern, range_notes):
				return range_notes.split(separator)
		
		note_name_set = set()
		list_note_names = get_range_pattern("–", range_notes)
		if not list_note_names:
			list_note_names = get_range_pattern("-", range_notes)
			if not list_note_names:
				raise ValueError(f"{range_notes} is not a valid string.")
			
		char1 = convert_sharps_to_flats(list_note_names[0])
		char2 = convert_sharps_to_flats(list_note_names[1])
		charnum1 = AVAILABLE_NOTES_TUPLE.index(char1[0])
		charnum2 = AVAILABLE_NOTES_TUPLE.index(char2[0])
		num1 = list_note_names[0][-1]
		num1_int = int(num1)
		num2 = list_note_names[1][-1]
		num2_int = int(num2)
		if num1_int > num2_int or (num1 ==  num2 and charnum2 < charnum1):
			raise ValueError(f"Invalid range. {list_note_names[0]} > {list_note_names[1]}")
		
		def add_notes_to_set(charnum1, charnum2):
			for charnum in range(charnum1, charnum2 + 1):
					note_char = AVAILABLE_NOTES_TUPLE[charnum]
					note_name_set.add(note_char + str(note_num))
		
		for note_num in range(num1_int, num2_int+1):

			if note_num == num1_int and note_num == num2_int:
				add_notes_to_set(charnum1, charnum2)

			elif note_num == num1_int:
				add_notes_to_set(charnum1, len(AVAILABLE_NOTES_TUPLE)-1)
			
			elif note_num == num2_int:
				add_notes_to_set(0, charnum2)
			else:
				add_notes_to_set(0, len(AVAILABLE_NOTES_TUPLE)-1)

		return note_name_set

	def get_set_notes(notes_string:str) -> set[str]:
		notes_string = notes_string.replace(" ", "")
		pattern = re.compile(f"({notes};)*({notes})") #example format: A1;B3
		if re.search(pattern, notes_string):
			set_notes = set(notes_string.split(";"))
		else:
			pattern = re.compile(f"({notes};)*({notes});") #example format: A1;B3;
			if re.search(pattern, notes_string):
				note_name_list = notes_string.split(";")
				note_name_list.pop()
				set_notes = set(note_name_list)
			else:
				raise ValueError(f"{notes_string} is not a valid string.")
		return set_notes

	if type(notes_string) != str:
		raise TypeError(f"Expected a string, but got {type(notes_string)} instead.") 
	
	notes_and_ranges_set = get_set_notes(notes_string)
	note_name_set = set()
	for note_or_range in notes_and_ranges_set:
		if re.search(note_range_pattern, note_or_range):
			note_name_set |= get_set_notes_from_range(note_or_range)
		else:
			new_note = convert_sharps_to_flats(note_or_range)
			note_name_set.add(new_note)

	note_name_list = sort_notes(note_name_set)
	return note_name_list