from TestCase import TestCase

def doQuestion(nBack) -> int:
    return int(input(f"A última nota tocada é igual à {nBack} nota?\n1 - Sim\n 2 - Não\n> "))

def testCasesInput() -> int:
    return int(input("How many test cases? "))

def nBackInput() -> int:
    return int(input("n-back: "))

def notesInput() -> int:
    return int(input("notes: "))

def createManualTestCase(id) -> TestCase:
    nBack = nBackInput()
    notes = notesInput()

    t = TestCase(id, nBack, notes)
    if t.isValidTestCase == False:
        raise Exception("notes must be higher than n-back. Insert values again. Press enter to return.\n")
    
    return t