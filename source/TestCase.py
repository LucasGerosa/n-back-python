import csv
import string
import FileUtils
from enum import Enum
from typing import List
from xmlrpc.client import Boolean
import IOUtils
import sys; import os
import random
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from utils.defaults import *
import notes
class ResultEnum(Enum):
    ACERTO = 1
    ERRO = 2

class TestCase:

    def __init__(self, id:int, nBack:int, numberOfNotes:int, bpm:float=DEFAULT_BPM, instrument=DEFAULT_INSTRUMENT) -> None:
        self.id: int = id
        self.nBack: int = nBack
        self.numberOfNotes: int = numberOfNotes
        self.note_group = self.get_random_notes(instrument, bpm, numberOfNotes)
        assert self.isValidTestCase(), f"numberOfNotes should be > nBack. Got numberOfNotes = {self.numberOfNotes} and nBack = {self.nBack} instead."        
        self.result: ResultEnum = ResultEnum.ERRO

    def __str__(self):
        return f"id: {self.id}, nBack is {self.nBack}, numberOfNotes is {self.numberOfNotes}"
    
    def get_random_notes(self, instrument, bpm, numberOfNotes) -> notes.Note_group:
        all_note_group = IOUtils.getNotes(instrument=instrument, audio_folder='', create_sound=False, bpm=bpm)
        random_notes_list = random.sample(all_note_group.notes, numberOfNotes)
        random_notes_group = notes.Note_group(random_notes_list)
        return random_notes_group

    def execute(self) -> None:
        self.note_group.play()
        self.doQuestion()
        self.validateAnswer()

    def validateAnswer(self) -> None:
        length = len(self.note_group)

        # Check if n-back note equals to last note
        lastNote: int = self.note_group[length - 1]
        nBackNote: int = self.note_group[length - 1 - self.nBack]

        if (lastNote == nBackNote):
            if (self.answer == 1):
                self.result = ResultEnum.ACERTO
            else:
                self.result = ResultEnum.ERRO
        else:
            if (self.answer == 1):
                self.result = ResultEnum.ERRO
            else:
                self.result = ResultEnum.ACERTO

    def doQuestion(self) -> None:
        while True:
            try:
                import ManualInputUtils
                self.answer = ManualInputUtils.doQuestion(self.nBack)
                break
            except ValueError as e:
                print('Opção não encontrada. Tente novamente./n')

    def isValidTestCase(self) -> Boolean:
        return self.numberOfNotes > self.nBack
    
    @staticmethod
    def saveResults(testCaseList:list, playerName:str) -> None:
        with FileUtils.createfile(playerName) as f:
            # create the csv writer
            writer = csv.writer(f, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
            i = 0
            writer.writerow(['id', 'numberOfNotes', 'notesExecuted', 'nBack', 'answer', 'result'])
            while i < len(testCaseList):
                t: TestCase = testCaseList[i]

                # write a row to the csv file
                writer.writerow(
                    [t.id, t.numberOfNotes, ' '.join(str(e) for e in t.note_group), t.nBack, t.answer, t.result])
                i += 1

        f.close()

    @staticmethod
    def executeFromFile(playerName:str, bpm:float=DEFAULT_BPM, instrument:str=DEFAULT_INSTRUMENT) -> list:
        p = FileUtils.readFromFile(bpm=bpm, instrument=instrument)
        testCaseList:List[TestCase] = p.testCaseList
        for testCase in testCaseList:
            testCase.execute()
        return testCaseList

    @staticmethod
    def executeLoop(playerName:str, bpm:float=DEFAULT_BPM, instrument:str=DEFAULT_INSTRUMENT) -> list:
        import ManualInputUtils
        testCaseList = []
        testCases = ManualInputUtils.testCasesInput()
        i = 0
        while i < testCases:
            while True:
                try:
                    t = ManualInputUtils.createManualTestCase(i, bpm, instrument)
                    testCaseList.append(t)
                    t.execute()
                    break
                except Exception:
                    import traceback
                    print(traceback.format_exc())
            i += 1

        TestCase.saveResults(testCaseList, playerName)

        return testCaseList
    
    @staticmethod
    def debug() -> None:
        NUMBER_OF_TESTCASES = 1
        NBACK = 4
        NUMBER_OF_NOTES = 6
        for id in range(NUMBER_OF_TESTCASES):
            try:
                testCase = TestCase(id, NBACK, NUMBER_OF_NOTES, bpm = DEFAULT_BPM, instrument=DEFAULT_INSTRUMENT)
                testCase.execute()
            except Exception:
                import traceback
                print(traceback.format_exc())
