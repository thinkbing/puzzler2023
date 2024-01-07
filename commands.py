# BASIC built-in commands
import re
from state import *

# Syntax: DATA value[,value...] (handled when reading program)
def DATA(statement, lineno):
    pass


# Function object used by DEF
class BasicFunction():
    def __init__(self, fvar, expr):
        self.fvar = fvar
        self.expr = expr
    def __call__(self, value):
        saved = variables.get(self.fvar)        # Variable may exist already
        variables[self.fvar] = value            # Set (or overwrite) value
        result = evalExpr(self.expr)
        del variables[self.fvar]
        if saved: variables[self.fvar] = saved  # Restore original value, if any
        return result

# Syntax: DEF function(variable)=expression
# Technically "function" is "FN name" but it usually seems to be written "FNNAME"
def DEF(statement, lineno):
    if not statement.startswith("FN"): syntaxError("FUNCTION NAME MUST START WITH FN")
    start = statement.find('(')
    fname = statement[0:start]
    end = statement.find(')')
    fvar = statement[start+1:end]
    start = statement.find('=')
    expr = statement[start + 1:]
    variables[fname] = BasicFunction(fvar, expr)


# List subclass that works with BASIC syntax for subscripting with parentheses
class BasicArray(list):
    def __call__(self, *args):
        if len(args) == 1:
            return self[args[0]]
        elif len(args) == 2:
            return self[args[0]][args[1]]
        else:
            syntaxError("3+ DIMENSIONAL ARRAYS NOT SUPPORTED")

# Syntax: arrayname(max[,max...]) [,...]
# The "max" parameter is the max array index, so array size = max+1
def DIM(statement, lineno):
    parts = parts = splitUnquoted('"()', ",", statement)
    for part in parts:
        variable = part[:part.find('(')] + "Ξ"
        dims = part[part.find('(')+1:-1]
        dims = dims.split(',')
        dim1 = evalExpr(dims[0])
        value = BasicArray([0]*(dim1+1))
        if len(dims) > 1:
            dim2 = evalExpr(dims[1])
            for i in range(len(value)):
                value[i] = BasicArray([0]*(dim2+1))
        if len(dims) > 2: syntaxError("3+ DIMENSIONAL ARRAYS NOT SUPPORTED")
        assignVar(variable, value)


# Syntax: no arguments
def END(statement, lineno):
    pass    # Caller will detect "END" and terminate execution loop

# Syntax: FOR var=start TO finish [STEP n]
def FOR(statement, lineno):
    parts = re.split(" |=", statement)
    if parts[2] != "TO": syntaxError("INVALID FOR LOOP: " + statement)
    variable = parts[0]
    startVal = evalExpr(parts[1])
    endVal = evalExpr(parts[3])
    step = 1
    if len(parts) == 6:
        if parts[4] != "STEP": syntaxError("INVALID FOR LOOP: " + statement)
        step = evalExpr(parts[5])
    forStack.append((nextLine(lineno), variable, startVal, endVal, step))
    assignVar(variable, startVal)

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

    i = statement.find("THEN")
    if i == -1: syntaxError("IF WITHOUT THEN")
    expr = statement[:i]
    result = evalExpr(expr)

    # If false, skip any statements from the same line
    # (i.e., go to the next whole-numbered line)
    if not result:
        return nextLine(lineno, wholeLine=True)

    # THEN will be followed by a line number (implicit GOTO) or one or more statements
    statement = statement[i + 5:]
    match = re.match("[0-9]+", statement)
    if match:
        return int(match.group())   # Jump to numbered statement
    else:
        return None     # Proceed to statement(s) following IF

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
        if part[-1] != '$':
            if '.' in val:
                val = float(val)
            else:
                val = int(val)
        assignVar(part, val)
    return None


def autoDim(arrayName, indexes):
    # Implicitly initialized arrays are treated as if they were DIM(11)
    if arrayName not in variables:      # TODO
        indexStr = ','.join(["11"]*len(indexes))
        DIM(arrayName[:-1] + "(" + indexStr + ")", None)

def assignArray(variable, value):
    # Append "Ξ" to distinguish arrays from scalars with same name
    start = variable.find('(')
    arrayName = variable[:start] + "Ξ"
    arrayExpr = variable[start + 1:-1]
    # Compute index values
    indexes = [evalExpr(part) for part in arrayExpr.split(',')]
    autoDim(arrayName, indexes)     # Create or resize array if necessary
    arrayVar = variables[arrayName]
    if len(indexes) == 1:
        arrayVar[indexes[0]] = value
    elif len(indexes) == 2:
        arrayVar[indexes[0]][indexes[1]] = value
    else:
        syntaxError("3+ DIMENSIONAL ARRAYS NOT SUPPORTED")

