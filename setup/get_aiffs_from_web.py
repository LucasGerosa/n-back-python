import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from utils.defaults import *
from dataclasses import dataclass
from notes.notes import DEFAULT_AUDIO_EXTENSION, DEFAULT_NOTE_EXTENSION
from utils.IOUtils import getNotes
'''Modified from  https://github.com/pranav7712/OFFICE_AUTOMATION'''
'''Contains utilities for downloading audio files from the web.'''
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
input_folder = f'{ROOT_DIR}/../input'

@dataclass(frozen=True)
class Instrument:
	name:str
	from_extension:str

	def get_output_file_name(self, note_intensity:str, note_full_name:str) -> str:
		return f'{self.name.capitalize()}.{note_intensity}.{note_full_name}.{self.from_extension}'
	
	def get_note_attributes_from_file_name(self, file_name:str) -> tuple:
		instrument_name, intensity, note_name = file_name.split('.')
		instrument_name = instrument_name.lower()
		return instrument_name, intensity, note_name

	def extract_url_file(self, note_intensity:str, will_download_duplicates = False) -> None:
		input_url = f'https://theremin.music.uiowa.edu/MIS{self.name}.html'
		extension = '.' + self.from_extension
		import os
		import requests
		from urllib.parse import urljoin
		from bs4 import BeautifulSoup
		import pandas as pd
		output_dir = f'{input_folder}/{self.name}/aiff'
		#If there is no such folder, the script will create one automatically
		if not os.path.exists(output_dir): 
			os.makedirs(output_dir)

		response = requests.get(input_url)
		soup = BeautifulSoup(response.text, "html.parser") 

		link_text=list()
		link_href=list()
		link_file=list()
		
		counter=0
		
		if note_intensity != user_input_messages.ALL:
			assert note_intensity in VALID_INTENSITIES, f'Invalid intensity: "{note_intensity}".'

		for link in soup.select(f"a[href$='{extension}']"):
			file_name = link['href'].split('/')[-1]
			file_path = os.path.join(output_dir, file_name)
			if 'mono' in file_path:
				continue
			
			if note_intensity != user_input_messages.ALL and note_intensity not in file_path:
				continue

			if not will_download_duplicates and os.path.exists(file_path):
				continue
			
			# with open(file_path, 'wb') as f:
			# 	f.write(requests.get(urljoin(input_url,link['href'])).content)
				
			# link_text.append(str(link.text))
			
			# link_href.append(link['href'])

			# link_file.append(link['href'].split('/')[-1])
			
			# counter+=1

			print(counter, "-Files Extracted from URL named ", file_name)
		
		print(f"All {self.name} {extension} files downloaded.")	

	def convertAudioFiles(self, convert_to = DEFAULT_NOTE_EXTENSION, delete_old_files = False) -> None: #Converts all files from aiff to mp3
		instrument_name = self.name
		convert_from = self.from_extension
		note_group = getNotes(instrument_name, extension=convert_from)
		note_group.convert(new_extension=convert_to, delete_old_files=delete_old_files)
	
piano = Instrument('piano', DEFAULT_AUDIO_EXTENSION)
guitar = Instrument('guitar', 'aif')
instruments = [piano, guitar]

def download_all(note_intensity, will_download_duplicates = False) -> None:
	for instrument in instruments: 
		instrument.extract_url_file(note_intensity=note_intensity, will_download_duplicates=will_download_duplicates)

def convertAllFiles(delete_old_files):
	for instrument in instruments:
		instrument.convertAudioFiles(delete_old_files=delete_old_files)

