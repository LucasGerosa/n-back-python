from configparser import ConfigParser
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '.'))
import note_str_utils

CUSTOM_SETTING = 'custom'
NOTES_SETTING = 'Notes'
NOTE_INTENSITY_SETTING = 'Note_intensity'

def get_setting(setting:str) -> str:
    config = ConfigParser()
    if not config.read("settings.ini"):
        raise FileNotFoundError("The settings.ini file hasn't yet been created. If you're running the program from the source code, run notes_config.py and try again. If you're not, this is a bug, so ask the developers to fix it.")
    
    return config[CUSTOM_SETTING][setting]

def change_setting(setting:str, new_value:str) -> None:
    config = ConfigParser()
    config.read("settings.ini")
    config[CUSTOM_SETTING][setting] = new_value
    with open("settings.ini", "w") as f:
        config.write(f)

def setup() -> None:
    config = ConfigParser()

    config['DEFAULT'] = {
        NOTES_SETTING : "all",
        NOTE_INTENSITY_SETTING : "mf"
    }
    config[CUSTOM_SETTING] = config["DEFAULT"]

    with open("settings.ini", "w") as f:
        config.write(f)

def test():
    print(get_setting(NOTES_SETTING))
    print(change_setting(NOTES_SETTING, 'A4-G5'))
    print(get_setting(NOTES_SETTING))

if __name__ == '__main__':
    setup()
    test()
    