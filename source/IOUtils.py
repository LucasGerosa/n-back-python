import os
import random
import time
import playsound
#import fnmatch
import typing
import glob #module for gettiong files that match  requirement
from pydub import AudioSegment, playback #note: you might need the dependencies mentioned at https://github.com/jiaaro/pydub/blob/master/API.markdown to use pydub

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

class Note:

    def __init__(self, path) -> None:
        self.path = path
        self.directory, fileNameExt = os.path.split(path)
        self.fileName, ext = os.path.splitext(fileNameExt)
        self.extension =  ext.split('.')[1]
        self.sound = AudioSegment.from_file(path, self.extension)
    
    def __str__(self) -> str:
        return f"Note object '{self.fileName}.{self.extension}' at {self.directory}."
    
    def play(self) -> None:
        if self.extension !='mp3':
            raise Exception(f"To be implemented; notes currently don't work with extensions besides mp3. Path: {self.path}")
        playback.play(self.sound)

class Note_group:
    '''Container class for Note instances.'''

    def __init__(self, notes:typing.Optional[typing.List[Note]] = None):
        if notes == None:
            self.notes: typing.List[Note] = []
        else:    
            self.notes = notes #type:ignore
    
    getNotePaths = lambda self: [note.path for note in self.notes]
    ''' Equivalent to this:
    def getNotePaths(self):
        note_paths = []
        for note in self.notes:
            note_paths.append(note.path)
        return [note.path for note in self.notes]
    '''
    def __len__(self):
        return len(self.notes)
    
    def __getitem__(self, index):
        return self.notes[index]

    def __contains__(self, note):
        return note in self.notes
    
    def __iter__(self):
        return iter(self.notes)
    
    def append(self, note):
        self.notes.append(note)

    def play(self):
        for note in self.notes:
            note.play()

def getNotes(directory = '', extension = 'mp3') -> Note_group:
    #files = [file for file in os.listdir(directory) if fnmatch.fnmatch(file, '*.' + AUDIO_EXTENSION)]
    file_paths = glob.glob(f"{ROOT_DIR}/../input/notas/{directory}*.{extension}")
    noteList = [Note(path = file_path) for file_path in file_paths] #List comprehension
    note_group = Note_group(noteList)
    return note_group

def convertAudioFiles(convert_from = 'aiff', convert_to = 'mp3', directory = 'aiff/') -> None:
    ''' 
    Audio signal parameters:
    
        Number of channels: mono or stereo
        Sample width: number of bytes for each saample
        framerate/sample_rate: E.g. 44,100 Hz standard rate for CD quality
        Number of frames
        Values of a frame
    '''
    from_files = getNotes(directory=directory, extension=convert_from)

    if convert_from == 'aiff':
        ext = "aac"
    else:
        ext = convert_from
    for from_file in from_files:
        sound = AudioSegment.from_file(from_file, ext)
        playback.play(sound)
        to_file = sound.export('../input/notas')

def cls():
    clear = lambda: os.system('cls' if os.name == 'nt' else 'clear')
    clear()

def printAndSleep(bpm: int) -> Note:
    cls()
    notes = getNotes()
    number = random.randint(0, len(notes) - 1)

    # retrieve sound from id
    note = notes[number]
    note.play()
    time.sleep(bpmToSeconds(bpm=60))
    return note

def bpmToSeconds(bpm: int) -> float:
    return 60 / bpm

if __name__ == '__main__':
    convertAudioFiles()