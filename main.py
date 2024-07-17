import math
from rpn import rpn

formula = "3/2"

def run():
    b = rpn.calculateInfix(formula)
    print("=====-----finale:")
    print(b)

if __name__ == "__main__":
    run()