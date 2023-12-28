from state import readProgram, execProgram, initialize
from functions import makeFunctions
from commands import makeCommands

if __name__ == '__main__':
    filename = "craps.bas"
    with open("programs/" + filename, "r") as file: program = file.read()
    initialize(makeFunctions(), makeCommands())
    readProgram(program)
    execProgram(None)


# TODOs
# Printing tweaks (newlines, ";" handling, etc.)
# Single-line loops
# Assignment to string variables P$
# Allow array var and non-array var of same name (bounce.bas)
# READ can create variables including arrays (bunny.bas)
# LET statement