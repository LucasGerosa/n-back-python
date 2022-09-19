import csv
from re import X

from source.Parameter import Parameter

def writeFile():
    f = open("output/result.csv", "x")

def getFolder():
    return "input/"

def retrieveFilename():
    return input("Give filename: ")

def readFromFile() -> Parameter:
    while True:
        try:
            filename = retrieveFilename()
            f = open(getFolder() + filename, 'r')
            testCases = int(f.readline())

            p = Parameter()
            p.testCaseList = []

            for i in range(testCases):
                from source.TestCase import TestCase
                t = TestCase(i, int(f.readline()), int(f.readline()))
                print(t)
                p.testCaseList.append(t)

            return p
        except TypeError as err:
            print("Error happened when retriving filename, try again. Error: " + err)

if __name__ == "__main__":
    readFromFile("testCase1.txt")