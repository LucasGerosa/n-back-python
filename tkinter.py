import random
import subprocess
import time
import os

def cls():
    os.system('cls' if os.name=='nt' else 'clear')

def main():
    print("Hello World!")

def retrievePlayer():
    name = input("Player Name: ")
    print(name)

def randomizeNumbers(rounds: int):
    i: int = 0
    numbers = []
    while (i < rounds):
        numbers.append(printAndSleep())
        i += 1
    
def printAndSleep() -> int:
    cls()
    number = print(random.randint(0, 10))
    time.sleep(5)

def home() -> int:
    cls()
    return int(input("1 - Start\n0 -> Quit\n> "))

if __name__ == "__main__":
    sequence = 10

    while (home() == 1):
        playerName =  retrievePlayer()
        numberOfRounds: int = int(input("How many rounds? "))
        nBack = int(input("n-back: "))

        if (numberOfRounds < nBack):
            input("numberOfRounds must be higher than n-back. Press enter to return.")
            continue

        numbers = randomizeNumbers(10)

        for r in range(numberOfRounds):
            input("n-back of number")



