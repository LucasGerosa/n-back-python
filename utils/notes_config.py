from configparser import ConfigParser
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '.'))
import note_str_utils

CUSTOM_SETTING = 'custom'
NOTES_SETTING = 'Notes'
NOTE_INTENSITY_SETTING = 'Note_intensity'

def get_setting(setting:str):
    config = ConfigParser()
    if not config.read("settings.ini"):
        raise FileNotFoundError("The settings.ini file hasn't yet been created. If you're running the program from the source code, run notes_config.py and try again. If you're not, this is a bug, so ask the developers to fix it.")
    if does_setting_exist(setting):
        return config[CUSTOM_SETTING][setting]

def change_setting(setting:str, new_value:str, create_setting = False) -> None:
    config = ConfigParser()
    config.read("settings.ini")
    if not config.has_option(CUSTOM_SETTING, setting) and not create_setting:
        raise KeyError("Setting doesn't exist. Call this function with 'create_setting=True for creating the setting.")
    
    config[CUSTOM_SETTING][setting] = new_value
    with open("settings.ini", "w") as f:
        config.write(f)

def does_setting_exist(setting:str):
    config = ConfigParser()
    config.read("settings.ini")
    return config.has_option(CUSTOM_SETTING, setting)

def reset_settings() -> None:
    config = ConfigParser()

    config['DEFAULT'] = {
        NOTES_SETTING : "all",
        NOTE_INTENSITY_SETTING : "mf"
    }
    config[CUSTOM_SETTING] = config["DEFAULT"]
    write_config(config)
    
def write_config(config):
    with open("settings.ini", "w") as f:
        config.write(f)


def test():
    print(get_setting(NOTES_SETTING))
    print(change_setting(NOTES_SETTING, 'A4-G5'))
    print(get_setting(NOTES_SETTING))

if __name__ == '__main__':
    reset_settings()
    #test()
    