import os
import typing
import random
import time
import sys
from pydub import AudioSegment, playback
from pydub.silence import detect_leading_silence
import gc
#import pyaudio
#from pydub import utils
import time
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from utils.defaults import *
from utils import note_str_utils

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.normpath(ROOT_DIR + '/..')
DEFAULT_NOTE_EXTENSION = 'mp3'
DEFAULT_AUDIO_EXTENSION = 'aiff'
NOTES_FOLDER = 'input'
AUDIO_FOLDER = 'aiff'

'''
This module provides abstraction for musical notes, allowing the user to play them and manipulate them, as well as convert and edit note files from aiff to mp3.
'''

import platform
os_name = platform.system()

def bpmToSeconds(bpm: float) -> float:
	return 60 / bpm

def get_app_path():
	if getattr(sys, 'frozen', False):
		# If the application is an executable created by PyInstaller
		app_path = os.path.dirname(sys.executable)
		return app_path
	# If the application is running as a script
	return PROJECT_DIR
	
def check_ffmpeg():
	app_path = get_app_path()  # Use the get_app_path() function we'll create in step 2
	ffmpeg_path = os.path.join(app_path, 'ffmpeg', 'bin')
	#ffmpeg_path = f'{PROJECT_DIR}/ffmpeg/bin'
	ffmpeg_in_root_dir = os.path.exists(ffmpeg_path)
	ffmpeg_in_path = os.path.normcase('ffmpeg/bin') in os.path.normcase(os.environ['PATH'])
	windows_ffmpeg_url = 'https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip'
	import requests
	if os_name == 'Windows':

		if ffmpeg_in_path:
			return
		
		if ffmpeg_in_root_dir:
			os.environ['PATH'] += f';{ffmpeg_path};'
			return
		
		else:
			print(f"ffmpeg not found. Attempting to download it...\nIf you do have it installed, please press ctrl+c and add it to path or move the ffmpeg folder to {PROJECT_DIR}")
			request = requests.get(windows_ffmpeg_url)
			if request.status_code == 200:
				with open("ffmpeg-release-essentials.zip", 'wb') as f:
					f.write(request.content)
				
				raise Exception(f"Successfully downloaded the ffmpeg zip to {PROJECT_DIR}. Now extract it to that folder and run this program again.")
			else:
				raise Exception(f'ffmpeg zip failed to download. Check your internet connection or go to {windows_ffmpeg_url} and extract that file to {PROJECT_DIR}, and then run this file again.\nIf that doesn\'t work, contact the developers.')

	elif os_name == 'Linux':
		import shutil

		if ffmpeg_in_root_dir:
			os.environ['PATH'] += f';{ffmpeg_path};'
			return
		
		elif shutil.which('ffmpeg'):
			os.environ['PATH'] += shutil.which('ffmpeg') + ';'
			return

		else:
			import webbrowser
			webbrowser.open("http://www.ffmpeg.org/download.html#build-linux")
		
	elif os_name == 'Darwin':
		print('MacOS is currently not supported. Ask the developers to implement it.')
		requests.get("https://evermeet.cx/ffmpeg/ffmpeg-109856-gf8d6d0fbf1.zip")
		
	else:
		raise OSError('Invalid OS. Please contact the developers.')

	raise OSError(f'ffmpeg not installed or not in the required directories. After installation it should be put in either the environment variables or in the root directory of this project. Download ffmpeg and/or put it in the root directory of this project.')

def remove_silence_and_save(note_path):
	pass

def remove_silence_and_save_all_notes():
	for instrument in os.listdir(NOTES_FOLDER):
		instrument_path = os.path.join(NOTES_FOLDER, instrument)
		for note in os.listdir(instrument_path):
			note_path = os.path.join(instrument_path, note)
			remove_silence_and_save(note_path)

#remove_silence_and_save_all_notes()
check_ffmpeg()

