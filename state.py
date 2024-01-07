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

def setTrace(val):
    global trace
    trace = val

def evalExpr(expr):

    # Replace = with == (but preserve <= and >=), and <> with !=
    expr = re.sub(r"([^<>])\=", r"\1==", expr)
    expr = expr.replace("<>", "!=")

    # Exponentiation
    expr = expr.replace("^", "**")

    # AND/OR to and/or
    expr = re.sub(r"(\W)(AND)(\W)", r"\1and\3", expr)
    expr = re.sub(r"(\W)(OR)(\W)", r"\1or\3", expr)

    # Convert variable names and functions ending in "$" to "Σ"
    expr = re.sub(r"([A-Z]+[0-9]*)(\$)", r"\1Σ", expr)

    # Convert array references to end in "Ξ" since non-array vars could have same names
    # /(?<!pattern/ is "negative lookbehind": if the rest of the regex matches but
    # /pattern/ is found immediately before that match, then the match fails
    # This makes sure we'll match "B(12)" if array var "B" exists, but not "TAB(12)"
    for var in variables:
        if var[-1] == 'Ξ' and var[:-1]+"(" in expr:
            expr = re.sub(fr"(?<![A-Z])({var[:-1]})\(", r"\1Ξ(", expr)

    globals = functions
    locals = variables
    try:
        result = eval(expr, globals, locals)
        return result
    except Exception as err:
        syntaxError(str(err))


def execStatement(statement, lineno):

    if statement.startswith("REM"): return # No spaces etc. required after "REM"

    # Convert variable assignments to "LET"
    # Examples: A=... BOO=... C12=... D(12)=... E(1+F(G))= FOO$=...
    match = re.match(r"^[A-Z]+[0-9]*\$?(\(.+\))?\=", statement)
    if match: statement = "LET " + statement

    # Match command
    match = re.match("[A-Z]+[0-9]*", statement)
    if not match: syntaxError(statement)
    word = match.group()

    if word in commands:
        # Valid command: execute it
        command = commands[word]
        remain = right(statement, word)
        return command(remain, lineno)
    elif not lineno:
        # Otherwise, if in immediate mode attempt to evaluate it
        print(evalExpr(statement))
    else:
        syntaxError(statement)


# Helpers
def lineIndex(linenum):
    return next(i for (i,l) in enumerate(progLines) if l[0] == linenum)

def nextLine(linenum, wholeLine=False):
    index = lineIndex(linenum) + 1
    while wholeLine and int(progLines[index][0]) == linenum:
        index = index + 1
    return progLines[index][0]

def splitUnquoted(quotes, delimiters, text):
    parts = []
    inside = 0
    start = 0
    for i in range(len(text)):
        if text[i] in quotes: inside = inside+1
        if text[i] in delimiters and inside%2 == 0:
            parts.append(text[start:i].strip())
            start = i+1
    if start < len(text):
        parts.append(text[start:len(text)].strip())
    return parts

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
    progLines.clear()
    variables.clear()
    gosubStack.clear()
    forStack.clear()
    dataList.clear()
    global dataIndex
    dataIndex = 0


def parseLine(line):

    # Parse line number, if any
    linenum = None
    match = re.match("[0-9]+", line)
    if match:
        linenum = int(match.group())
        line = right(line, match.group())

    # Parse statements, assigning fractional line number for multi-statement lines
    if line.startswith("REM"): return [(linenum, line)]
    if line.startswith("IF"): line = re.sub(r"THEN(?![ ]+[0-9]+)", r"THEN:", line)
    if ':' not in line: return [(linenum, line)]
    statements = splitUnquoted('"', ":", line)
    return [(linenum + 0.1*i if linenum else None, s) for (i,s) in enumerate(statements)]


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
        line = input("] ")
        try:
            statements = parseLine(line)
            for (linenum, statement) in statements:
                if linenum:
                    storeLine(linenum, statement)
                else:
                    execStatement(statement, linenum)
        except Exception as exc:
            print(exc)