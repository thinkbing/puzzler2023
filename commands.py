# BASIC built-in commands
import re
from state import *

# Syntax: DATA value[,value...] (handled when reading program)
def DATA(statement, lineno):
    pass

# List subclass that works with BASIC syntax for subscripting with parentheses
class BasicArray(list):
    def __call__(self, value): return self[value]

# Syntax: arrayname[size[,size...]]
def DIM(statement, lineno):
    parts = re.split(",", statement)
    for part in parts:
        variable = part[0:part.find('(')]
        size = int(part[part.find('(')+1:-1]) + 1   # TODO not sure about that +1...
        value = [0]*size
        assignVar(variable, BasicArray(value))
    # TODO if len(parts) > 2: syntaxError("MULTI-DIMENSIONAL ARRAYS NOT SUPPORTED")

# Syntax: no arguments
def END(statement, lineno):
    exit(0)     # TODO throw exception to return to REPL

# Syntax: FOR var=start TO finish [STEP n]
def FOR(statement, lineno):
    parts = re.split(" |=", statement)
    if parts[2] != "TO": syntaxError("INVALID FOR LOOP: " + statement)
    variable = parts[0]
    min = evalExpr(parts[1])
    max = evalExpr(parts[3])
    step = 1
    if len(parts) == 6:
        if parts[4] != "STEP": syntaxError("INVALID FOR LOOP: " + statement)
        step = evalExpr(parts[5])
    forStack.append((nextLine(lineno), variable, min, max, step))
    assignVar(variable, min)

# Syntax: GOSUB lineno
def GOSUB(statement, lineno):
    gosubStack.append(nextLine(lineno))
    return GOTO(statement, lineno)

# Syntax: GOTO lineno
def GOTO(statement, lineno):
    # Line number validity will be checked when returned
    return int(statement)

# Syntax: IF expr THEN [lineno | statement]
def IF(statement, lineno):
    i = statement.find("THEN");
    if i == -1: syntaxError("IF WITHOUT THEN")
    expr = statement[:i-1]
    result = evalExpr(expr)
    if not result: return None
    statement = statement[i + 5:]
    match = re.match("[0-9]+", statement)
    if match:
        return int(match.group())
    else:
        return execStatement(statement)

# Syntax: INPUT ["message";]var[,...]]
def INPUT(statement, lineno):
    if statement[0] == "\"":
        i = statement.rfind(";")
        if i == -1: syntaxError("NO INPUT VARIABLE(S) FOUND")
        print(statement[1:i-1], end=None)
        statement = statement[i+1:]
    parts = statement.split(",")
    for part in parts:
        val = input()
        if part[-1] != '$': val = int(val)  # TODO could be float
        assignVar(part, val)
    return None

# Syntax: ON variable GOTO lineno[,lineno,...]
# Variable is one-based
def ON(statement, lineno):
    parts = re.split(" |,", statement)
    if not parts[1] == "GOTO": syntaxError("INCORRECT ON...GOTO SYNTAX")
    variable = parts[0]
    value = evalExpr(variable)
    parts = parts[2:]
    if value <= 0 or value > len(parts): return None # Don't GOTO anywhere
    return int(parts[value-1])

# Syntax: NEXT [variable]
def NEXT(statement, lineno):

    while True:
        if len(forStack) == 0: syntaxError("NEXT WITHOUT FOR")
        (loopline, variable, min, max, step) = forStack[-1]
        if len(statement) == 0 or statement == variable: break
        forStack.pop() # Technically not supposed to have unterminated loops, but programs use them

    value = variables[variable]
    value = value + step
    if value <= max:
        assignVar(variable, value)
        return loopline
    else:
        forStack.pop()
        return None

# Syntax: PRINT ["message"|expr][;...]
def PRINT(statement, lineno):
    parts = statement.split(";")
    for (i,part) in enumerate(parts):
        if len(part) == 0:
            pass
        elif part.startswith("\""):
            parts[i] = part[1:-1]
        else:
            parts[i] = evalExpr(part)
    ending = "" if len(statement) > 0 and statement[-1] == ';' else None
    print(*parts, end=ending)
    return None

def READ(statement, lineno):
    global dataIndex
    parts = statement.split(',')
    for part in parts:
        if dataIndex >= len(dataList): syntaxError("OUT OF DATA ERROR")
        value = dataList[dataIndex]
        assignVar(part.strip(), value)
        dataIndex = dataIndex + 1

def REM(statement, lineno):
    pass

def RESTORE(statement, lineno):
    global dataIndex
    dataIndex = 0

def RETURN(statement, lineno):
    if len(gosubStack) == 0: syntaxError("RETURN WITHOUT GOSUB")
    frame = gosubStack.pop()
    return frame

def makeCommands():
    return {
        "DATA": DATA,
        "DIM": DIM,
        "END": END,
        "FOR": FOR,
        "GOSUB": GOSUB,
        "GOTO": GOTO,
        "IF": IF,
        "INPUT": INPUT,
        "NEXT": NEXT,
        "ON": ON,
        "PRINT": PRINT,
        "READ": READ,
        "REM": REM,
        "RESTORE": RESTORE,
        "RETURN": RETURN
    }