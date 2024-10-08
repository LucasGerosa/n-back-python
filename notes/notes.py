import os
import typing
import random
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

	def __init__(self, path:str, bpm:float=DEFAULT_BPM, create_sound:bool=True, note_value:float=DEFAULT_NOTE_VALUE) -> None:
		self.set_path(path) #TODO:don't allow the creation of a note with an invalid path
		self.full_name:str = self.get_full_name()
		self.name:str = self.full_name[:-1]
		self.octave:str = self.full_name[-1]
		if self.extension == 'aif':
			self.change_extension('aiff')
		if create_sound: #this will prevent sounds from being created if they are not going to be played, improving performance
			self.sound = AudioSegment.from_file(self.path, self.extension)

		self.create_sound:bool = create_sound
		self.bpm = bpm
		self.note_value = note_value
		self.intensity = self.get_intensity()
	
	def __eq__(self, other_note) -> bool:
		return self.path == other_note.path
	
	def __str__(self) -> str:
		return f"Note object '{self.fileName}.{self.extension}' at {self.directory}."
	
	def remove_silence(self) -> None: #TODO: edit the file to remove the sound, not just in runtime
		trim_leading_silence = lambda x: x[detect_leading_silence(x) :]
		#trim_trailing_silence = lambda x: trim_leading_silence(x.reverse()).reverse() #removes silence from 
		#strip_silence = lambda x: trim_trailing_silence(trim_leading_silence(x))
		#stripped = strip_silence(self.sound)
		self.sound = trim_leading_silence(self.sound)
	
	def set_path(self, new_path) -> None:
		self.path = new_path
		self.directory, fileNameExt = os.path.split(new_path) #directory won't have a trailing '/'
		self.fileName, ext = os.path.splitext(fileNameExt)
		self.extension =  ext.split('.')[1]

		instrument_dir, DEFAULT_AUDIO_EXTENSION_dir = os.path.split(self.directory)
		if DEFAULT_AUDIO_EXTENSION_dir == DEFAULT_AUDIO_EXTENSION:
			self.instrument:str = os.path.split(instrument_dir)[1]
		else:
			self.instrument:str = DEFAULT_AUDIO_EXTENSION_dir
	
	def get_full_name(self) -> str: #gets the name of the note (e.g. Gb3, D4, etc)
		name = self.fileName.split('.')[-1]
		return name
	
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
			raise Exception(f"To be implemented; notes with extensions besides mp3 can't be played. Path of note: {self.path}")
	
		if not self.create_sound:
			self.sound = AudioSegment.from_file(self.path, self.extension)
		self.remove_silence()
		t = bpmToSeconds(self.bpm)*4*self.note_value
		#current_playback = self._play_with_pyaudio(self.sound, t)
		current_playback = playback._play_with_simpleaudio(self.sound)
		
		time.sleep(bpmToSeconds(self.bpm)*4*self.note_value)
		
		current_playback.stop()
		del current_playback  # Suggest deletion of the playback object
		gc.collect()  # Explicitly suggest garbage collection
		
	def change_extension(self, new_extension:str) -> None:
		new_path = os.path.join(self.directory, self.fileName + '.' + new_extension)
		if os.path.exists(new_path):
			self.delete_file()
		else:
			os.rename(self.path, new_path)
		self.set_path(new_path)
	
	def convert(self, new_extension:str = DEFAULT_NOTE_EXTENSION, directory:str = NOTES_FOLDER, delete_old_file = False) -> None: #note: this directory should not be from the main directory of the project
		new_path = os.path.join(ROOT_DIR, '..', directory, self.instrument, self.fileName + '.' + new_extension)
		self.sound.export(new_path, format = new_extension)
		#This is equivalent to "ffmpeg -i input/notas/aiff/do.aiff input/notas/aiff/do.mp3"
		if delete_old_file:
			self.delete_file()
		self.set_path(new_path)
	
	def delete_file(self) -> None:
		os.remove(self.path)
	
	def add_semitone(self, semitones:int): #TODO: create subtraction and addition methods (__add__, __sub__)
		#makes a note with the same attributes but with X semitones of difference
		if semitones < 0:			
			name = self.name + "b" * (semitones * -1)
		elif semitones > 0: 
			name = self.name + "#" * semitones
		full_name = note_str_utils.convert_sharps_to_flats(name + self.octave)
		
		assert not note_str_utils.is_note_greater(full_name, HIGHEST_NOTE), f"Tried to increase the semitone of {self.full_name}, getting {full_name}, but {HIGHEST_NOTE} is the last possible note on the program."
		assert not note_str_utils.is_note_greater(LOWEST_NOTE, full_name), f"Tried to decrease the semitone of {self.full_name}, but {LOWEST_NOTE} is the first possible note on the program."
		print("add_semitone(): Previous note:" + self.full_name + "; Altered note:" + full_name)
		
		return get_note_from_note_name(self.intensity, full_name, self.bpm, self.create_sound, self.instrument, self.note_value)
	
	@staticmethod
	def get_greater_note(note1, note2):
		if note1 > note2:
			return note1
		return note2
			
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

	def __contains__(self, note):
		return note in self.notes
	
	def __iter__(self):
		return iter(self.notes)

	def __str__(self):
		return 'Note_group containing ' + str(self.notes)

	def __add__(self, other_note_group):
		return Note_group(self.notes + other_note_group.notes)
	
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

''' 
	For future reference for working with aiff or wav
	Audio signal parameters:
	
		Number of channels: mono or stereo
		Sample width: number of bytes for each saample
		framerate/sample_rate: E.g. 44,100 Hz standard rate for CD quality
		Number of frames
		Values of a frame
	'''

def get_note_from_note_name(intensity:str, note_name:str, bpm:float=DEFAULT_BPM, create_sound:bool=True, instrument:str='piano', note_value:float=DEFAULT_NOTE_VALUE) -> Note:
	app_path = get_app_path()
	file_name = os.path.join(app_path, NOTES_FOLDER, instrument, f"{instrument.capitalize()}.{intensity}.{note_name}.{DEFAULT_NOTE_EXTENSION}")

	return Note(file_name, bpm, create_sound, note_value=note_value)

if __name__ == '__main__':
	pass
