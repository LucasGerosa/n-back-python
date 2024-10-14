import os
import typing
import random
import sys
from pydub import AudioSegment, playback
from pydub.silence import detect_leading_silence
import gc
#import pyaudio
#from pydub import utils
#TODO: change some of the methods in these classes to private methods

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

check_ffmpeg()

class Note:

	def __init__(self, path:str, bpm:float=DEFAULT_BPM, will_create_sound:bool=True, note_value:float=DEFAULT_NOTE_VALUE) -> None:
		self.path = path #TODO:don't allow the creation of a note with an invalid path
		if self.extension == 'aif':
			self.change_extension('aiff')
		self._will_create_sound = None
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
			self.create_sound()
		self._will_create_sound = will_create_sound
	
	def create_sound(self) -> None:
		
		def remove_silence(sound) -> AudioSegment: #TODO: edit the file to remove the sound, not just in runtime
			trim_leading_silence = lambda x: x[detect_leading_silence(x) :]
			#trim_trailing_silence = lambda x: trim_leading_silence(x.reverse()).reverse() #removes silence from 
			#strip_silence = lambda x: trim_trailing_silence(trim_leading_silence(x))
			#stripped = strip_silence(self.sound)
			return trim_leading_silence(sound)
		
		self._sound = remove_silence(AudioSegment.from_file(self.path, self.extension))
	
	@property
	def sound(self):
		return self._sound
	
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
			self.create_sound()
		#current_playback = self._play_with_pyaudio(self.sound, t)
		current_playback = playback._play_with_simpleaudio(self.sound)
		t = bpmToSeconds(self.bpm)*4*self.note_value
		time.sleep(t)
		current_playback.stop()
		del current_playback  # Suggest deletion of the playback object
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
		self.sound.export(new_path, format = new_extension) #! Maybe this needs to be self._sound instead. Needs testing
		#This is equivalent to "ffmpeg -i input/notas/aiff/do.aiff input/notas/aiff/do.mp3"
		if delete_old_file:
			self.delete_file()
		self.path = new_path
	
	def delete_file(self) -> None:
		os.remove(self.path)
	
	def __add__(self, semitones):
		#TODO: make this method change the note's path instead of creating a new note
		#makes a note with the same attributes but with X semitones of difference
		assert isinstance(semitones, int), f"Can't add {type(semitones)} to a Note object."
		if semitones < 0:			
			name = self.name + "b" * (-semitones)
		elif semitones > 0: 
			name = self.name + "#" * semitones
		full_name = note_str_utils.convert_sharps_to_flats(name + self.octave)
		
		assert not note_str_utils.is_note_greater(full_name, HIGHEST_NOTE), f"Tried to increase the semitone of {self.full_name}, getting {full_name}, but {HIGHEST_NOTE} is the last possible note on the program."
		assert not note_str_utils.is_note_greater(LOWEST_NOTE, full_name), f"Tried to decrease the semitone of {self.full_name}, but {LOWEST_NOTE} is the first possible note on the program."
		
		return Note.get_note_from_note_name(full_name, self.intensity, self.bpm, self.will_create_sound, self.instrument, self.note_value)
	
	def __sub__(self, semitones:int):
		return self.__add__(-semitones)

	@staticmethod
	def get_greater_note(note1, note2):
		if note1 > note2:
			return note1
		return note2

	@staticmethod
	def get_note_from_note_name(note_name:str, intensity:str=DEFAULT_INTENSITY, bpm:float=DEFAULT_BPM, will_create_sound:bool=True, instrument:str='piano', note_value:float=DEFAULT_NOTE_VALUE):
		app_path = get_app_path()
		file_name = os.path.join(app_path, NOTES_FOLDER, instrument, f"{instrument.capitalize()}.{intensity}.{note_name}.{DEFAULT_NOTE_EXTENSION}")

		return Note(file_name, bpm, will_create_sound, note_value=note_value)
			
class Note_group:
	'''Container class for Note instances. This can be treated pretty much as a list of notes with extra methods.'''

	def __init__(self, notes:typing.Optional[typing.List[Note]] = None):
		self.stop_flag = False
		if notes == None:
			self.notes: typing.List[Note] = []
		else:    
			self.notes = notes #type:ignore
	
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
		self.notes[index] = value
	
	def __delitem__(self, index):
		del self.data[index]

	def __contains__(self, note):
		return note in self.notes
	
	def __iter__(self):
		return iter(self.notes)

	def __str__(self):
		return 'Note_group containing ' + str(self.notes)

	def __add__(self, other_note_group):
		#assert isinstance(other_note_group, Note_group), f"Can't add Note_group object with {type(other_note_group)} object."
		if isinstance(other_note_group, Note_group):
			return Note_group(self.notes + other_note_group.notes)
		elif isinstance(other_note_group, list) or isinstance(other_note_group, tuple):
			return Note_group(self.notes + other_note_group)
		else:
			raise TypeError(f"Can't add Note_group object with {type(other_note_group)} object.")
	
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
		self.notes.append(note)

	def play(self):
		notes_played = 0
		for note in self.notes:
			
			if self.stop_flag:
				self.stop_flag = False
				break

			try:
				note.play()
			except Exception as e:
				print("\nNumber of notes played before this error: " + str(notes_played) + "\n")
				raise e
			notes_played += 1
	
	def change_extension(self, new_extension) -> None:
		for note in self.notes:
			note.change_extension(new_extension)
	
	def convert(self, new_extension:str = DEFAULT_NOTE_EXTENSION, directory:str = NOTES_FOLDER, delete_old_files = False) -> None:
		for note in self.notes:
			note.convert(new_extension, directory, delete_old_files)
	
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
	
	@staticmethod
	def get_note_group_from_note_names(note_names:typing.List[str], intensity:str=DEFAULT_INTENSITY, bpm:float=DEFAULT_BPM, will_create_sound:bool=True, instrument:str='piano', note_value:float=DEFAULT_NOTE_VALUE) -> 'Note_group':
		notes = []
		for note_name in note_names:
			notes.append(Note.get_note_from_note_name(note_name, intensity, bpm, will_create_sound, instrument, note_value))
		return Note_group(notes)

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
	n = Note("input/piano/Piano.mf.C4.mp3")
	for i in range(5):
		n.play()
