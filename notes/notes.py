'''
This module provides abstraction for musical notes, allowing the user to play them and manipulate them, as well as convert and edit note files from aiff to mp3.
'''
import os
import typing
import random
import time
import sys
from pydub import AudioSegment, playback
from pydub.silence import detect_leading_silence
import glob #module for getting files that match  requirement
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

app_path = get_app_path()

def check_ffmpeg():
	  # Use the get_app_path() function we'll create in step 2
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

#remove_silence_and_save_all_notes()
#check_ffmpeg()

# def check_vlc(): 
# 	try:
# 		version = vlc.libvlc_get_version()
# 	except AttributeError:
# 		os.environ['PATH'] += os.path.join(app_path, 'vlc')
# check_vlc()

os.environ['PATH'] += ";" + os.path.join(app_path, "vlc")
# print(os.environ['PATH'])
import vlc

class Note:
	'''Represents musical notes, pointing to an mp3 file that can be played, or other audio files that can't be played.'''

	def __init__(self, path:str, bpm:float=DEFAULT_BPM, note_value:float=DEFAULT_NOTE_VALUE) -> None:
		self.path = path
		self.bpm = bpm
		self.note_value = note_value
		self.intensity = self.get_intensity()
		#self._sound:AudioSegment = AudioSegment.from_file(self.path, self.extension)
		self._sound = vlc.MediaPlayer(self.path)

	@property
	def sound(self):
		return self._sound

	@sound.deleter
	def sound(self) -> None:
		del self._sound
	
	@property
	def path(self):
		return self._path

	@path.setter
	def path(self, new_path) -> None:
		assert os.path.exists(new_path), f"Note path {new_path} does not exist."
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
		if self.extension !='mp3':
			raise NotImplementedError(f"Notes with extensions besides mp3 can't be played yet. Path of note: {self.path}")
	
		t = bpmToSeconds(self.bpm) * 4 * self.note_value
		self.sound.play()
		# current_playback = playback._play_with_simpleaudio(self.sound)
		time.sleep(t)
		self.sound.stop()
		time.sleep(0.1)
		#self.sound.stop()
		# current_playback.stop()
		
	# def change_extension(self, new_extension:str) -> None:
	# 	new_path = os.path.join(self.directory, self.fileName + '.' + new_extension)
	# 	if os.path.exists(new_path):
	# 		self.delete_file()
	# 	else:
	# 		os.rename(self.path, new_path)
	# 	self.path = new_path
	
	def convert(self, new_extension:str = DEFAULT_NOTE_EXTENSION, directory:str = NOTES_FOLDER, delete_old_file = False) -> None: #note: this directory should not be from the main directory of the project
		new_path = os.path.join(ROOT_DIR, '..', directory, self.instrument, self.fileName + '.' + new_extension)
		self.sound.export(new_path, format = new_extension)
		#This is equivalent to "ffmpeg -i input/notas/aiff/do.aiff input/notas/aiff/do.mp3"
		if delete_old_file:
			self.delete_file()
		self.path = new_path
	
	def remove_silence(self) -> AudioSegment:
		start_trim = detect_leading_silence(self.sound)
		# end_trim = detect_leading_silence(self.sound.reverse()) #removing trailing silence screws up the sound
		# trimmed_sound = self.sound[start_trim:len(self.sound)-end_trim]
		trimmed_sound = self.sound[start_trim:]
		trimmed_sound.export(self.path, format = self.extension)
		self._sound = trimmed_sound
	
	def delete_file(self) -> None:
		os.remove(self.path)
		del self
	
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
		
		return Note.get_note_from_note_full_name(full_name, self.intensity, self.bpm, self.instrument, self.note_value)
	
	def __sub__(self, semitones:int):
		return self.__add__(-semitones)

	@staticmethod
	def get_greater_note(note1, note2):
		if note1 > note2:
			return note1
		return note2

	@staticmethod
	def get_note_file_name_from_note_full_name(note_full_name:str, audio_folder:str='', intensity:str=DEFAULT_INTENSITY, instrument:str=DEFAULT_INSTRUMENT, extension=DEFAULT_NOTE_EXTENSION):
		app_path = get_app_path()
		file_name = os.path.join(app_path, NOTES_FOLDER, instrument, audio_folder, f"{instrument}.{intensity}.{note_full_name}.{extension}")
		return file_name

	@staticmethod
	def get_note_from_note_full_name(note_full_name:str, audio_folder:str='', intensity:str=DEFAULT_INTENSITY, bpm:float=DEFAULT_BPM, instrument:str=DEFAULT_INSTRUMENT, note_value:float=DEFAULT_NOTE_VALUE, extension=DEFAULT_NOTE_EXTENSION):
		file_name = Note.get_note_file_name_from_note_full_name(note_full_name, audio_folder, intensity, instrument, extension)
		return Note(file_name, bpm, note_value=note_value)
	
	@staticmethod
	def does_note_file_exist(note_full_name:str, audio_folder:str='' ,intensity:str=DEFAULT_INTENSITY, instrument:str=DEFAULT_INSTRUMENT):
		file_name = Note.get_note_file_name_from_note_full_name(note_full_name, audio_folder, intensity, instrument)
		return os.path.exists(file_name)
			
