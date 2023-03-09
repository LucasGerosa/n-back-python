from TestCase import TestCase
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from utils.defaults import *

def doQuestion(nBack) -> int:
    while True:
        yes_or_no = input(f"A última nota tocada é igual à {nBack} nota anterior?\n1 - Sim\n 2 - Não\n> ")
        if yes_or_no == '1' or yes_or_no == '2':
            return int(yes_or_no)
        print(f"Invalid answer. Expected 1 or 2; got {yes_or_no} instead.")

def testCasesInput() -> int:
    while True:
        amount_test_cases = input("How many test cases? ")
        if amount_test_cases.isnumeric():
            return int(amount_test_cases)
        print(f"Needs to be an integer. Got '{amount_test_cases}' instead.")

def nBackInput() -> int:
    return int(input("n-back: "))

def notesInput() -> int:
    return int(input("notes: "))

def createManualTestCase(id, bpm: float=DEFAULT_BPM, instrument=DEFAULT_INSTRUMENT) -> TestCase:
    nBack = nBackInput()
    notes = notesInput()

    t = TestCase(id, nBack, notes, bpm, instrument)
    if t.isValidTestCase == False:
        raise Exception("notes must be higher than n-back. Insert values again. Press enter to return.\n")
    
    return t