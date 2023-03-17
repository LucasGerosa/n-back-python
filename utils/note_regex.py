import re


notes = "[A-G|a-g][0-9]"
note_range_pattern = re.compile(f"{notes}[-|–]{notes}")
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
    for c in range(ord(c1), ord(c2)+1):
        yield chr(c)
	
def get_set_notes_from_range(range_notes:str) -> set:
	list_note_names = get_range_pattern("–", range_notes)
	if list_note_names:
		get_char_range()
	
	list_note_names = get_range_pattern("-", range_notes)
	if list_note_names:

		return
	raise Exception(f"{range_notes} is not a valid string.")

def get_set_notes(notes_string:str) -> set:
	notes_string.replace(" ", "")
	
	pattern = re.compile(f"({notes};)*({notes})") #example format: A1;B3
	if re.search(pattern, notes_string):
		return set(notes_string.split(";"))
	
	pattern = re.compile(f"({notes};)*({notes});") #example format: A1;B3;
	if re.search(pattern, notes_string):
		note_name_list = notes_string.split(";")
		note_name_list.pop()
		return set(note_name_list)
	
	note_ranges = re.findall(note_range_pattern, notes_string)
	if note_ranges:
		note_name_set = set()
		for note_range in note_ranges:
			note_name_set |= get_set_notes_from_range(note_range)

		return note_name_set


	raise Exception(f"{notes_string} is not a valid string.")