import IOUtils as IOUtils
from TestCase import TestCase

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
            TestCase.executeFromFile(playerName)
            
        elif option == 1:
            TestCase.executeLoop(playerName)
                        
        


