Downloading from source
- Download the source code through the [releases](https://github.com/rbpimenta/n-back-python/releases), or, with git installed, type
```
git clone https://github.com/rbpimenta/n-back-python.git
```
in the terminal.

- Make sure you have python 3 installed by typing one the following:
```
which python
which python3
which py
```
If one command returns nothing, try the other ones. You are going to use the command that returns the path to Python for all python commands. I'll use 'python3,' but you can replace it with 'py' or 'python' if 'python3' doesn't work.

If python is not installed, install it with ```sudo apt-get install python3```.

- Then, in the terminal, change the working directory to this project's:
```cd /path/to/the/project/n-back-python```

- Create a python virtual environment ```python3 -m venv venv```
If this fails, you might need to install python3-venv before running the command: ```sudo apt install python3-venv```

- Change file permission to executable ```chmod +x venv/bin/activate```

- Activate the venv: ```source ./venv/bin/activate```. There should appear a "(venv)" at the start of the next line.

- ```sudo apt-get install -y python3-dev libasound2-dev```

- Run ```pip install -r requirements.txt``` to install all the modules used by this program.
If this fails, you might need to install pip 
```sudo apt-get install python3-pip``` and run the command again.

- ```sudo apt install ffmpeg```

- ```python3 setup.py``` and follow the prompts to install all the mp3 files.
