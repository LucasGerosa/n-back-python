import IOUtils
from TestCase import TestCase
import sys; import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from utils.defaults import *
from utils import notes_config, note_str_utils

def retrieveInfo():
        name = input("Player Name:\n")
        while True:
            bpm = input(f"Bpm (default: {DEFAULT_BPM}bpm):\n")
            if bpm == "":
                bpm = DEFAULT_BPM
                break
            elif bpm.isnumeric():
                bpm = float(bpm)
                break
            print('That is not a valid bpm number. Try again.')
        
        while True:
            instrument = input(f"Instrument ({' or '.join(INSTRUMENTS)}; {DEFAULT_INSTRUMENT } is default):\n")
            if instrument == "":
                instrument = 'piano'
                break
            elif instrument in INSTRUMENTS:
                break
            print('That is not a valid instrument; try again.')
        return name, bpm, instrument

def home() -> str:
    return input("1 -> Start\n2 -> Import from file\n0 -> Quit\nsettings -> to change the settings\n> ")
    
def settings_prompt():
    setting = input(f"""
What setting do you want to alter? Current values:
{notes_config.NOTES_SETTING} = {notes_config.get_setting(notes_config.NOTES_SETTING)}
{notes_config.NOTE_INTENSITY_SETTING} = {notes_config.get_setting(notes_config.NOTE_INTENSITY_SETTING)}
""")
    new_value = input("What value do you want to alter it to?\n")
    notes_config.change_setting(setting, new_value)


def main() -> None:
    IOUtils.cls()
    while True:
        sequence = 10
        option = home()
        if option == "debug":
            TestCase.debug()
            input("Debugging session finished.\nPress ENTER to continue.")
            return
        if option == 'settings':
            settings_prompt()

        elif not (option.isnumeric() or 0 <= int(option) <= 2):
            print(f"The input needs to be a number from 0 to 2. {option} was given. Try again.\n\n")
        
        else:

            while True:
                if option == '0':
                    return
                info =  retrieveInfo()  
                if option == '2':
                    TestCase.executeFromFile(*info)
                        
                elif option == '1':
                    TestCase.executeLoop(*info)
                
                else:
                    raise TypeError(f"The input needs to be a number from 0 to 2. {option} was given.")
        

if __name__ == "__main__":
    main()
                        
