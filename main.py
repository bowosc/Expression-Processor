import math
from rpn import rpn

formula = "(-3/2)(4+ln(2))/5^e^pi"

def run():
    b = rpn.calculateInfix(formula)
    print("=====-----finale:")
    print(b)

if __name__ == "__main__":
    run()