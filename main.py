from state import initialize, repl
from functions import makeFunctions
from commands import makeCommands


if __name__ == '__main__':
    initialize(makeFunctions(), makeCommands())
    repl()

# TODOs
# Printing tweaks (newlines, ";" handling, etc.)
# Allow array var and non-array var of same name (bounce.bas)
#       Store arrays with @ suffix (similar to strings) to avoid conflict
# READ can create variables including arrays (bunny.bas)
# LET statement

# Working programs:
# 3dplot.bas
# aceyducey.bas
# amazing.bas
# batnum.bas
# bunny.bas
# diamond.bas
# sinewave.bas
# tictactoe1.bas
# tictactoe2.bas - needs some print fixes, e.g. P$" "