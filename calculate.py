import math

def calculate(formula):
    return eval(formula, {"arcsin": math.asin, "arccos": math.acos, "arctan": math.atan})