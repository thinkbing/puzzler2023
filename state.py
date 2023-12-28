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
    return text[len(after) + 1:].lstrip()

def syntaxError(message):
    print("?SYNTAX ERROR: " + message)
    exit(-1)    # TODO throw exception instead

def evalExpr(expr):

    # Hacks to change "=" to "==" and "<>" to "!="
    expr = expr.replace(">=", ">>")
    expr = expr.replace("<=", "<<")
    expr = expr.replace("=",  "==")
    expr = expr.replace(">>", ">=")
    expr = expr.replace("<<", "<=")
    expr = expr.replace("<>", "!=")

    # Exponentiation
    expr = expr.replace("^", "**")

    # Convert variable names and functions ending in "$" to "_"
    expr = re.sub(r"([A-Z]+)(\$)", r"\1_", expr)

    globals = functions
    locals = variables
    try:
        result = eval(expr, globals, locals)
        return result
    except NameError as err:
        syntaxError(str(err))

def assignVar(variable, value):
    if re.match(r"[A-Z}+[0-9]*\(.*\)", variable):
        start = variable.find('(')
        arrayName = variable[0:start]
        arrayName = arrayName.replace("$", "_")
        arrayIndex = variable[start+1:-1]
        if arrayName not in variables: syntaxError("UNKNOWN ARRAY " + variable)
        arrayVar = variables[arrayName]
        arrayIndex = evalExpr(arrayIndex)
        arrayVar[arrayIndex] = value
    else:
        variable = variable.replace("$", "_")
        variables[variable] = value
    if trace: print(variables)

def execStatement(statement, lineno):

    if statement.startswith("REM"): return # No spaces etc. required after "REM"

    # Match variable or command
    match = re.match("[A-Z]+[0-9]*\$?", statement)
    if not match:
        syntaxError(statement)
    word = match.group()
    if len(statement) > len(word) and statement[len(word)] == '(':
        word = statement[0:statement.find('=')]
    remain = right(statement, word)

    if len(remain) > 0 and statement[len(word)] == '=':
        assignVar(word, evalExpr(remain))
        return None

    if word in commands:
        command = commands[word]
        return command(right(statement, word), lineno)
    else:
        syntaxError("COMMAND NOT FOUND: " + word)

def splitStatements(line):
    if not ':' in line: return [line]
    quote = False
    start = 0
    statements = []
    for (i,c) in enumerate(line):
        if c == '"': quote = not quote
        if c == ':' and not quote:
            statements.append(line[start:i].strip())
            start = i+1
    if start < len(line):
        statements.append(line[start:].strip())
    return statements

def lineIndex(linenum):
    return next(i for (i,l) in enumerate(progLines) if l[0] == linenum)

def nextLine(linenum):
    index = lineIndex(linenum)
    return progLines[index+1][0]

# Execute a series of lines from the specified index.
# Each line can contain one or more statements separated by ':'
def execProgram(linenum):
    if not linenum: linenum = progLines[0][0]
    while True:
        index = lineIndex(linenum)
        if index is None: syntaxError(f"UNKNOWN LINE NUMBER {linenum}")
        line = progLines[index][1]
        if trace: print(f"{linenum} {line}")
        statements = splitStatements(line)
        nextLinenum = None
        for statement in statements:
            nextLinenum = execStatement(statement, linenum)
            if nextLinenum: break

        # Otherwise proceed to next line in order
        # If statement returns a new line number, jump to it
        if nextLinenum:
            if trace: print(f"Jumping to {linenum}")
            linenum = nextLinenum
        else:
            if index >= len(progLines): break # Fall off end
            if statement == "END": break
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
    match = re.match("[0-9]+", line)
    if not match: return (None, line)
    linenum = int(match.group())
    statements = right(line, match.group())
    return (linenum, statements)


def storeLine(linenum, statements):

    # Remove existing line and pseudo-lines, if any
    existing = [i for (i,l) in enumerate(progLines) if int(l[0]) == linenum]
    for i in reversed(existing): del progLines[i]

    # Insert in order
    insort(progLines, (linenum, statements))

    # Add DATA elements immediated
    if statements.startswith("DATA"):
        data = statements[4:].strip()
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
        line = input("] ")
        (linenum, statements) = parseLine(line)
        if linenum:
            storeLine(linenum, statements)
        else:
            # TODO split statements etc. first
            execStatement(statements, linenum)