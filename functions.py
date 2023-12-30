# BASIC built-in functions
from random import random, seed
from math import sin, cos, tan, atan, exp, sqrt, log


def ABS(val): return abs(val)
def ASC(val): return ord(val)
def ATN(val): return atan(val)
def CHR_(val): return chr(val)
def COS(val): return cos(val)
def EXP(val): return exp(val)
def INT(val): return int(val)
def LEFT_(v1, v2): return v1[0:v2]
def LEN(val): return len(val)
def LOG(val): return log(val)
def RIGHT_(v1, v2): return v1[-v2:]
def SGN(val): return val and (1,-1)[val<0]
def SIN(val): return sin(val)
def SQR(val): return sqrt(val)
def STR_(val): return str(val)
def TAB(val): return ' '*int(val)
def TAN(val): return tan(val)
def VAL(val): return float(val) if '.' in val else int(val)

# Return substring from start (of specified length, or through end)
def MID_(val, start, length=None):
    if length:
        return val[start-1:start-1+length]
    else:
        return val[start-1]

# RND: if <0, seed and return; if =0, return last number; if >0, return random float 0-1
lastRand = None
def RND(val):
    if val == 0: return lastRand
    if val < 0: seed(val)
    return random()


import inspect, sys
def makeFunctions():
    # Auto-generate function map from member functions in UPPERCASE
    members = inspect.getmembers(sys.modules[__name__])
    commands = {name:obj for name, obj in members if inspect.isfunction(obj) and name.upper() == name}
    return commands