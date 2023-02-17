from source.IOUtils import getNotes
from utils import get_aiffs_from_web
from source.notes import DEFAULT_NOTE_EXTENSION, DEFAULT_AUDIO_EXTENSION
import os
import sys

class user_input_messages:
    yes = 'y'
    no = 'n'
    KeyboardInterrupt_message = 'Ctrl+c pressed. Canceling '
    @staticmethod
    def print_invalid_input():
        print('That is not a valid input. Try again.')

def convertAudioFiles(instrument='piano', convert_from = DEFAULT_AUDIO_EXTENSION, convert_to = DEFAULT_NOTE_EXTENSION, delete_old_files = False) -> None: #Converts all files from aiff to mp3
    note_group = getNotes(instrument, extension=convert_from)
    note_group.convert(new_extension=convert_to, delete_old_files=delete_old_files)

def convertAllFiles(delete_old_files):
    convertAudioFiles('piano', delete_old_files=delete_old_files)
    convertAudioFiles('guitar', 'aif', delete_old_files=delete_old_files)

def download_files(flag):
    print('Downloading notes from the web. This might take a while. Press ctrl+c to cancel.')
    try:
        if flag == 'all':
            get_aiffs_from_web.download_all()
            return
        
        if flag == 'guitar':
            get_aiffs_from_web.extract_url_from_instrument(flag, 'aif')
            return
        
        get_aiffs_from_web.extract_url_from_instrument(flag)
    
    except KeyboardInterrupt:
        print(user_input_messages.KeyboardInterrupt_message + 'download')

def main():
    print("Note: it's not recommended to stop the program before it's done downloading and converting all files. If you do so, you might need to do it all over again.\n")
    while True:
        user_input = input(f"Download files from the web? \n\nall -> download all files\n(instrument_name) -> Only download files from the instrument. E.g. 'piano' or 'guitar'\n{user_input_messages.no} -> don't download files\n")
        if user_input == 'all':
            download_files('all')
            break
        
        elif user_input == user_input_messages.no:
            break
        
        else:
            download_files(user_input)

    try:
        while True:
            user_input = input(f'The files will now be converted. Delete aiff files after conversion? {user_input_messages.yes}/{user_input_messages.no}\nYou can also press ctrl+c to skip conversion.')

            if user_input == user_input_messages.yes:
                delete_old_files = True
                break
            elif user_input == user_input_messages.no:
                delete_old_files = False
                break
            else:
                user_input_messages.print_invalid_input()
        print("Converting audio files. This might take a while; don't shut down the program")

        convertAllFiles(delete_old_files=delete_old_files)
    except KeyboardInterrupt:
        print(user_input_messages.KeyboardInterrupt_message + 'conversion')
    else:
        print('Completed converting audio files.')
    
    ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
    ffmpeg_path = f'{ROOT_DIR}/ffmpeg/bin'
    ffmpeg_in_root_dir = os.path.exists(ffmpeg_path)
    ffmpeg_in_path = os.path.normcase('ffmpeg/bin') in os.path.normcase(os.environ['PATH'])

    if ffmpeg_in_path or ffmpeg_in_root_dir:
        print("ffmpeg installed and in the correct directory.")
        return
    
    import requests
    import platform
    if platform.system() == 'Windows':
        requests.get('https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip')
        raise WindowsError('ffmpeg not installed or not in the required directories. After installation it should be put in either the environment variables or in the root directory of this project.')
    
    elif platform.system() == 'Linux':
        import webbrowser
        webbrowser.open("http://www.ffmpeg.org/download.html#build-linux")
    
    elif platform.system() == 'Darwin':
        requests.get("https://evermeet.cx/ffmpeg/ffmpeg-109856-gf8d6d0fbf1.zip")
    
    else:
        raise Exception('Invalid OS.')
            

 #TODO: make it attempt to install ffmpeg based on the OS. On linux it should be pretty easy, but windows might not be possible.


if __name__ == '__main__':
    main()