def assignVar(variable, value):
    variable = variable.replace("$", "Σ")
    if '(' in variable:
        # Assignment to array
        assignArray(variable, value)
    else:
        # Assignment to regular variable
        variables[variable] = value
    if trace: print(variables)

def LET(statement, lineno):
    equal = statement.find('=')
    variable = statement[:equal]
    expr = statement[equal+1:]
    value = evalExpr(expr)
    assignVar(variable, value)


# Syntax: LIST [fromline[,toline]]
# Can't be used in deferred mode
from itertools import groupby
def LIST(statement, lineno):
    if lineno: syntaxError("LIST ONLY SUPPORTED FOR IMMEDIATE MODE")
    parts = re.split("[\,\-]", statement)
    startLine = int(parts[0]) if len(statement) > 0 else -1
    endLine = int(parts[1]) if len(parts) > 1 else 999999
    for (linenum, group) in groupby(progLines, lambda v: int(v[0])):
        if linenum < startLine or linenum > endLine: continue
        print(f"{int(linenum)} ", end="")
        print(*[v[1] for v in group], sep=":")


# Syntax: LOAD filename
# Can't be used in deferred mode
def LOAD(statement, lineno):
    if lineno: syntaxError("LOAD ONLY SUPPORTED FOR IMMEDIATE MODE")
    clearProgram()
    count = 0
    with open("programs/" + statement, "r") as file:
        for line in file:
            line = line.rstrip()
            if len(line) == 0: continue
            for (linenum, statements) in parseLine(line):
                if not linenum: syntaxError("LINE NUMBER NOT FOUND: " + line)
                storeLine(linenum, statements)
            count = count + 1
    print(f"LOADED {count} LINES")

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

# Syntax: NEXT [variable][,variable...]
def NEXT(statement, lineno):
    nexts = statement.split(",") if len(statement) > 0 else [None]
    for nextVar in nexts:
        while True:
            if len(forStack) == 0: syntaxError("NEXT WITHOUT FOR")
            (loopline, variable, startVal, endVal, step) = forStack[-1]
            if nextVar is None or nextVar == variable: break
            forStack.pop()  # Can happen if we terminate an inner loop early by NEXTing the outer loop
        value = variables[variable]
        value = value + step
        done = value > endVal if step > 0 else value < endVal
        if not done:
            assignVar(variable, value)
            return loopline
        else:
            forStack.pop()
    return None


def NOTRACE(statement, lineno):
    setTrace(False)


def parsePrint(statement):
    pos = 0
    while pos < len(statement):
        c = statement[pos]
        if c in '",;' and pos > 0:
            # Emit a token if we hit a delimiter
            yield statement[:pos]
            statement = statement[pos:]
            pos = 0
        if c in ',;':
            # Emit a token for , or ; itself
            yield c
            statement = statement[pos+1:]
            pos = 0
        elif c == '"':
            # Consume to end of quoted string and emit token including " chars
            pos = pos + 1
            while pos < len(statement) and statement[pos] != '"': pos = pos + 1
            yield statement[:pos]
            statement = statement[pos+1:]
            pos = 0
        elif c == '(':
            # Skip to matching paren, ignoring delimiters within
            parens = 1
            while pos < len(statement) and parens > 0:
                pos = pos + 1
                if statement[pos] == '(': parens = parens + 1
                elif statement[pos] == ')': parens = parens - 1
        else:
            pos = pos + 1
    if len(statement) > 0: yield statement

# Syntax: PRINT ["message"|expr][;...]
# Separation by ; concatenates text without spaces (though some programs seem to assume it adds space)
# Separation by , moves to next tab stop (16 spaces per stop)
# Trailing , or ; suppresses newline
def PRINT(statement, lineno):
    length = 0
    last = None
    for part in parsePrint(statement):
        if part[0] == '"':
            text = part[1:]
        elif part == ',':
            text = ' ' * ((int(length/16)+1)*16 - length)
        elif part == ';':
            text = ""    # Some programs assume this is " "
        else:
            text = str(evalExpr(part))
        length = length + len(text)
        print(text, end="")
        last = part
    if last not in (",",";"):
        print()         # Newline, unless ending in , or ;
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

def RUN(statement, lineno):
    if lineno: syntaxError("LOAD ONLY SUPPORTED FOR IMMEDIATE MODE")
    startLine = int(statement) if len(statement) else None
    execProgram(startLine)

def TRACE(statement, lineno):
    setTrace(True)

import inspect, sys
def makeCommands():
    # Auto-generate command map from member functions in UPPERCASE
    members = inspect.getmembers(sys.modules[__name__])
    commands = {name:obj for name, obj in members if inspect.isfunction(obj) and name.upper() == name}
    return commands