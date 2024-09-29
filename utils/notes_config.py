from configparser import ConfigParser
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '.'))

CUSTOM_SETTING = 'custom'
NOTES_SETTING = 'Notes'
NOTE_INTENSITY_SETTING = 'Note intensity'
DEFAULT = 'DEFAULT'
NOTE_VALUE_SETTING = 'Note duration'
LANGUAGE_SETTING = 'Language'
LEGAL_LANGUAGES = ('pt_BR', 'en')
LEGAL_NOTE_INTENSITIES = ('pp', 'mf', 'ff')

def get_notes_setting(section = CUSTOM_SETTING) -> str:
    notes_str = get_setting(NOTES_SETTING, section = section)
    return notes_str

def get_intensity_setting(section = CUSTOM_SETTING) -> str:
    intensity = get_setting(NOTE_INTENSITY_SETTING, section=section)
    return intensity

def get_setting(setting:str, section = CUSTOM_SETTING):
    config = ConfigParser()
    if not config.read("settings.ini"):
        raise FileNotFoundError("The settings.ini file hasn't yet been created. If you're running the program from the source code, run notes_config.py and try again. If you're not, this is a bug, so ask the developers to fix it.")
    if does_setting_exist(setting):
        return config[section][setting]
    raise Exception("Setting does not exist. The settings.ini file is corrupted or something is wrong with the program.")    

def change_setting(setting:str, new_value:str, create_setting = False, section = CUSTOM_SETTING) -> None:
    config = ConfigParser()
    config.read("settings.ini")
    if not config.has_option(section, setting) and not create_setting:
        raise KeyError("Setting doesn't exist. Call this function with 'create_setting=True for creating the setting.")
    
    config[section][setting] = new_value
    with open("settings.ini", "w") as f:
        config.write(f)

def does_setting_exist(setting:str, section = CUSTOM_SETTING):
    config = ConfigParser()
    config.read("settings.ini")
    return config.has_option(section, setting)

def reset_settings():
    config = ConfigParser()

    config[DEFAULT] = {
        NOTES_SETTING : "C4-C5",
        NOTE_INTENSITY_SETTING : "mf",
        NOTE_VALUE_SETTING : "1/4",
        LANGUAGE_SETTING : "pt_BR"
    }
    config[CUSTOM_SETTING] = config["DEFAULT"]
    write_config(config)
    return config[DEFAULT]

def write_config(config):
    with open("settings.ini", "w") as f:
        config.write(f)

def get_all_settings(section = CUSTOM_SETTING):
    config = ConfigParser()
    if not config.read("settings.ini"):
        raise FileNotFoundError("The settings.ini file hasn't yet been created. If you're running the program from the source code, run notes_config.py and try again. If you're not, this is a bug, so ask the developers to fix it.")
    return config[section]

if __name__ == '__main__':
    def test():
        print(get_setting(NOTES_SETTING))
        print(change_setting(NOTES_SETTING, 'A4-G5'))
        print(get_setting(NOTES_SETTING))
    reset_settings()
    #test()
    