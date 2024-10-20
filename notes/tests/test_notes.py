import sys; import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from notes.notes import getAllNotesStr, DEFAULT_NOTE_EXTENSION

def test_getAllNotesStr():
	assert getAllNotesStr(extension=DEFAULT_NOTE_EXTENSION, audio_folder="")