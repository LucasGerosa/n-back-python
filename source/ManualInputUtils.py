from TestCase import TestCase

def doQuestion(nBack):
    return int(input(f"A última nota tocada é igual à {nBack} nota?\n1 - Sim\n 2 - Não\n> "))

def testCasesInput():
    return int(input("How many test cases? "))

def nBackInput():
    return int(input("n-back: "))

def notesInput():
    return int(input("notes: "))

def createManualTestCase(id) -> TestCase:
    nBack = nBackInput()
    notes = notesInput()

    t = TestCase(id, nBack, notes)
    if t.isValidTestCase == False:
        raise Exception("notes must be higher than n-back. Insert values again. Press enter to return.\n")
    
    return t