import pytest
import sys; import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from TestCase import NbackTestCase, TonalDiscriminationTaskTestCase, VolumeTestCase, get_note_group_from_config
import TestCase
from notes import notes

sample_note_group = notes.Note_group.get_note_group_from_note_names(['C4', 'D4', 'E4', 'F4', 'G4', 'A4', 'B4'])

def test_get_note_group_from_config():
	assert get_note_group_from_config().notes != []

def test_TonalDiscriminationTaskTestCase():
	tdt_testCase = TonalDiscriminationTaskTestCase(0, 10)

def test_VolumeTestCase():
	volumeTestCase = VolumeTestCase(sample_note_group)

def test_TestCase():
	testCase = TestCase.TestCase(sample_note_group, 1, 10)

def test_NbackTestCase():
	nback_test_case = NbackTestCase(sample_note_group, 2, 1, 10)

