
# Tonal N-back Test

## Overview

This project is designed to do musical tests involving cognition by using musical notes. Currently, the main tests being supported are the tonal n-back test and tonal discrimination task used by Ding et al. (2018). Theck the LICENSE file for information on copyright.

## Usage

To use this project, follow these steps:

### Releases
1. (On windows) download either the msi or zip file. Then, run the nback.exe.

### Running from source code
1. If you need to download the notes from the web automatically, run `setup/setup.py` and follow the prompts. Otherwise, download the folder with the notes of the chosen instruments and put it in the `input` folder. It should look like the following: `input/(instrument name)/(note files.mp3)`
2. Run `app.py`
3. The output files will be generated in the corresponding subfolders under `output/notas/`.

See the `install_linux.md` file for more help installing on linux.

## Dependencies
- Python 3.10.2. Other python versions might work but have not been tested.
- All required packets are in the requirements.txt
- Run `setup.py` to set up any additional dependencies, or do the setup manually in the [setup](#setup) section.
- Qt6 must be installed in order for the GUI to appear.

See the other md files for installing from source.

## Folder Structure

### `source/`

Has the main files that direct the program. They coordinate not only the GUI, but manage the note objects (see next folder) for use in the tests. They also validate and save the user responses.

### `note/`

This folder contains the abstraction for music. Including representation of notes and scales.

### `utils/`

Contains files with some generally useful functions used by many files. Files from this folder are generally not specific to this project and could be used for other projects.

### `tests/`

In the above folders, there will be a `tests` folder containing unit test files for the main files. Run `pytest` at the project directory to run all the unit tests.

### `input/`

This folder contains the audio files used by the program.

### `output/`

This folder is where the program saves csv files, organized by folder with the participant name or ID.


### `translations/`

Add translations to text in the app.po file and compile it with `msgfmt app.po -o app.mo`

### `setup/`

Has files for setting up this program. Ideally, this would only need to be done once, when you install a new version of the program. This setup can be done manually instead. Download the input folder from this [drive](https://drive.google.com/drive/folders/19axa31xTREufETdWL1Ecop8WFUGSBidj?usp=drive_link), or put custom audio files (follow the same naming conventions as the ones in the drive) in the correct folder with the instrument name in the input folder.

### Other files

- `app.spec` is used to generate a an executable with pyinstaller with the following command:
`pyinstaller app.spec --distpath path_to_this_project -y`
- `Nback.aip`: contains the settings used for generating an msi file for a nicer installation.
- `settings.ini`: settings used for the tests of the program. These can be modified through the GUI.

## Known bugs
Check the [issues](https://github.com/LucasGerosa/n-back-python/issues) on github.

## Audio files
Thanks to the University of Iowa for providing the audio files. The files are available at https://theremin.music.uiowa.edu/

The program can work with custom audio files. Just make sure to put them in the input folder under the correct instrument folder, and make sure they're named correctly.