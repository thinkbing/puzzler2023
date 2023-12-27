# BASIC built-in functions
from random import random, seed
from math import sin

# ABS: absolute value of number
def ABS(val):
    return abs(val)

# ASC: ascii value of character
def ASC(val):
    return ord(val)

def CHR_(val):
    return chr(val)

# INT: truncate number to integer
def INT(val):
    return int(val)

# LEFT$: return leftmost n characters
def LEFT_(val, val2):
    return val[0:val2]

# LEN: return length of string
def LEN(val):
    return len(val)

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

# SIN: sine of argument
def SIN(val):
    return sin(val)

# TAB: space n characters
def TAB(val):
    return ' '*val

def makeFunctions():
    return {
        "ABS": ABS,
        "ASC": ASC,
        "CHR_": CHR_,
        "INT": INT,
        "LEFT_": LEFT_,
        "LEN": LEN,
        "MID_": MID_,
        "RND": RND,
        "SIN": SIN,
        "TAB": TAB
    }