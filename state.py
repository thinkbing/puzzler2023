# Program state management
import re

progLines = []
progNums = []
progIndexes = {}
variables = {}
gosubStack = []
forStack = []
trace = False
functions = {}
commands = {}

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

    globals = functions
    locals = variables
    try:
        result = eval(expr, globals, locals)
        return result
    except NameError as err:
        syntaxError(str(err))

def assignVar(variable, value):
    variables[variable] = value
    if trace: print(variables)

def nextLine(lineno):
    index = progIndexes[lineno]
    return progNums[index + 1]

def execStatement(statement, lineno):

    match = re.match("[A-Z]+", statement)
    if not match:
        syntaxError(statement)
    word = match.group()
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
            statements.append(line[start:i])
            start = i+1
    if start < len(line):
        statements.append(line[start:])
    return statements

# Execute a series of lines from the specified index.
# Each line can contain one or more statements separated by ':'
def execProgram(index):
    while True:
        if index >= len(progLines): break
        line = progLines[index]
        lineno = progNums[index]
        if trace: print(f"{lineno} {line}")
        statements = splitStatements(line)
        linenum = None
        for statement in statements:
            linenum = execStatement(statement, lineno)
            if linenum: break

        # Otherwise proceed to next line in order
        # If statement returns a new line number, jump to it
        if linenum:
            if not linenum in progIndexes: syntaxError("UNKNOWN LINE NUMBER " + linenum)
            if trace: print(f"Jumping to {linenum}")
            index = progIndexes[linenum]
        else:
            index = index+1

def readProgram(progText):
    lines = progText.splitlines()
    index = 0
    for line in lines:
        if len(line) == 0: continue
        match = re.match("[0-9]+", line)
        if not match: syntaxError(line)
        linenum = int(match.group())
        progIndexes[linenum] = index
        progLines.append(right(line, match.group()))
        progNums.append(linenum)
        index = index+1

def initialize(fns, cmds):
    global functions, commands
    functions = fns
    commands = cmds