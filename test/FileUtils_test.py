from unittest.mock import MagicMock, Mock, patch
import source.FileUtils as FileUtils
import unittest
from unittest.mock import MagicMock

class FileUtilsUnitTest(unittest.TestCase):
    
    def test_processFile(self):
        with patch.object(FileUtils, 'retrieveFilename', return_value='testCase1.txt') as m1:
            with patch.object(FileUtils, 'getFolder', return_value='test/resources/input/') as m2:
                p = FileUtils.readFromFile()
                
                self.assertEqual(1, len(p.testCaseList))

                from source.TestCase import TestCase
                t:TestCase = p.testCaseList[0]
                self.assertEqual(1, t.nBack)
                self.assertEqual(2, t.numberOfNotes)

if __name__ == '__main__':
    unittest.main()