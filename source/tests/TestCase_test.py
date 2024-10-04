import os
import unittest
from unittest import mock
from unittest.mock import MagicMock, patch

import source.ManualInputUtils as ManualInputUtils
from utils import FileUtils
from source.TestCase import ResultEnum, TestCase

PLAYER_NAME = 'playerDummy'
OUTPUT_FILENAME_PATH = f"{FileUtils.OUTPUT_DIR}/{PLAYER_NAME}/{FileUtils.RESULT_FILENAME}"
OUTPUT_DIR_PATH = f"{FileUtils.OUTPUT_DIR}/{PLAYER_NAME}"

class TestCaseUtilsTest(unittest.TestCase):
    def tearDown(self):
        if os.path.exists(OUTPUT_FILENAME_PATH):
            os.remove(OUTPUT_FILENAME_PATH)

        if os.path.exists(OUTPUT_DIR_PATH):
            os.rmdir(OUTPUT_DIR_PATH)

        self.assertFalse(os.path.exists(OUTPUT_FILENAME_PATH))
        self.assertFalse(os.path.exists(OUTPUT_DIR_PATH))

    def test_isValidTestCase_nBackLessThanNotes(self):
        t = TestCase(1, 1, 2)
        self.assertTrue(t.isValidTestCase())

    def test_isValidTestCase_nBackEqualsToNotes(self):
        t = TestCase(1, 1, 1)
        self.assertTrue(t.isValidTestCase())

    def test_isInvalidTestCase_nBackGreaterThanNotes(self):
        t = TestCase(1, 2, 1)
        self.assertFalse(t.isValidTestCase())

    # Last two notes are the same, answer was yes (1), so result should be ACERTO
    def test_validateAnswer_ACERTO_nBackEquals1_answer1(self):
        t = TestCase(1, 1, 1)
        t.notesExecuted = [1, 2, 2]
        t.answer = 1

        t.validateAnswer()
        self.assertEqual(ResultEnum.ACERTO, t.result)

    # Last two notes are the same, answer was no (2), so result should be ERRO
    def test_validateAnswer_ERRO_nBackEquals1_answer2(self):
        t = TestCase(1, 1, 1)
        t.notesExecuted = [1, 2, 2]
        t.answer = 2

        t.validateAnswer()
        self.assertEqual(ResultEnum.ERRO, t.result)

    # Last two notes are NOT the same, answer was yes (1), so result should be ERRO
    def test_validateAnswer_ERRO_nBackEquals1_answer1(self):
        t = TestCase(1, 1, 1)
        t.notesExecuted = [1, 1, 2]
        t.answer = 1

        t.validateAnswer()
        self.assertEqual(ResultEnum.ERRO, t.result)

    # Last two notes are NOT the same, answer was no (1), so result should be ACERTO
    def test_validateAnswer_ACERTO_nBackEquals1_answer2(self):
        t = TestCase(1, 1, 1)
        t.notesExecuted = [1, 1, 2]
        t.answer = 2

        t.validateAnswer()
        self.assertEqual(ResultEnum.ACERTO, t.result)

    def test_randomizeNumbers(self):
        numberOfNotes = 3
        t = TestCase(1, 1, numberOfNotes)
        t.randomizeNumbers()
        self.assertEqual(numberOfNotes, len(t.notesExecuted))

    @patch.multiple(ManualInputUtils,
                    testCasesInput=MagicMock(return_value=1),
                    nBackInput=MagicMock(return_value=1),
                    notesInput=MagicMock(return_value=1),
                    doQuestion=MagicMock(return_value=1))
    @mock.patch("source.IOUtils.printAndSleep", method='printAndSleep', side_effect=[1])
    def test_shouldExecuteLoop(self, *m1, **m2):
        testCaseList = TestCase.executeLoop(PLAYER_NAME)

        self.assertIsNotNone(testCaseList)

        t: TestCase = testCaseList[0]
        self.assertEqual(1, len(t.notesExecuted))
        self.assertEqual(ResultEnum.ACERTO, t.result)

    @patch.multiple('source.ManualInputUtils',
                    testCasesInput=MagicMock(return_value=1),
                    nBackInput=MagicMock(return_value=1),
                    notesInput=MagicMock(return_value=5),
                    doQuestion=MagicMock(return_value=1))
    @mock.patch("source.IOUtils.printAndSleep", method='printAndSleep', side_effect=[1, 3, 5, 4, 2])
    def test_shouldExecuteLoop_whenMultipleNotes(self, m1):
        testCaseList = TestCase.executeLoop(PLAYER_NAME)

        self.assertIsNotNone(testCaseList)

        t: TestCase = testCaseList[0]
        self.assertEqual(5, len(t.notesExecuted))
        self.assertEqual(ResultEnum.ERRO, t.result)


if __name__ == '__main__':
    unittest.main()
