import re


notes = "[A-G|a-g][0-9]"
note_range_pattern = re.compile(f"{notes}[-|–]{notes}")
note_dict = {
	'C':0,
	'D':1,
	'E':2,
	'F':3,
	'G':4,
	'A':5,
	'B':6
}
#re.search(pattern, string) #only gets the first occurence
#re,findall(pattern, string) #like re.search but gets all occurences
#re.fullmatch(pattern, string)
#[^c] #all characters different than c 
#^[c] #string needs to start with 
#A group is a part of a regex pattern enclosed in parentheses () metacharacter

def get_range_pattern(separator:str, range_notes:str):
	note_range_pattern = re.compile(f"{notes}{separator}{notes}")
	if re.fullmatch(note_range_pattern, range_notes):
		return range_notes.split(separator)

def get_char_range(c1, c2):
	"""Generates the characters from `c1` to `c2`, inclusive."""
	chars = []
	for c in range(ord(c1), ord(c2)+1):
		chars.append(chr(c))
	    
	return chars
	
def get_set_notes_from_range(range_notes:str) -> set[str]:
	note_name_set = set()
	list_note_names = get_range_pattern("–", range_notes)
	if not list_note_names:
		list_note_names = get_range_pattern("-", range_notes)
		if not list_note_names:
			raise Exception(f"{range_notes} is not a valid string.")

	char1 = list_note_names[0][0].upper()
	char2 = list_note_names[1][0].upper()
	charnum1 = note_dict[char1]
	charnum2 = note_dict[char2]
	num1 = list_note_names[0][1]
	num2 = list_note_names[1][1]
	if int(num1) > int(num2):
		raise Exception(f"Invalid range. {num1} > {num2}")
	for num in range(int(num1), int(num2)):
		for char in range(charnum1, charnum2):
			note_name_set.add(char + str(num))
	return note_name_set
	
def get_final_set_notes(notes_string:str):

	def get_set_notes(notes_string:str) -> set[str]:
		notes_string = notes_string.replace(" ", "")
		
		pattern = re.compile(f"({notes};)*({notes})") #example format: A1;B3
		if re.search(pattern, notes_string):
			return set(notes_string.split(";"))
		
		pattern = re.compile(f"({notes};)*({notes});") #example format: A1;B3;
		if re.search(pattern, notes_string):
			note_name_list = notes_string.split(";")
			note_name_list.pop()
			return set(note_name_list)

		raise Exception(f"{notes_string} is not a valid string.")

	notes_and_ranges_set = get_set_notes(notes_string)
	note_name_set = set()
	for note_or_range in notes_and_ranges_set:
		if re.search(note_range_pattern, note_or_range):
			note_name_set |= get_set_notes_from_range(note_or_range)
		else:
			note_name_set.add(note_or_range)
	return note_name_set

def test():
	s1 = "A1;C2"
	s2 = "C2;      B2"
	s3 = "A4-G5"
	s4 = "D3-C4"
	print(get_final_set_notes(s1))
	print(get_final_set_notes(s2))
	print(get_final_set_notes(s3))
	print(get_final_set_notes(s4))

if __name__ == '__main__':
	test()