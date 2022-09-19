from unittest.mock import MagicMock, Mock, patch
import source.ManualInputUtils as ManualInputUtils
import unittest

from source.TestCase import TestCase

class TestCaseUtilsTest(unittest.TestCase):

    @patch.multiple('source.ManualInputUtils',
                    nBackInput=MagicMock(return_value=1),
                    notesInput=MagicMock(return_value=1))
    def test_shouldCreateManualTestCase(self, **mocks):
        t: TestCase = ManualInputUtils.createManualTestCase(1)
        self.assertIsNotNone(t)
        self.assertEqual(1, t.id)
        self.assertEqual(1, t.nBack)
        self.assertEqual(1, t.numberOfNotes)


if __name__ == '__main__':
    unittest.main()