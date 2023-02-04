from pydub import AudioSegment, playback #note: you might need the dependencies mentioned at https://github.com/jiaaro/pydub/blob/master/API.markdown to use pydub
import os
import typing


DEFAULT_NOTE_EXTENSION = 'mp3'
DEFAULT_AUDIO_EXTENSION = 'aiff'
NOTES_FOLDER = 'input/notas/'
AUDIO_FOLDER = 'aiff/'
#TODO: add different folders for different instruments and add functionality for that.

class Note:

    def __init__(self, path) -> None:
        self.set_path(path)
        self.sound = AudioSegment.from_file(self.path, self.extension)
    
    def __eq__(self, other_note) -> bool:
        return self.path == other_note.path
    
    def __str__(self) -> str:
        return f"Note object '{self.fileName}.{self.extension}' at {self.directory}."
    
    def set_path(self, new_path) -> None:
        self.path = new_path
        self.directory, fileNameExt = os.path.split(new_path)
        self.fileName, ext = os.path.splitext(fileNameExt)
        self.extension =  ext.split('.')[1]
    
    def play(self) -> None:
        if self.extension !='mp3': #TEMPORARY
            raise Exception(f"To be implemented; notes currently don't work with extensions besides mp3. Path of note: {self.path}")
        playback.play(self.sound)
    
    def change_extension(self, new_extension:str) -> None: #this function should only be used for debugging purposes.
        new_path = self.directory + self.fileName + '.' + new_extension
        os.rename(self.path, new_path)
        self.set_path(new_path)
    
    def convert(self, new_extension:str = DEFAULT_NOTE_EXTENSION, directory:str = NOTES_FOLDER) -> None:
        new_path = directory + self.fileName + '.' + new_extension
        self.sound.export(new_path, format = new_extension)
        #This is equivalent to "ffmpeg -i input/notas/aiff/do.aiff input/notas/aiff/do.mp3"
        self.set_path(new_path)

class Note_group:
    '''Container class for Note instances. This can be treated pretty much as a list of notes with extra methods.'''

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

    def __str__(self):
        return 'Note_group containing ' + str(self.notes)

    def __add__(self, other_note_group):
        return Note_group(self.notes + other_note_group.notes)
    
    def append(self, note):
        self.notes.append(note)

    def play(self):
        for note in self.notes:
            note.play()
    
    def change_extension(self, new_extension) -> None:
        for note in self.notes:
            note.change_extension(new_extension)
    
    def convert(self, new_extension:str = DEFAULT_NOTE_EXTENSION, directory:str = NOTES_FOLDER) -> None:
        for note in self.notes:
            note.convert(new_extension, directory)
            

''' 
	For future reference for working with aiff or wav
    Audio signal parameters:
    
        Number of channels: mono or stereo
        Sample width: number of bytes for each saample
        framerate/sample_rate: E.g. 44,100 Hz standard rate for CD quality
        Number of frames
        Values of a frame
    '''