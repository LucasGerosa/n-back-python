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
    return input("1 -> Start\n2 -> Import from file\n0 -> Quit\n> ")
    

def main() -> None:
    while True:
        sequence = 10
        option = home()
        if option == "debug":
            TestCase.debug()
            input("Debugging session finished.\nPress ENTER to continue.")
            return

        if not option.isnumeric() and 0 <= int(option) <= 2:
        
            raise TypeError(f"The input needs to be a number from 0 to 2. {option} was given.")
        
        while True:
            if option == '0':
                return
            info =  retrieveInfo()  
            if option == '2':
                TestCase.executeFromFile(*info)
                    
            elif option == '1':
                TestCase.executeLoop(*info)
            
            else:
                raise TypeError(f"The input needs to be a number from 0 to 2. {option} was given.")
    

if __name__ == "__main__":
    main()
                        
