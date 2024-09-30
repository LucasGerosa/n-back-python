from utils.note_str_utils import AVAILABLE_NOTES_TUPLE


class ChromaticScale:
	name = 'Chromatic'
	def __init__(self, root_note:str):
		assert root_note in AVAILABLE_NOTES_TUPLE, f"Invalid root note: {root_note}"
		self.root_note = root_note
		self.notes_str_tuple = AVAILABLE_NOTES_TUPLE
		self.intervals = (1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1)
	
	def get_note_index(self, note):
		return self.notes_str_tuple.index(note)
	
	def __str__(self):
		return f'{self.root_note} {self.name} scale containing ' + str(self.notes_str_tuple)
	
	def find_able_up_down_semitones(self, semitones:int):
		assert semitones != 0, "semitones start at 1. Calling this function without semitones makes no sense."
		
		if semitones > 0: #this ensures the semitones count starts at 1, making it more intuitive.
			semitones -= 1
		
		possible_notes = []
		note_i = 0
		for note in self.notes_str_tuple:
			if self.intervals[note_i + semitones] == 1:
				possible_notes.append(note)
			note_i += 1
		
		return possible_notes

class MajorScale(ChromaticScale):
	name = 'Major'
	def __init__(self, root_note:str):
		super().__init__(root_note)
		self.intervals = (2, 2, 1, 2, 2, 2, 1)  # Pattern of the scale: Whole (2), Half (1)
		self.notes_str_tuple = self.generate_scale()
	
	def generate_scale(self):
		notes_str_tuple = []
		index = self.get_note_index(self.root_note)
		for interval in self.intervals:
			notes_str_tuple.append(self.notes_str_tuple[index % len(self.notes_str_tuple)])  # Wrap around notes
			index += interval
		return tuple(notes_str_tuple)
	

if __name__ == '__main__':
	C_scale = MajorScale('C')
	print(C_scale)
	print("Notes that can go up a semitone: ", C_scale.find_able_up_semitone())
	print("Notes that can go down a semitone: ", C_scale.find_able_down_semitone())

