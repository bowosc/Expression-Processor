import math
from rpn import rpn

formula = "sin(3^cos(4pi))/ln(4)"

def run():
    b = rpn.infixtorpn(formula)
    b = rpn.rpntosolution(b)
    print("=====-----finale:")
    print(b)

if __name__ == "__main__":
    run()