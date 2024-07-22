import math
from rpn import rpn

formula = "(-1)(-3/2)(4+ln(2))/5^e"

def run():
    b = rpn.calculateInfix(formula)
    print("{} = {}".format(formula, b))

if __name__ == "__main__":
    run()