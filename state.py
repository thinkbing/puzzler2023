# Program state management
import re

functions = {}
commands = {}
progLines = []
variables = {}
gosubStack = []
forStack = []
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

def execStatement(statement, lineno):

    if statement.startswith("REM"): return # No spaces etc. required after "REM"

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
            linenum = progLines[index+1][0]

def readProgram(progText):
    lines = progText.splitlines()
    for line in lines:
        if len(line) == 0: continue
        match = re.match("[0-9]+", line)
        if not match: syntaxError(line)
        linenum = int(match.group())
        progLines.append((linenum, right(line, match.group())))

def initialize(fns, cmds):
    global functions, commands
    functions = fns
    commands = cmds