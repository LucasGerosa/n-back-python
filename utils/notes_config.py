from configparser import ConfigParser


def get_setting(setting):
    config = ConfigParser()
    if config.read("settings.ini"):
        raise FileNotFoundError("The settings.ini file hasn't yet been created. If you're running the program from the source code, run notes_config.py and try again. If you're not, this is a bug, so ask the developers to fix it.")
    
    return config['custom'][setting]

def setup():
    config = ConfigParser()

    config['DEFAULT'] = {
        "Notes" : "all",
        "Note_intensity" : "mf"
    }
    config['custom'] = config["DEFAULT"]

    with open("settings.ini", "w") as f:
        config.write(f)

if __name__ == '__main__':
    setup()