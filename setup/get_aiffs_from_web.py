'''

Modified from  https://github.com/pranav7712/OFFICE_AUTOMATION

Contains utilities for downloading audio files from the web, converting these files to mp3 and removing any trailing and leading silences from them.

Thanks to the University of Iowa for providing the audio files. The files are available at https://theremin.music.uiowa.edu/

The program can work with custom audio files. Just make sure to put them in the input folder under the correct instrument folder.

'''
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from utils.defaults import *
from utils.terminal_utils import user_input_messages
from utils import general_utils
from dataclasses import dataclass
from notes.notes import DEFAULT_AUDIO_EXTENSION, DEFAULT_NOTE_EXTENSION, getAllNotes


ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
input_folder = f'{ROOT_DIR}/../input'

@dataclass(frozen=True)
class Instrument:
	'''Class for downloading instrument audio files from the web, as well as converting and editing them as needed.'''
	name:str
	from_extension:str
	ignore_file_with:tuple = ()

	def get_output_file_name(self, note_intensity:str, note_full_name:str) -> str:
		return f'{self.name.capitalize()}.{note_intensity}.{note_full_name}.{self.from_extension}'
	
	def get_note_attributes_from_file_name(self, file_name:str) -> tuple:
		instrument_name, intensity, note_name = file_name.split('.')
		instrument_name = instrument_name.lower()
		return instrument_name, intensity, note_name

	def extract_url_file(self, note_intensity:str, will_download_duplicates = False) -> None:
		input_url = f'https://theremin.music.uiowa.edu/MIS{self.name}.html'
		extension = '.' + self.from_extension
		import requests
		from urllib.parse import urljoin
		from bs4 import BeautifulSoup
		output_dir = f'{input_folder}/{self.name}/aiff'
		#If there is no such folder, the script will create one automatically
		if not os.path.exists(output_dir): 
			os.makedirs(output_dir)

		response = requests.get(input_url)
		soup = BeautifulSoup(response.text, "html.parser") 
		
		if note_intensity != user_input_messages.ALL:
			assert note_intensity in VALID_INTENSITIES, f'Invalid intensity: "{note_intensity}".'

		counter:int=0
		ignored_files:int = 0
		for link in soup.select(f"a[href$='{extension}']"):
			try:
				file_name = link['href'].split('/')[-1]
				file_no_extension, extension =  os.path.splitext(file_name)
				file_no_extension = general_utils.lower_first_letter(file_no_extension)
				if extension == '.aif':
					extension = '.aiff'
				new_file_name = file_no_extension + extension
				file_path = os.path.join(output_dir, new_file_name)

				if any(ignored_string in file_path for ignored_string in self.ignore_file_with):
					ignored_files+=1
					continue
				
				if note_intensity != user_input_messages.ALL and note_intensity not in file_path:
					ignored_files+=1
					continue

				if os.path.exists(file_path):
					print(f"Skipping download of file {file_name}. File {file_path} already exists.")
					ignored_files+=1
					continue

				if not will_download_duplicates:
					mp3_file_path = os.path.join(output_dir, '..', file_no_extension + '.mp3')
					if os.path.exists(mp3_file_path):
						print(f"Skipping download. mp3 file {mp3_file_path} already exists.")
						ignored_files+=1
						continue
				
				with open(file_path, 'wb') as f:
					f.write(requests.get(urljoin(input_url,link['href'])).content)
			
			except KeyboardInterrupt:
				print(user_input_messages.KEYBOARDINTERRUPT_MESSAGE + f'download. Just in case, {file_path} has been removed as it was not fully downloaded.')
				os.remove(file_path)

			counter+=1

			print(counter, "-Files Extracted from URL named ", file_name)
		
		print(f"All {self.name} {extension} files downloaded. {ignored_files} files were ignored because of the chosen settings.")	

	def convertAudioFiles(self, convert_to = DEFAULT_NOTE_EXTENSION, delete_old_files = False) -> None: #Converts all files from aiff to mp3
		instrument_name = self.name
		convert_from = self.from_extension
		for intensity in VALID_INTENSITIES:
			note_group = getAllNotes(intensity, instrument=instrument_name, extension=convert_from)
			for note in note_group.convert(new_extension=convert_to, delete_old_files=delete_old_files):
				print("Successfully converted", note.path)
	
	def removeSilence(self, note_extension = DEFAULT_NOTE_EXTENSION) -> None:
		for intensity in VALID_INTENSITIES:
			note_group = getAllNotes(intensity, self.name, note_extension)
			for note in note_group.remove_silence():
				print("Successfully removed silence from", note.path)
	
piano = Instrument('piano', DEFAULT_AUDIO_EXTENSION)
guitar = Instrument('guitar', 'aif', ('mono',))
instruments = [piano, guitar]

def download_all(note_intensity, will_download_duplicates = False) -> None:
	for instrument in instruments: 
		instrument.extract_url_file(note_intensity=note_intensity, will_download_duplicates=will_download_duplicates)

def convertAllFiles(delete_old_files):
	for instrument in instruments:
		instrument.convertAudioFiles(delete_old_files=delete_old_files)

def removeSilenceFromAllFiles():
	for instrument in instruments:
		instrument.removeSilence()

