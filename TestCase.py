from xmlrpc.client import Boolean
import IOUtils
import FileUtils
from enum import Enum

class ResultEnum(Enum):
    ACERTO = 1,
    ERRO = 2

class TestCase:  
    def __init__(self, id, nBack, numberOfNotes) -> None:
        self.id = id
        self.nBack = nBack
        self.numberOfNotes = numberOfNotes
        self.notesExecuted = []
        self.result = ResultEnum.ERRO
        self.bpm = 60

    def __str__(self):
        return f"id: {self.id}, nBack is {self.nBack}, numberOfNotes is {self.numberOfNotes}"
    
    id: int
    nBack: int
    numberOfNotes: int
    notesExecuted: list
    bpm: int
    answer: int
    result: ResultEnum

    def execute(self):
        self.randomizeNumbers(self.numberOfNotes)
        self.doQuestion()
        self.validaResposta()

    def validaResposta(self):
        length = len(self.notesExecuted)
        if (self.answer == self.notesExecuted[length - self.nBack]):
            self.result = ResultEnum.ACERTO
        else:
            self.result = ResultEnum.ERRO

    def randomizeNumbers(self, rounds: int):
        i: int = 0
        
        while (i < rounds):
            self.notesExecuted(IOUtils.printAndSleep())
        i += 1

    def doQuestion(self):
        while True:
            try:
                resposta = input(f"A última nota tocada é igual {self.nBack} nota?\n1 - Sim\n 2 - Não\n> ")
                self.answer = resposta
                return resposta
            except ValueError as e:
                print('Opção não encontrada. Tente novamente.')

    def isValidTestCase(self) -> Boolean:
        if self.numberOfNotes < self.nBack:
            return False
        else:
            return True

    def executeFromFile():
        p = FileUtils.readFromFile()
        testCases = len(p.testCaseList)
        testCaseList = p.testCaseList

        i = 0
        while i < len(testCaseList):
            t : TestCase = testCaseList[i]
            t.execute()
            i += 1

    def executeLoop():
        testCaseList = []
        testCases = int(input("How many test cases? "))
        i = 0
        while i < testCases:
            while True:
                try:
                    nBack = int(input("n-back: "))
                    notes = int(input("qtd notes: "))

                    t = TestCase(i, nBack, notes)
                    if t.isValidTestCase == False:
                        raise Exception("notes must be higher than n-back. Insert values again. Press enter to return.\n")
                    
                    testCaseList.append(t)
                    t.execute()
                    break
                except Exception:
                    pass

            i += 1

