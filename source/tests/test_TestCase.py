import pytest
import sys; import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from TestCase import NbackTestCase, TonalDiscriminationTaskTestCase, VolumeTestCase, get_note_group_from_config
import TestCase
from notes import notes

sample_note_group = notes.Note_group.get_note_group_from_note_names(['C4', 'D4', 'E4', 'F4', 'G4', 'A4', 'B4', 'C5'])

def test_get_note_group_from_config():
	assert get_note_group_from_config().notes != []

def test_TonalDiscriminationTaskTestCase():
	tdt_testCase = TonalDiscriminationTaskTestCase(0, 10)

def test_VolumeTestCase():
	volumeTestCase = VolumeTestCase(sample_note_group)

def test_TestCase():
	testCase = TestCase.TestCase(sample_note_group, 1, 10)

def test_NbackTestCase():

	def check_NbackTestCase(t:NbackTestCase, answer:TestCase.AnswerType):
		last_note = t.note_group[-1]
		nback_note = t.note_group[-2]
		t.print_notes()
		t.print_correct_answer()
		result = t.validateAnswer(answer)
		t.print_result()
		assert t.answer == answer

		if answer == t.correct_answer:
			assert result == TestCase.ResultType.CORRECT
		else:
			assert result == TestCase.ResultType.INCORRECT

		if t.correct_answer == TestCase.AnswerType.SAME:
			assert last_note == nback_note
		else:
			assert last_note != nback_note
	
	def test_NbackTestCase(t:NbackTestCase, available_semitones_notes:list):
		check_NbackTestCase(t, TestCase.AnswerType.SAME)
		check_NbackTestCase(t, TestCase.AnswerType.DIFFERENT)
		assert [note.full_name for note in t._semitone_note_list] == available_semitones_notes
		
	nback_test_case1 = NbackTestCase(sample_note_group, id_num=0, nBack=1, numberOfNotes=2, isLastNoteDifferent=True, semitones=1)
	assert len(nback_test_case1.note_group) == 2
	test_NbackTestCase(nback_test_case1, ['E4', 'B4'])
	
	nback_test_case2 = NbackTestCase(sample_note_group, id_num=0, nBack=1, numberOfNotes=2, isLastNoteDifferent=False, semitones=1)
	test_NbackTestCase(nback_test_case2, ['E4', 'F4', 'B4', 'C5'])

	nback_test_case3 = NbackTestCase(sample_note_group, id_num=0, nBack=1, numberOfNotes=2, isLastNoteDifferent=False, semitones=-1)
	test_NbackTestCase(nback_test_case3, ['E4', 'F4', 'B4', 'C5'])
	
	nback_test_case4 = NbackTestCase(sample_note_group, id_num=0, nBack=1, numberOfNotes=2, isLastNoteDifferent=True, semitones=-1)
	test_NbackTestCase(nback_test_case4, ['F4', 'C5'])