class Note:
	'''Represents musical notes, pointing to an mp3 file that can be played.'''

	def __init__(self, path:str, bpm:float=DEFAULT_BPM, will_create_sound:bool=True, note_value:float=DEFAULT_NOTE_VALUE) -> None:
		self.path = path #TODO:don't allow the creation of a note with an invalid path
		if self.extension == 'aif':
			self.change_extension('aiff')
		self._will_create_sound = False
		self.will_create_sound:bool = will_create_sound
		self.bpm = bpm
		self.note_value = note_value
		self.intensity = self.get_intensity()
	
	@property
	def will_create_sound(self):
		return self._will_create_sound
	
	@will_create_sound.setter
	def will_create_sound(self, will_create_sound:bool) -> None:
		assert type(will_create_sound) == bool, f"will_create_sound must be a boolean, not {type(will_create_sound)}"
		if will_create_sound and not self.will_create_sound: #this will prevent sounds from being created if they are not going to be played, improving performance
			self._create_sound()
		self._will_create_sound = will_create_sound
	
	def _create_sound(self) -> None:
		
		self._sound:AudioSegment = AudioSegment.from_file(self.path, self.extension)
		#self._sound = self.remove_silence()

	@property
	def sound(self):
		return self._sound

	@sound.deleter
	def sound(self) -> None:
		self._will_create_sound = False
		del self._sound
	
	@property
	def path(self):
		return self._path

	@path.setter
	def path(self, new_path) -> None:
		self._path = new_path
		self._directory, fileNameExt = os.path.split(new_path) #directory won't have a trailing '/'
		self._fileName, ext = os.path.splitext(fileNameExt)
		self._extension =  ext.split('.')[1]
		self._full_name = self.fileName.split('.')[-1]
		self._name, self._octave = note_str_utils.separate_note_name_octave(self.full_name)
		instrument_dir, DEFAULT_AUDIO_EXTENSION_dir = os.path.split(self.directory)
		if DEFAULT_AUDIO_EXTENSION_dir == DEFAULT_AUDIO_EXTENSION:
			self._instrument:str = os.path.split(instrument_dir)[1]
		else:
			self._instrument:str = DEFAULT_AUDIO_EXTENSION_dir
	
	@staticmethod
	def get_note_attributes_from_path(path:str) -> tuple:
		directory, file_name = os.path.split(path)
		file_name, extension = os.path.splitext(file_name)
		instrument, intensity, note_full_name = file_name.split('.')
		return directory, instrument.lower(), intensity, note_full_name, extension

	@property
	def directory(self):
		return self._directory
	
	@property
	def instrument(self):
		return self._instrument
	
	#TODO: add setter method for changing the path when the full_name is changed
	@property
	def full_name(self):
		return self._full_name
	
	@property
	def name(self):
		return self._name
	
	@property
	def octave(self):
		return self._octave
	
	@property
	def fileName(self):
		return self._fileName
	
	@property
	def extension(self):
		return self._extension

	def __eq__(self, other_note) -> bool:
		if isinstance(other_note, Note):
			return self.path == other_note.path
		raise TypeError(f"Can't compare Note object with {type(other_note)} object.")
	
	def __str__(self) -> str:
		return f"Note object '{self.fileName}.{self.extension}' at {self.directory}."
	
	def get_intensity(self) -> str: #gets the intensity of the note (e.g. pp, mf, f, etc)
		intensity = self.fileName.split('.')[1]
		return intensity

	def __gt__(self, other_note):
		return note_str_utils.is_note_greater(self.full_name, other_note.full_name)
	
	def __lt__(self, other_note):
		return note_str_utils.is_note_greater(other_note.full_name, self.full_name)
	
	def __ne__(self, other_note):
		return not self.__eq__(other_note)
	
	def __ge__(self, other_note):
		return self.__gt__(other_note) or self.__eq__(other_note)
	
	def __le__(self, other_note):
		return self.__lt__(other_note) or self.__eq__(other_note)
	

	# def _play_with_pyaudio(self, seg, t):
		# p = pyaudio.PyAudio()
		# stream = p.open(format=p.get_format_from_width(seg.sample_width),
		# 				channels=seg.channels,
		# 				rate=seg.frame_rate,
		# 				output=True)

		# # Just in case there were any exceptions/interrupts, we release the resource
		# # So as not to raise OSError: Device Unavailable should play() be used again

		# chunk = utils.make_chunks(seg, t)[0]
		# stream.write(chunk._data)
		# stream.stop_stream()
		# stream.close()

		# p.terminate()

	def play(self) -> None:
		if self.extension !='mp3': #TEMPORARY
			raise NotImplementedError(f"Notes with extensions besides mp3 can't be played. Path of note: {self.path}")
	
		if not self.will_create_sound:
			self._create_sound()
		#current_playback = self._play_with_pyaudio(self.sound, t)
		t = bpmToSeconds(self.bpm) * 4 * self.note_value
		current_playback = playback._play_with_simpleaudio(self.sound)
		time.sleep(t)
		current_playback.stop()
		del current_playback  # Suggest deletion of the playback object
		del self.sound  # Suggest deletion of the sound object
		gc.collect()  # Explicitly suggest garbage collection
		
	def change_extension(self, new_extension:str) -> None:
		new_path = os.path.join(self.directory, self.fileName + '.' + new_extension)
		if os.path.exists(new_path):
			self.delete_file()
		else:
			os.rename(self.path, new_path)
		self.path = new_path
	
	def convert(self, new_extension:str = DEFAULT_NOTE_EXTENSION, directory:str = NOTES_FOLDER, delete_old_file = False) -> None: #note: this directory should not be from the main directory of the project
		new_path = os.path.join(ROOT_DIR, '..', directory, self.instrument, self.fileName + '.' + new_extension)
		self.sound.export(new_path, format = new_extension)
		#This is equivalent to "ffmpeg -i input/notas/aiff/do.aiff input/notas/aiff/do.mp3"
		if delete_old_file:
			self.delete_file()
		self.path = new_path
	
	def remove_silence(self) -> AudioSegment:
		start_trim = detect_leading_silence(self.sound)
		end_trim = detect_leading_silence(self.sound.reverse())
		trimmed_sound = self.sound[start_trim:len(self.sound)-end_trim]
		trimmed_sound.export(self.path, format = self.extension)
		#return trimmed_sound
	
	def delete_file(self) -> None:
		os.remove(self.path)
	
	def __add__(self, semitones):
		#makes a note with the same attributes but with X semitones of difference
		assert isinstance(semitones, int), f"Can't add {type(semitones)} to a Note object."
		if semitones < 0:			
			name = self.name + "b" * (-semitones)
		elif semitones > 0: 
			name = self.name + "#" * semitones
		full_name = note_str_utils.convert_sharps_to_flats(name + self.octave)
		
		assert not note_str_utils.is_note_greater(full_name, HIGHEST_NOTE), f"Tried to increase the semitone of {self.full_name}, getting {full_name}, but {HIGHEST_NOTE} is the last possible note on the program."
		assert not note_str_utils.is_note_greater(LOWEST_NOTE, full_name), f"Tried to decrease the semitone of {self.full_name}, but {LOWEST_NOTE} is the first possible note on the program."
		
		return Note.get_note_from_note_full_name(full_name, self.intensity, self.bpm, self.will_create_sound, self.instrument, self.note_value)
	
	def __sub__(self, semitones:int):
		return self.__add__(-semitones)

	@staticmethod
	def get_greater_note(note1, note2):
		if note1 > note2:
			return note1
		return note2

	@staticmethod
	def get_note_file_name_from_note_full_name(note_full_name:str, intensity:str=DEFAULT_INTENSITY, instrument:str=DEFAULT_INSTRUMENT):
		app_path = get_app_path()
		file_name = os.path.join(app_path, NOTES_FOLDER, instrument, f"{instrument.capitalize()}.{intensity}.{note_full_name}.{DEFAULT_NOTE_EXTENSION}")
		return file_name

	@staticmethod
	def get_note_from_note_full_name(note_full_name:str, intensity:str=DEFAULT_INTENSITY, bpm:float=DEFAULT_BPM, will_create_sound:bool=True, instrument:str=DEFAULT_INSTRUMENT, note_value:float=DEFAULT_NOTE_VALUE):
		file_name = Note.get_note_file_name_from_note_full_name(note_full_name, intensity, instrument)
		return Note(file_name, bpm, will_create_sound, note_value=note_value)
	
	@staticmethod
	def does_note_file_exist(note_full_name:str, intensity:str=DEFAULT_INTENSITY, instrument:str=DEFAULT_INSTRUMENT):
		file_name = Note.get_note_file_name_from_note_full_name(note_full_name, intensity, instrument)
		return os.path.exists(file_name)
			