class Note_group:
	'''Container class for Note instances. This is a more memory and time efficient way of storing a sequence of notes, as duplicate notes, e.g. inputting 'C4' 100 times, will create a note_group storing 100 references to a single note object..'''

	def __init__(self, notes_str:typing.List[str]|typing.Tuple[str], intensity:str=DEFAULT_INTENSITY, bpm:float=DEFAULT_BPM, instrument:str=DEFAULT_INSTRUMENT, note_value:float=DEFAULT_NOTE_VALUE, audio_folder='', extension=DEFAULT_NOTE_EXTENSION):
		self._notes:typing.List[Note] = []
		self._notes_str:list[str] = []
		note_str_set = set(notes_str) #type:ignore
		note_set = [Note.get_note_from_note_full_name(note_str, audio_folder, intensity, bpm, instrument, note_value, extension) for note_str in note_str_set]
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
		del self._notes[index]
		del self._notes_str[index]

	def __contains__(self, note):
		return note in self.notes
	
	def __iter__(self):
		return iter(self.notes)

	def __str__(self):
		return 'Note_group containing ' + str(self.notes_str)

	def __add__(self, other_note_group):
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
				yield note
			except Exception as e:
				time_ended = time.time()
				print("\nNumber of notes played before this error: " + str(notes_played))
				print("Time elapsed: " + str(time_ended - time_started) + " seconds.\n")
				raise e
			notes_played += 1
		time_ended = time.time()
		print("Total time elapsed: " + str(time_ended - time_started) + " seconds.")
	
	#This function is not relevant for now.
	# def change_extension(self, new_extension) -> None:
	# 	for note in self.notes:
	# 		note.change_extension(new_extension)
	
	def convert(self, new_extension:str = DEFAULT_NOTE_EXTENSION, directory:str = NOTES_FOLDER, delete_old_files = False):
		for note in self.notes:
			note.convert(new_extension, directory, delete_old_files)
			yield note
	
	def remove_silence(self):
		for note in self:
			note.remove_silence()
			yield note
	
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

def getAllNotesStr(intensity=DEFAULT_INTENSITY, instrument:str = DEFAULT_INSTRUMENT, extension:str = DEFAULT_AUDIO_EXTENSION, audio_folder:str = AUDIO_FOLDER) -> list[str]:
	'''Returns all'''
	path = os.path.join(ROOT_DIR, '..', NOTES_FOLDER, instrument, audio_folder, f"*.{extension}")
	file_paths = glob.glob(path)
	note_str_list = []
	for file_path in file_paths:
		full_file_name = os.path.split(file_path)[-1]
		file_intensity = full_file_name.split('.')[1]
		if intensity == file_intensity:
			note_str_list.append(Note.get_note_attributes_from_path(file_path)[-2])
	return note_str_list

def getAllNotes(intensity=DEFAULT_INTENSITY, instrument:str = DEFAULT_INSTRUMENT, extension:str = DEFAULT_AUDIO_EXTENSION, audio_folder:str = AUDIO_FOLDER, bpm:float=DEFAULT_BPM, note_value:float=DEFAULT_NOTE_VALUE) -> Note_group:
	note_str_list = getAllNotesStr(intensity, instrument, extension, audio_folder)
	note_group = Note_group(note_str_list, intensity, bpm, instrument, note_value, audio_folder, extension)
	return note_group


if __name__ == '__main__':
	total_notes = 0
	def test_all_notes():
		global total_notes
		note_group = getAllNotes(audio_folder='', extension=DEFAULT_NOTE_EXTENSION)
		for note in note_group:
			total_notes += 1
			print("Played", note.full_name, total_notes)
	
	note = Note.get_note_from_note_full_name('C4', bpm=75)
	print(note.path)
	for i in range(99999):
		note.play()
		print(i)
	# sound = vlc.MediaPlayer(r"c:\Users\Lucas\GitHub\n-back-python\input\piano\piano.mf.C4.mp3")
	# sound.play()
	# time.sleep(60/75)