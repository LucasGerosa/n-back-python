import IOUtils
from TestCase import TestCase

def retrievePlayer() -> str:
    name = input("Player Name: ")
    return name

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
        playerName =  retrievePlayer()  
        if option == '2':
            TestCase.executeFromFile(playerName)
            
        elif option == '1':
            TestCase.executeLoop(playerName)
                        
        


