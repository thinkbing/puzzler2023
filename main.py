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
# Compound statements after THEN should only execute if true
#       Treat THEN num as "THEN GOTO num"
#       Treat THEN as "THEN:" so everything after is micronumbered
#       When THEN is false, skip to next whole-numbered line
#       Otherwise fall through to execute the micronumbered statements
#       When LISTing, replace "THEN GOTO" with just "THEN"
#   In parseLine: replace "THEN" with "THEN:"
#   Change IF logic to skip to next whole line if False (add parameter to nextLine)