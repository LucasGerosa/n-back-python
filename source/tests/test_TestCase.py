import pytest
import sys; import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from TestCase import NbackTestCase, TonalDiscriminationTaskTestCase, VolumeTestCase
import TestCase
from notes import notes
from utils import note_str_utils
from utils.defaults import AVAILABLE_TDT_NOTE_QUANTITIES

sample_note_list = ['C4', 'D4', 'E4', 'F4', 'G4', 'A4', 'B4', 'C5']
sample_tuple = (sample_note_list, 'mf', 1/4)


def test_TonalDiscriminationTaskTestCase():
	for i in AVAILABLE_TDT_NOTE_QUANTITIES: #TODO add the tests
		pass
	tdt_testCase = TonalDiscriminationTaskTestCase(10)
	

def test_VolumeTestCase():
	volumeTestCase = VolumeTestCase(sample_tuple)

def test_TestCase():
	testCase = TestCase.RandomTestCase(1, 10)
	notes_str = testCase.get_random_notes_str('piano')[0]
	notes_str2 = testCase.get_random_notes_str('piano', sample_tuple)[0]
	print(notes_str2)
	assert all(note_str in sample_note_list for note_str in notes_str2)

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
		assert note_str_utils.sort_notes(t._semitone_note_str_list) == available_semitones_notes
		
	nback_test_case1 = NbackTestCase(sample_tuple, id_num=0, nBack=1, numberOfNotes=2, isLastNoteDifferent=True, semitones=1)
	assert len(nback_test_case1.note_group) == 2
	test_NbackTestCase(nback_test_case1, ['E4', 'B4'])
	
	nback_test_case2 = NbackTestCase(sample_tuple, id_num=0, nBack=1, numberOfNotes=2, isLastNoteDifferent=False, semitones=1)
	test_NbackTestCase(nback_test_case2, ['E4', 'F4', 'B4', 'C5'])

	nback_test_case3 = NbackTestCase(sample_tuple, id_num=0, nBack=1, numberOfNotes=2, isLastNoteDifferent=False, semitones=-1)
	test_NbackTestCase(nback_test_case3, ['E4', 'F4', 'B4', 'C5'])
	
	nback_test_case4 = NbackTestCase(sample_tuple, id_num=0, nBack=1, numberOfNotes=2, isLastNoteDifferent=True, semitones=-1)
	test_NbackTestCase(nback_test_case4, ['F4', 'C5'])


