from source.IOUtils import getNotes
from utils import get_aiffs_from_web
from source.notes import DEFAULT_NOTE_EXTENSION, DEFAULT_AUDIO_EXTENSION

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
            user_input = input(f'The files will now be converted. Delete aiff files after conversion? {user_input_messages.yes}/{user_input_messages.no}\n')

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

 #TODO: make it attempt to install ffmpeg based on the OS. On linux it should be pretty easy, but windows might not be possible.


if __name__ == '__main__':
    main()