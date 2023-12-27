from state import readProgram, execProgram, initialize
from functions import makeFunctions
from commands import makeCommands

if __name__ == '__main__':
    filename = "batnum.bas"
    with open("programs/" + filename, "r") as file: program = file.read()
    initialize(makeFunctions(), makeCommands())
    readProgram(program)
    execProgram(0)
