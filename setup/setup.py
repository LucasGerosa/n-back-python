import get_aiffs_from_web
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from utils.defaults import *
from utils.terminal_utils import *
from notes.notes import DEFAULT_NOTE_EXTENSION, os_name
from utils import notes_config
from pydub.exceptions import CouldntDecodeError
'''Run this file once and follow the prompts for downloading and converting the audio files used by the program.'''


def download_files(instrument_name:str, note_intensity:str, will_download_duplicates = False):
	print('Downloading notes from the web. This might take a while. Press ctrl+c to cancel.')
	try:
		
		if instrument_name == user_input_messages.ALL:
			get_aiffs_from_web.download_all(note_intensity=note_intensity, will_download_duplicates=will_download_duplicates)
			return
		
		instrument_name = instrument_name.lower()
		
		for instrument in get_aiffs_from_web.instruments:
			if instrument_name == instrument.name:
				instrument.extract_url_file(note_intensity=note_intensity, will_download_duplicates = will_download_duplicates)
				return
		
		raise ValueError(f'Instrument {instrument_name} not found.')
	
	except KeyboardInterrupt:
		print(user_input_messages.KEYBOARDINTERRUPT_MESSAGE + 'download')

def main():
	print("Note: it's not recommended to stop the program before it's done downloading and converting all files. If you do so, you might need to do it all over again.\n")
	while True:
		user_input = input(f"Download files from the web?\n\n{user_input_messages.ALL} -> download all files\n(instrument_name) -> Only download files from the instrument. E.g. 'piano' or 'guitar'\n{user_input_messages.NO} -> don't download files\n\n")

		if user_input == user_input_messages.NO:
			break
		
		scroll_terminal()
		note_intensity = input(f"Download files of what intensity?\n\n{user_input_messages.ALL} -> download all files\n'pp' or 'mf' or 'ff' -> Only download files of this intensity\n{user_input_messages.SETTING} -> Only download files with the extension in the settings\n{user_input_messages.NO} -> don't download any files\n\n")
		if note_intensity == user_input_messages.NO:
			break
		
		if note_intensity == user_input_messages.SETTING:
			note_intensity = notes_config.get_setting(notes_config.NOTE_INTENSITY_SETTING)
		
		if note_intensity != user_input_messages.ALL and note_intensity not in VALID_INTENSITIES:
			print(f'Invalid intensity: "{note_intensity}".')
			continue
		
		scroll_terminal()
		user_input3 = input(f"Only download files that don't already exist as {DEFAULT_NOTE_EXTENSION} files (default: {user_input_messages.YES})? {user_input_messages.YES_or_NO}\n\n")
		will_download_duplicates = user_input3 == user_input_messages.NO
		
		if user_input == user_input_messages.ALL:
			download_files(user_input_messages.ALL, note_intensity=note_intensity, will_download_duplicates=will_download_duplicates)
			break
		
		download_files(user_input, note_intensity=note_intensity, will_download_duplicates=will_download_duplicates)
		break
	
	try:
		while True:
			user_input = input(f'The files will now be converted. Delete aiff files after conversion? {user_input_messages.YES_or_NO}\nYou can also press ctrl+c to skip conversion (cancelling could corrupt the last mp3 file attempted to be converted).\n')

			if user_input == user_input_messages.YES:
				delete_old_files = True
				break
			if user_input == user_input_messages.NO:
				delete_old_files = False
				break
			user_input_messages.print_invalid_input()

		print("Converting audio files. This might take a while; don't shut down the program. Press ctrl+c to cancel.")
		try:
			get_aiffs_from_web.convertAllFiles(delete_old_files=delete_old_files)
		except CouldntDecodeError as e:
			print(e)
			print('The file could not be decoded. This is likely because the file is corrupted or not an audio file. Please delete the file and download it again.')

	except KeyboardInterrupt:
		print(user_input_messages.KEYBOARDINTERRUPT_MESSAGE + 'conversion')
		
	else:
		print('Completed converting audio files.')
	
	print('Now all the leading and trailing silence from the files will be removed. Press ctrl+c to cancel (not recommended as it could corrupt the files).')
	try:
		get_aiffs_from_web.removeSilenceFromAllFiles()
	except KeyboardInterrupt:
			print(user_input_messages.KEYBOARDINTERRUPT_MESSAGE + 'removing silence. Run this setup again to remove silence from the remaining files, else they might not sound in sinc with the other files.')
	ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
	ffmpeg_path = f'{ROOT_DIR}/ffmpeg/bin'
	ffmpeg_in_root_dir = os.path.exists(ffmpeg_path)
	ffmpeg_in_path = os.path.normcase('ffmpeg/bin') in os.path.normcase(os.environ['PATH'])

	import shutil
	if ffmpeg_in_path or ffmpeg_in_root_dir or shutil.which('ffmpeg'):
		print("ffmpeg installed and in the correct directory.")
		return
	else:
		print('ffmpeg not found.')


if __name__ == '__main__':
	main()