from cgi import test
from source import IOUtils
import unittest   # The test framework

class IOUtilsTests(unittest.TestCase):
    def test_bpm_to_seconds(self):
        test_list = [(1, 60), (0.4, 150)]
        for seconds, bpm in test_list:
            print(seconds)
            print(bpm)
            with self.subTest():
                self.assertEquals(seconds, IOUtils.bpmToSeconds(bpm))

    def test_printAndSleep(self):
        number = IOUtils.printAndSleep(60)

        self.assertIsNotNone(number)
        self.assertLessEqual(number, 10) #FIXME
        self.assertGreaterEqual(number, 0)

if __name__ == '__main__':
    unittest.main()