# Program state management
import re
from bisect import insort

functions = {}
commands = {}
progLines = []
variables = {}
gosubStack = []
forStack = []
dataList = []
dataIndex = 0
trace = False


def right(text, after):
    return text[len(after):].lstrip()

def syntaxError(message):
    raise Exception("?SYNTAX ERROR: " + message)

def evalExpr(expr):

    # Replace = with == (but preserve <= and >=), and <> with !=
    expr = re.sub(r"([^<>])\=", r"\1==", expr)
    expr = expr.replace("<>", "!=")

    # Exponentiation
    expr = expr.replace("^", "**")

    # AND/OR to and/or
    expr = re.sub(r"(\W)(AND)(\W)", r"\1and\3", expr)
    expr = re.sub(r"(\W)(OR)(\W)", r"\1or\3", expr)

    # Convert variable names and functions ending in "$" to "_"
    expr = re.sub(r"([A-Z]+[0-9]*)(\$)", r"\1_", expr)

    globals = functions
    locals = variables
    try:
        result = eval(expr, globals, locals)
        return result
    except Exception as err:
        syntaxError(str(err))

def assignVar(variable, value):
    if re.match(r"[A-Z]+[0-9]*\$?\(.*\)", variable):
        # Assignment to array variable
        start = variable.find('(')
        arrayName = variable[0:start]
        arrayName = arrayName.replace("$", "_")
        arrayIndex = variable[start+1:-1]
        if arrayName not in variables: syntaxError("UNKNOWN ARRAY " + variable)
        arrayVar = variables[arrayName]
        arrayIndex = evalExpr(arrayIndex)
        arrayVar[arrayIndex] = value
    else:
        # Assignment to regular variable
        variable = variable.replace("$", "_")
        variables[variable] = value
    if trace: print(variables)

def execStatement(statement, lineno):

    if statement.startswith("REM"): return # No spaces etc. required after "REM"

    # Match variable or command
    match = re.match("[A-Z]+[0-9]*\$?", statement)
    if not match: syntaxError(statement)
    word = match.group()
    # TODO messy handling of array subscripts
    if len(statement) > len(word) and statement[len(word)] == '(':
        word = statement[0:statement.find('=')]
    remain = right(statement, word)

    if len(remain) > 0 and remain[0] == '=':
        # variable=value: assign it
        assignVar(word, evalExpr(remain[1:]))
        return None
    elif word in commands:
        # Valid command: execute it
        command = commands[word]
        return command(right(statement, word), lineno)
    else:
        # Otherwise, attempt to evaluate it
        print(evalExpr(word))


# Helpers
def lineIndex(linenum):
    return next(i for (i,l) in enumerate(progLines) if l[0] == linenum)

def nextLine(linenum, wholeLine=False):
    index = lineIndex(linenum) + 1
    while wholeLine and int(progLines[index][0]) == linenum:
        index = index + 1
    return progLines[index][0]

def splitUnquoted(delimiters, text):
    quotes = 0
    lst = list(text)
    for i in range(len(lst)):
        if lst[i] == '"': quotes = quotes+1
        if lst[i] in delimiters and quotes%2 == 1: lst[i] = '•'
    text = "".join(lst)
    parts = re.split("[" + delimiters + "]", text)
    return [part.strip().replace("•",":") for part in parts]

# Execute a series of lines from the specified index.
def execProgram(linenum):

    if not linenum: linenum = progLines[0][0]   # Default to start
    while True:

        # Find and execute current statement
        index = lineIndex(linenum)
        if index is None: syntaxError(f"UNKNOWN LINE NUMBER {linenum}")
        statement = progLines[index][1]
        if trace: print(f"{linenum} {statement}")
        nextLinenum = execStatement(statement, linenum)

        # If statement returns a new line number, jump to it
        # Otherwise proceed to next line in order
        if nextLinenum:
            if trace: print(f"Jumping to {nextLinenum}")
            linenum = nextLinenum
        else:
            if index == len(progLines)-1: break     # Fall off end
            if statement == "END": break            # Or hit "END"
            linenum = progLines[index+1][0]


def initialize(fns, cmds):
    global functions, commands
    functions = fns
    commands = cmds


def clearProgram():
    progLines = []
    variables = {}
    gosubStack = []
    forStack = []
    dataList = []
    dataIndex = 0


def parseLine(line):

    # Parse line number, if any
    linenum = None
    match = re.match("[0-9]+", line)
    if match:
        linenum = int(match.group())
        line = right(line, match.group())

    # Parse statements, assigning fractional line number for multi-statement lines
    if ':' not in line: return [(linenum, line)]
    if line.startswith("IF"): line = line.replace("THEN", "THEN:")
    statements = splitUnquoted(":", line)
    return [(linenum + 0.1*i, s) for (i,s) in enumerate(statements)]


def storeLine(linenum, statement):

    # Remove existing line and pseudo-lines, if any
    existing = [i for (i,l) in enumerate(progLines) if int(l[0]) == linenum]
    for i in reversed(existing): del progLines[i]

    # Insert in order
    insort(progLines, (linenum, statement))

    # Add DATA elements immediately
    if statement.startswith("DATA"):
        data = statement[4:].strip()
        parts = data.split(",")
        for part in parts:
            if len(part) == 0: continue
            if part[0] == '"':
                dataList.append(part[1:-1])
            elif '.' in part:
                dataList.append(float(part))
            else:
                dataList.append(int(part))


def repl():
    while True:
        line = input()
        try:
            statements = parseLine(line)
            for (linenum, statement) in statements:
                if linenum:
                    storeLine(linenum, statement)
                else:
                    execStatement(statement, linenum)
        except Exception as exc:
            print(exc)