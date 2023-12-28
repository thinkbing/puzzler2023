from state import initialize, repl
from functions import makeFunctions
from commands import makeCommands


if __name__ == '__main__':
    initialize(makeFunctions(), makeCommands())
    repl()

# TODOs
# Printing tweaks (newlines, ";" handling, etc.)
# Single-line loops
# Assignment to string variables P$
# Allow array var and non-array var of same name (bounce.bas)
# READ can create variables including arrays (bunny.bas)
# LET statement