class Note_group:
	'''Container class for Note instances. This can be treated pretty much as a list of notes with extra methods.'''

	def __init__(self, notes_str:typing.List[str], intensity:str=DEFAULT_INTENSITY, bpm:float=DEFAULT_BPM, will_create_sound:bool=True, instrument:str=DEFAULT_INSTRUMENT, note_value:float=DEFAULT_NOTE_VALUE):
		self._notes:typing.List[Note] = []
		self._notes_str:list[str] = []
		note_str_set = set(notes_str) #type:ignore
		note_set = [Note.get_note_from_note_full_name(note_str, intensity, bpm, will_create_sound, instrument, note_value) for note_str in note_str_set]
		for note_str in notes_str:
			for note in note_set:
				if note.full_name == note_str:
					self._notes.append(note)
					self._notes_str.append(note_str)
					break		
	
	@property
	def notes(self):
		return self._notes

	@property
	def notes_str(self):
		return self._notes_str
	
	getNotePaths = lambda self: [note.path for note in self.notes]
	''' Equivalent to this:
	def getNotePaths(self):
		note_paths = []
		for note in self.notes:
			note_paths.append(note.path)
		return [note.path for note in self.notes]
	'''
	def __len__(self):
		return len(self.notes)
	
	def __getitem__(self, index):
		return self.notes[index]

	def __setitem__(self, index, value):
		raise NotImplementedError("Setting items in a Note_group is not recommended. It's preferable to create a Note_group only when you have all the notes you need.")
		self.notes[index] = value
	
	def __delitem__(self, index):
		del self.data[index]

	def __contains__(self, note):
		return note in self.notes
	
	def __iter__(self):
		return iter(self.notes)

	def __str__(self):
		return 'Note_group containing ' + str(self.notes_str)

	def __add__(self, other_note_group):
		#assert isinstance(other_note_group, Note_group), f"Can't add Note_group object with {type(other_note_group)} object."
		if isinstance(other_note_group, Note_group):
			return Note_group(self.notes_str + other_note_group.notes_str)
		elif isinstance(other_note_group, list) or isinstance(other_note_group, tuple):
			return Note_group(self.notes_str + other_note_group)
		else:
			raise TypeError(f"Can't add Note_group object with {other_note_group} ({type(other_note_group)}) object.")
	
	def __radd__(self, other_note_group):
		return self.__add__(other_note_group)
	
	def __eq__(self, value):
		if isinstance(value, Note_group):
			return self.notes == value.notes
		elif isinstance(value, list) or isinstance(value, tuple):
			return self.notes == value
		return False
	
	def __ne__(self, value):
		return not self.__eq__(value)
	
	def append(self, note):
		raise NotImplementedError("Appending notes to a Note_group is not recommended. It's preferable to create a Note_group only when you have all the notes you need.")
		self.notes.append(note)

	def play(self):
		notes_played = 0
		time_started = time.time()
		for note in self.notes:

			try:
				note.play()
				yield 
			except Exception as e:
				time_ended = time.time()
				print("\nNumber of notes played before this error: " + str(notes_played))
				print("Time elapsed: " + str(time_ended - time_started) + " seconds.\n")
				raise e
			notes_played += 1
		time_ended = time.time()
		print("Total time elapsed: " + str(time_ended - time_started) + " seconds.")
	
	def change_extension(self, new_extension) -> None:
		for note in self.notes:
			note.change_extension(new_extension)
	
	def convert(self, new_extension:str = DEFAULT_NOTE_EXTENSION, directory:str = NOTES_FOLDER, delete_old_files = False):
		for note in self.notes:
			note.convert(new_extension, directory, delete_old_files)
			yield note
	
	def remove_silence(self):
		for note in self:
			note.remove_silence(note.sound)
			yield
	
	def getRandomNote(self):
		number_of_notes = len(self.notes)
		if number_of_notes == 0:
			return None
		random_number = random.randint(0, number_of_notes - 1)
		# retrieve sound from id
		random_note = self.notes[random_number]
		random_note.play()
		return random_note

	def delete_files(self) -> None:
		for note in self.notes:
			note.delete_file()

