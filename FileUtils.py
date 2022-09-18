import csv
from re import X

from Parameter import Parameter
from TestCase import TestCase

def writeFile():
    f = open("output/result.csv", "x")

def readFromFile() -> Parameter:
    while True:
        try:
            filename = input("Give filename: ")
            f = open("input/" + filename, 'r')
            testCases = int(f.readline())

            p = Parameter()
            p.testCaseList = []

            for i in range(testCases):
                t = TestCase(i, int(f.readline()), int(f.readline()))
                print(t)
                p.testCaseList.append(t)

            return p
        except TypeError as err:
            print("Error happened when retriving filename, try again. Error: " + err)

if __name__ == "__main__":
    readFromFile("testCase1.txt")