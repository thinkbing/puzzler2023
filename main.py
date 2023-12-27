import re
from random import random, seed

program = """
10 PRINT TAB(33);"BATNUM"
20 PRINT TAB(15);"CREATIVE COMPUTING  MORRISTOWN, NEW JERSEY"
30 PRINT:PRINT:PRINT
110 PRINT "THIS PROGRAM IS A 'BATTLE OF NUMBERS' GAME, WHERE THE"
120 PRINT "COMPUTER IS YOUR OPPONENT."
130 PRINT 
140 PRINT "THE GAME STARTS WITH AN ASSUMED PILE OF OBJECTS. YOU"
150 PRINT "AND YOUR OPPONENT ALTERNATELY REMOVE OBJECTS FROM THE PILE."
160 PRINT "WINNING IS DEFINED IN ADVANCE AS TAKING THE LAST OBJECT OR"
170 PRINT "NOT. YOU CAN ALSO SPECIFY SOME OTHER BEGINNING CONDITIONS."
180 PRINT "DON'T USE ZERO, HOWEVER, IN PLAYING THE GAME."
190 PRINT "ENTER A NEGATIVE NUMBER FOR NEW PILE SIZE TO STOP PLAYING."
200 PRINT
210 GOTO 330
220 FOR I=1 TO 10
230 PRINT
240 NEXT I
330 INPUT "ENTER PILE SIZE";N
350 IF N>=1 THEN 370
360 GOTO 330
370 IF N<>INT(N) THEN 220
380 IF N<1 THEN 220
390 INPUT "ENTER WIN OPTION - 1 TO TAKE LAST, 2 TO AVOID LAST: ";M
410 IF M=1 THEN 430
420 IF M<>2 THEN 390
430 INPUT "ENTER MIN AND MAX ";A,B
450 IF A>B THEN 430
460 IF A<1 THEN 430
470 IF A<>INT(A) THEN 430
480 IF B<>INT(B) THEN 430
490 INPUT "ENTER START OPTION - 1 COMPUTER FIRST, 2 YOU FIRST ";S
500 PRINT:PRINT
510 IF S=1 THEN 530
520 IF S<>2 THEN 490
530 C=A+B
540 IF S=2 THEN 570
550 GOSUB 600
560 IF W=1 THEN 220
570 GOSUB 810
580 IF W=1 THEN 220
590 GOTO 550
600 Q=N
610 IF M=1 THEN 630
620 Q=Q-1
630 IF M=1 THEN 680
640 IF N>A THEN 720
650 W=1
660 PRINT "COMPUTER TAKES";N;"AND LOSES."
670 RETURN
680 IF N>B THEN 720
690 W=1
700 PRINT "COMPUTER TAKES";N;"AND WINS."
710 RETURN
720 P=Q-C*INT(Q/C)
730 IF P>=A THEN 750
740 P=A
750 IF P<=B THEN 770
760 P=B
770 N=N-P
780 PRINT "COMPUTER TAKES";P;"AND LEAVES";N
790 W=0
800 RETURN
810 PRINT:PRINT "YOUR MOVE ";
820 INPUT P
830 IF P<>0 THEN 870
840 PRINT "I TOLD YOU NOT TO USE ZERO! COMPUTER WINS BY FORFEIT."
850 W=1
860 RETURN
870 IF P<>INT(P) THEN 920
880 IF P>=A THEN 910
890 IF P=N THEN 960
900 GOTO 920
910 IF P<=B THEN 940
920 PRINT "ILLEGAL MOVE, REENTER IT ";
930 GOTO 820
940 N=N-P
950 IF N<>0 THEN 1030
960 IF M=1 THEN 1000
970 PRINT "TOUGH LUCK, YOU LOSE."
980 W=1
990 RETURN
1000 PRINT "CONGRATULATIONS, YOU WIN."
1010 W=1
1020 RETURN
1030 IF N>=0 THEN 1060
1040 N=N+P
1050 GOTO 920
1060 W=0
1070 RETURN
1080 END
"""