''' 
	For future reference for working with aiff or wav
	Audio signal parameters:
	
		Number of channels: mono or stereo
		Sample width: number of bytes for each saample
		framerate/sample_rate: E.g. 44,100 Hz standard rate for CD quality
		Number of frames
		Values of a frame
	'''

if __name__ == '__main__':
	import time
	
	def load_notes(note_num, note_group, note_value=1/4, will_create_sound=True):
		start_time = time.time()
		for _ in range(note_num):
			n = Note("input/piano/Piano.mf.C4.mp3", note_value=note_value, will_create_sound=will_create_sound)
			note_group.append(n)
		end_time = time.time()
		exe_time = end_time - start_time
		print(f"Execution time: {exe_time} seconds. Approximately {exe_time/note_num} seconds per note.")

	def test_generator(note_num):
		player = note_group.play()
		notes_played = 0
		for _ in range(note_num):
			next(player)
			notes_played += 1
		print("Number of notes played:", notes_played)
	
	def test0(): #fails after 60 notes.
		load_notes(note_num, note_group, note_value)
		test_generator(note_num)

	def test1(): #fails; creating 2 different generators with half the notes still does not work.
		load_notes(note_num, note_group, note_value)
		test_generator(note_num//2)
		test_generator(note_num//2)
	
	def test2(): #fails; creating a notes and playing them 100 times doesn't work.
		notes_played = 0
		for _ in range(note_num):
			note = Note("input/piano/Piano.mf.C4.mp3", note_value=note_value)
			try:
				note.play()
			except Exception as e:
				print("Number of notes played before this error: " + str(notes_played))
				raise e
			notes_played += 1

	def test3(): #fails; creating one note and playing it 100 times doesn't work.
		notes_played = 0
		note = Note("input/piano/Piano.mf.C4.mp3", note_value=note_value)
		playback._play_with_simpleaudio(note.sound)
		for _ in range(note_num):
			try:
				note.play()
			except Exception as e:
				print("Number of notes played before this error: " + str(notes_played))
				raise e
			notes_played += 1
	
	def test4():
		note_gp = Note_group(['F4', 'G4', 'A4', 'B4', 'C5', 'C4', 'D4', 'E4'])
		for note in note_gp:
			print(note)
		
		note_gp = Note_group(['A4']*100)
		print(note_gp)
	
	note_value = 1/32
	note_num = 100
	test4()
	
	#load_notes(note_group, 1/32)
	
	#test1(1/4) #49s; 60 notes
	#test1(1/2) #97s; 60 notes
	#test1(1/8) #25s; 60 notes
	#test1(1/8, False) #31s; 60 notes; 6e-6s per note

	