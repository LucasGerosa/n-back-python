import IOUtils
from TestCase import TestCase
import sys; import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from utils.defaults import *

def retrieveInfo():
        name = input("Player Name:\n")
        while True:
            bpm = input(f"Bpm (default: {DEFAULT_BPM}bpm):\n")
            if bpm == "":
                bpm = DEFAULT_BPM
                break
            elif bpm.isnumeric():
                bpm = float(bpm)
                break
            print('That is not a valid bpm number. Try again.')
        
        while True:
            instrument = input(f"Instrument ({' or '.join(INSTRUMENTS)}; {DEFAULT_INSTRUMENT } is default):\n")
            if instrument == "":
                instrument = 'piano'
                break
            elif instrument in INSTRUMENTS:
                break
            print('That is not a valid instrument; try again.')
        return name, bpm, instrument

def home() -> str:
    IOUtils.cls()
    userInput = input("1 -> Start\n2 -> Import from file\n0 -> Quit\n> ")
    if userInput.isnumeric() and 0 <= int(userInput) <= 2:
        return userInput
        
    else:
        raise TypeError(f"The input needs to be a number from 0 to 2. {userInput} was given.")

if __name__ == "__main__":
    sequence = 10
    option = home()

    while (option != '0'):
        info =  retrieveInfo()  
        if option == '2':
            TestCase.executeFromFile(*info)
                
        elif option == '1':
            TestCase.executeLoop(*info)
                        
        


