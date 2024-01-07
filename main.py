from state import initialize, repl
from functions import makeFunctions
from commands import makeCommands


if __name__ == '__main__':
    initialize(makeFunctions(), makeCommands())
    repl()

# TODOs
# Auto initialization of variables to zero
# READ can create variables including arrays (bunny.bas)

# Working programs:
# 3dplot.bas
# aceyducey.bas
# amazing.bas
# basketball.bas
# batnum.bas
# bunny.bas
# diamond.bas
# sinewave.bas
# tictactoe1.bas
# tictactoe2.bas - needs some print fixes, e.g. P$" "

# Array assignment fails for expression 'C(F(R,C))=something'