program = """
3 PRINT TAB(33);"CHEMIST"
6 PRINT TAB(15);"CREATIVE COMPUTING  MORRISTOWN, NEW JERSEY"
8 PRINT:PRINT:PRINT
10 PRINT "THE FICTITIOUS CHECMICAL KRYPTOCYANIC ACID CAN ONLY BE"
20 PRINT "DILUTED BY THE RATIO OF 7 PARTS WATER TO 3 PARTS ACID."
30 PRINT "IF ANY OTHER RATIO IS ATTEMPTED, THE ACID BECOMES UNSTABLE"
40 PRINT "AND SOON EXPLODES.  GIVEN THE AMOUNT OF ACID, YOU MUST"
50 PRINT "DECIDE WHO MUCH WATER TO ADD FOR DILUTION.  IF YOU MISS"
60 PRINT "YOU FACE THE CONSEQUENCES."
70 T=0
100 A=INT(RND(1)*50)
110 W=7*A/3
120 PRINT A;"LITERS OF KRYPTOCYANIC ACID.  HOW MUCH WATER";
130 INPUT R
140 D=ABS(W-R)
150 IF D>W/20 THEN 200
160 PRINT " GOOD JOB! YOU MAY BREATHE NOW, BUT DON'T INHALE THE FUMES!"
170 PRINT
180 GOTO 100
200 PRINT " SIZZLE!  YOU HAVE JUST BEEN DESALINATED INTO A BLOB"
210 PRINT " OF QUIVERING PROTOPLASM!"
220 T=T+1
230 IF T=9 THEN 260
240 PRINT " HOWEVER, YOU MAY TRY AGAIN WITH ANOTHER LIFE."
250 GOTO 100
260 PRINT " YOUR 9 LIVES ARE USED, BUT YOU WILL BE LONG REMEMBERED FOR"
270 PRINT " YOUR CONTRIBUTIONS TO THE FIELD OF COMIC BOOK CHEMISTRY."
280 END
"""

progLines = []
progNums = []
progIndexes = {}
variables = {}
gosubStack = []
forStack = []
trace = False

# ABS: absolute value of number
def ABS(val):
    return abs(val)

# INT: truncate number to integer
def INT(val):
    return int(val)

# RND: if <0, seed and return; if =0, return last number; if >0, return random float 0-1
lastRand = None
def RND(val):
    if val == 0: return lastRand
    if val < 0: seed(val)
    return random()

# TAB: space n characters
def TAB(val):
    return ' '*val

functions = {
    "ABS": ABS,
    "INT": INT,
    "RND": RND,
    "TAB": TAB
}

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

# Syntax: NEXT [variable]
def NEXT(statement, lineno):
    if len(forStack) == 0: syntaxError("NEXT WITHOUT FOR")
    (loopline, variable, min, max, step) = forStack[-1]
    if len(statement) > 0 and statement != variable: syntaxError("INCORRECT LOOP NESTING")
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
        elif part.startswith("TAB("):
            print("TODO print " + part)
        elif part.startswith("\""):
            parts[i] = part[1:-1]
        else:
            parts[i] = evalExpr(part)
    ending = "" if len(statement) > 0 and statement[-1] == ';' else None
    print(*parts, end=ending)
    return None

def REM(statement, lineno):
    pass

def RETURN(statement, lineno):
    if len(gosubStack) == 0: syntaxError("RETURN WITHOUT GOSUB")
    frame = gosubStack.pop()
    return frame

commands = {
    "FOR": FOR,
    "GOSUB": GOSUB,
    "GOTO": GOTO,
    "IF": IF,
    "INPUT": INPUT,
    "NEXT": NEXT,
    "PRINT": PRINT,
    "REM": REM,
    "RETURN": RETURN
}

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

if __name__ == '__main__':
    readProgram(program)
    execProgram(0)
