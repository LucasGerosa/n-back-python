import csv
import string
import FileUtils
from enum import Enum
from typing import List
from xmlrpc.client import Boolean
import IOUtils


class ResultEnum(Enum):
    ACERTO = 1
    ERRO = 2

class TestCase:

    def __init__(self, id, nBack, numberOfNotes, instrument='piano') -> None:
        self.id: int = id
        self.nBack: int = nBack
        self.numberOfNotes: int = numberOfNotes
        self.note_group = IOUtils.getNotes(instrument=instrument, audio_folder='', create_sound=False)
        assert self.isValidTestCase(), f"numberOfNotes should be > nBack. Got numberOfNotes = {self.numberOfNotes} and nBack = {self.nBack} instead."        
        self.notesExecuted: IOUtils.Note_group = IOUtils.Note_group()
        self.result: ResultEnum = ResultEnum.ERRO
        self.bpm: int = 60

    def __str__(self):
        return f"id: {self.id}, nBack is {self.nBack}, numberOfNotes is {self.numberOfNotes}"

    def execute(self) -> None:
        self.randomizeNumbers()
        self.doQuestion()
        self.validateAnswer()

    def validateAnswer(self) -> None:
        length = len(self.notesExecuted)

        # Check if n-back note equals to last note
        lastNote: int = self.notesExecuted[length - 1]
        nBackNote: int = self.notesExecuted[length - 1 - self.nBack]

        if (lastNote == nBackNote):
            if (self.answer == 1): #what does this 1 represent?
                self.result = ResultEnum.ACERTO
            else:
                self.result = ResultEnum.ERRO
        else:
            if (self.answer == 1):
                self.result = ResultEnum.ERRO
            else:
                self.result = ResultEnum.ACERTO

    def randomizeNumbers(self) -> None:
        for _ in range(self.numberOfNotes): #by convention, _ is used for the iterator variable if it's not going to be used
            self.notesExecuted.append(IOUtils.printAndSleep(self.bpm, self.note_group)) #FIXME

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
                    [t.id, t.numberOfNotes, ' '.join(str(e) for e in t.notesExecuted), t.nBack, t.answer, t.result])
                i += 1

        f.close()

    @staticmethod
    def executeFromFile(playerName: str) -> list:
        p = FileUtils.readFromFile()
        testCaseList:List[TestCase] = p.testCaseList
        for testCase in testCaseList:
            testCase.execute()

        return testCaseList

    @staticmethod
    def executeLoop(playerName: str)  -> list:
        import ManualInputUtils
        testCaseList = []
        testCases = ManualInputUtils.testCasesInput()
        i = 0
        while i < testCases:
            while True:
                try:
                    t = ManualInputUtils.createManualTestCase(i)
                    testCaseList.append(t)
                    t.execute()
                    break
                except Exception:
                    import traceback
                    print(traceback.format_exc())

            i += 1

        TestCase.saveResults(testCaseList, playerName)

        return testCaseList
