# BASIC built-in functions
from random import random, seed
from math import sin

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

# SIN: sine of argument
def SIN(val):
    return sin(val)

# TAB: space n characters
def TAB(val):
    return ' '*val

def makeFunctions():
    return {
        "ABS": ABS,
        "INT": INT,
        "RND": RND,
        "SIN": SIN,
        "TAB": TAB
    }