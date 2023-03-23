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
from utils import notes_config, note_str_utils
import notes
import numpy as np
from fractions import Fraction

class ResultEnum(Enum):
    ACERTO = 1
    ERRO = 2

def get_note_group_from_config(bpm=DEFAULT_BPM, instrument=DEFAULT_INSTRUMENT) -> notes.Note_group:
    setting_not_exist_msg = "Setting does not exist. The settings.ini file is corrupted or something is wrong with the program."
    note_value_str = notes_config.get_setting(notes_config.NOTE_VALUE_SETTING)
    try:
        note_value = float(Fraction(note_value_str))
    
    except ValueError:
        raise ValueError(f"The setting '{notes_config.NOTE_VALUE_SETTING}' needs to be a number. Got {note_value_str} instead. Reset your settings or contact the developers.")
    
    intensity = notes_config.get_intensity_setting()
    if intensity == None:
        raise Exception(setting_not_exist_msg)
    note_str = notes_config.get_notes_setting()
    if note_str == notes_config.get_notes_setting(notes_config.DEFAULT):
        note_group = IOUtils.getNotes(intensity=intensity, instrument=instrument, audio_folder='', create_sound=False, bpm=bpm, note_value=note_value)
        return note_group
    elif note_str == None:
        raise Exception(setting_not_exist_msg)
    note_str_list = note_str_utils.get_final_list_notes(note_str)
    note_list = [notes.get_note_from_note_name(intensity, note_str, note_value=note_value) for note_str in note_str_list]
    return notes.Note_group(note_list)
class TestCase:

    def __init__(self, id:int, nBack:int, numberOfNotes:int, bpm:float=DEFAULT_BPM, instrument=DEFAULT_INSTRUMENT) -> None:
        self.id: int = id
        self.nBack: int = nBack
        self.numberOfNotes: int = numberOfNotes
        self.note_group = self.get_random_notes(bpm, instrument, numberOfNotes)
        assert self.isValidTestCase(), f"numberOfNotes should be > nBack. Got numberOfNotes = {self.numberOfNotes} and nBack = {self.nBack} instead."        
        self.result: ResultEnum = ResultEnum.ERRO

    def __str__(self):
        return f"id: {self.id}, nBack is {self.nBack}, numberOfNotes is {self.numberOfNotes}"
    
    def get_random_notes(self, bpm:float, instrument:str, numberOfNotes:int) -> notes.Note_group:
        note_group = get_note_group_from_config(bpm=bpm, instrument=instrument)
        random_notes_list = np.random.choice(note_group.notes, numberOfNotes)
        random_notes_group = notes.Note_group(random_notes_list)
        return random_notes_group

    def execute(self) -> None:
        self.note_group.play()
        self.doQuestion()
        self.validateAnswer()

    def validateAnswer(self) -> None:
        # Check if n-back note equals to last note
        lastNote: int = self.note_group[-1]
        nBackNote: int = self.note_group[-1 - self.nBack]

        if lastNote == nBackNote:
            if self.answer == 1:
                self.result = ResultEnum.ACERTO
            elif self.answer == 2:
                self.result = ResultEnum.ERRO
            else:
                raise Exception("Unexpected value caused by bad handling of unexpected values. Ask the developers to fix this.")
        else:
            if self.answer == 1:
                self.result = ResultEnum.ERRO
            elif self.answer == 2:
                self.result = ResultEnum.ACERTO
            else:
                raise Exception("Unexpected value caused by bad handling of unexpected values. Ask the developers to fix this.")

    def doQuestion(self) -> None:
        while True:
            try:
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
                    [t.id, t.numberOfNotes, ' '.join(note.name for note in t.note_group), t.nBack, t.answer, t.result])
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
        try:
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
        except KeyboardInterrupt:
            print("Ctrl+c was pressed. Stopping now.")
    
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

import ManualInputUtils