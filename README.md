
# Tonal N-back Test

## Overview

This project is designed to do musical tests involving cognition by using musical notes. Currently, the main tests being supported are the tonal n-back test and tonal discrimination task used by Ding et al. (2018).

## Folder Structure

### `source/`

Has the main files that direct the program. Creating new tests involves new code on all 3 of them.
- `app.py`: Contains the main GUI elements and controls the flow of the program. Run this file to run the program. This file is huge, and some refactoring should be done to organize it and abstract away some clutter.
- `test_threads.py`: Coordinates the different threads of the audio and GUI.
- `TestCase.py`: Coordinates the logic of each test, as well as validating and saving user responses.

### `input/`

This folder contains the audio files used by the program.

### `output/`

This folder is where the program saves csv files, organized by folder with the participant name or ID.

### `note/`

This folder contains the abstraction for music. Including representation of notes and scales.

### `tests/`

This folder contains unit tests for the project. It is currently very outdated and not used.

### `utils/`

Contains files with some generally useful functions used by many files.

### `translations/`

Add translations to text in the app.po file and compile it with `msgfmt app.po -o app.mo`

### `setup/`

Has files for setting up this program. Ideally, this would only need to be done once, when you install a new version of the program. This setup can be done manually instead. Download the input folder from this [drive](https://drive.google.com/drive/folders/19axa31xTREufETdWL1Ecop8WFUGSBidj?usp=drive_link), or put custom audio files (follow the same naming conventions as the ones in the drive) in the correct folder with the instrument name in the input folder.

### Important files

- `app.spec` is used to generate a an executable with pyinstaller with the following command:
`pyinstaller app.spec --distpath path_to_this_project -y`

## Usage

To use this project, follow these steps:

### Source code
1. If you need to download the notes from the web automatically, run `setup/setup.py` and follow the prompts. Otherwise, download the folder with the notes of the chosen instruments and put it in the `input` folder. It should look like the following: `input/(instrument name)/(note files.mp3)`
2. Run `app.py`
3. The output files will be generated in the corresponding subfolders under `output/notas/`.

### Releases
1. (On windows) download either the msi or zip file. Then, run the nback.exe.

## Dependencies
- Python 3.10.2. Other python versions might work but have not been tested.
- All required packets are in the requirements.txt
- Run setup.py to set up any additional dependencies, or do the setup manually in the [setup](#setup) section.
- Qt6 must be installed in order for the GUI to appear.

See the other md files for installing from source.

## Known bugs
On ubuntu, for some reason, after playing audios with simpleaudio about 60 times, it gives an error saying `_simpleaudio.SimpleaudioError: Error opening PCM device. -- CODE: -111 -- MSG: Connection refused.` It doesn't matter if it's the same audio being played 60 times or 60 different audios playing one time. I imagine it's some kind of error with drivers; that after too many attempts of connection, OS blocks further connections. I don't know how to fix that issue, and it doesn't appear on windows.

## Audio files
Thanks to the University of Iowa for providing the audio files. The files are available at https://theremin.music.uiowa.edu/

The program can work with custom audio files. Just make sure to put them in the input folder under the correct instrument folder.