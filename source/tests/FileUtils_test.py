import os
import unittest
from unittest.mock import patch
from utils import FileUtils


class FileUtilsUnitTest(unittest.TestCase):

    def test_createOutputDirectory(self):
        FileUtils.createOutputDirectoryIfNotExist()
        self.assertTrue(os.path.exists(FileUtils.OUTPUT_DIR))

    def test_createPlayerDirectory(self):
        FileUtils.createPlayerDirectoryIfNotExist('playerDummy')
        self.assertTrue(os.path.exists(f"{FileUtils.OUTPUT_DIR}/playerDummy"))
        os.rmdir(f"{FileUtils.OUTPUT_DIR}/playerDummy")

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