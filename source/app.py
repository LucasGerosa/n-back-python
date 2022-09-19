from msilib.schema import Error
import random
import time
from xmlrpc.client import Boolean

import source.IOUtils as IOUtils
import source.FileUtils as FileUtils
from source.TestCase import TestCase

def retrievePlayer():
    name = input("Player Name: ")
    print(name)

def home() -> int:
    IOUtils.cls()
    return int(input("1 - Start\n2 -> Import from file\n0 -> Quit\n> "))

if __name__ == "__main__":
    sequence = 10

    option = home()

    while (option != 0):
        playerName =  retrievePlayer()  
        testCaseList = []
        if option == 2:
            TestCase.executeFromFile()
            
        elif option == 1:
            TestCase.executeLoop()
                        
        


