import re
from _collections_abc import Iterable

notes = "[A-G|a-g][b|#]*[0-9]"
note_range_pattern = re.compile(f"{notes}[-|–]{notes}")
note_list = [	#TODO: add functionality for equality of sharp and flat notes
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
]
#re.search(pattern, string) #only gets the first occurence
#re,findall(pattern, string) #like re.search but gets all occurences
#re.fullmatch(pattern, string)
#[^c] #all characters different than c 
#^[c] #string needs to start with 
#A group is a part of a regex pattern enclosed in parentheses () metacharacter

def sort_notes(note_iterable:Iterable[str]) -> list[str]: #sorts an iterable of note names
	if not note_iterable:
		raise ValueError("The iterable is empty.")
	def sort_note_num(note_str:str) -> int:
		return int(note_str[-1])

	def sort_note_char(note_str:str) -> int:
		return note_list.index(note_str[:-1])
	
	note_name_list = list(note_iterable)
	note_name_list.sort(key=sort_note_char)
	note_name_list.sort(key=sort_note_num)
	return note_name_list

def convert_sharps_to_flats(note_char:str, note_number:str) -> str: #Ex. input: "ab#bb3" output: "E3"
	sharps_and_flats = note_char[1:]
	note_char0 = note_char[0].upper()
	note_char0_num = note_list.index(note_char0)
	num_sharps = 0
	num_flats = 0
	note_list_len = len(note_list)
	for sharp_or_flat in sharps_and_flats:
		if sharp_or_flat == '#':
			num_sharps += 1
		elif sharp_or_flat == 'b':
			num_flats += 1
		else:
			raise ValueError(f"Expected only flats (b) and sharps (#), but got {sharps_and_flats} instead. If you're the end user and is seeing this error, something is wrong with the program itself.")
	increase_decrease = num_sharps - num_flats
	new_note_char0_num = note_char0_num + increase_decrease
	new_note_char0 = note_list[new_note_char0_num % note_list_len]
	
	i = increase_decrease
	if increase_decrease < 0:
		if new_note_char0_num < 0:
			new_note_number = int(note_number)
			while i < 0: #this is in case the decrease is more than 1. For example, if the increase_decrease is -20, the note should be 2 octaves lower
				new_note_number -= 1
				i += note_list_len
			return new_note_char0 + str(new_note_number)
	
	elif increase_decrease > 0:
		if new_note_char0_num >= note_list_len:
			new_note_number = int(note_number)
			while i > 0:
				new_note_number += 1
				i -= note_list_len

			return new_note_char0 + str(new_note_number)

	return new_note_char0 + note_number
	
def get_final_list_notes(notes_string:str) -> list[str]:
	
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
				raise Exception(f"{range_notes} is not a valid string.")

		char1 = convert_sharps_to_flats(list_note_names[0][:-1], list_note_names[0][-1])
		char2 = convert_sharps_to_flats(list_note_names[1][:-1], list_note_names[1][-1])
		charnum1 = note_list.index(char1)
		charnum2 = note_list.index(char2)
		num1 = list_note_names[0][-1]
		num1_int = int(num1)
		num2 = list_note_names[1][-1]
		num2_int = int(num2)
		if num1_int > num2_int or (num1 ==  num2 and charnum2 < charnum1):
			raise Exception(f"Invalid range. {list_note_names[0]} > {list_note_names[1]}")
		
		def add_notes_to_set(charnum1, charnum2):
			for charnum in range(charnum1, charnum2 + 1):
					note_char = note_list[charnum]
					note_name_set.add(note_char + str(note_num))
		
		for note_num in range(num1_int, num2_int+1):

			if note_num == num1_int and note_num == num2_int:
				add_notes_to_set(charnum1, charnum2)

			elif note_num == num1_int:
				add_notes_to_set(charnum1, len(note_list)-1)
			
			elif note_num == num2_int:
				add_notes_to_set(0, charnum2)
			else:
				add_notes_to_set(0, len(note_list)-1)

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
				raise Exception(f"{notes_string} is not a valid string.")
		return set_notes

	notes_and_ranges_set = get_set_notes(notes_string)
	note_name_set = set()
	for note_or_range in notes_and_ranges_set:
		if re.search(note_range_pattern, note_or_range):
			note_name_set |= get_set_notes_from_range(note_or_range)
		else:
			new_note = convert_sharps_to_flats(note_or_range[:-1], note_or_range[-1])
			note_name_set.add(new_note)

	note_name_list = sort_notes(note_name_set)
	return note_name_list

def test():
	print(convert_sharps_to_flats('a###', '3'))
	print(convert_sharps_to_flats('Cbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb', '3'))
	print(convert_sharps_to_flats('b#', '3'))
	s1 = "A1;C2"
	s2 = "C2;      B2"
	s3 = "A4-G5"
	s4 = "D3-C4"
	s5 = "C4-B5"
	s6 = "a1-b2"
	s7 = "Ab3-Cb4"
	s8 = "A4-G5; A1-C2"
	s9 = "A4-G5;C####2"
	s10 = "C4-C6"
	s11 = "Cbb2"
	#print(get_final_list_notes(s1))
	#print(get_final_list_notes(s2))
	#print(get_final_list_notes(s3))
	#print(get_final_list_notes(s4))
	#print(get_final_list_notes(s5))
	#print(get_final_list_notes(s6))
	#print(get_final_list_notes(s7))
	#print(get_final_list_notes(s8))
	#print(get_final_list_notes(s9))
	#print("s10: ", get_final_list_notes(s10))
	#print("s11: ", get_final_list_notes(s11))

if __name__ == '__main__':
	test()