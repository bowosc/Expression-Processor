import math
from rpn import rpn

formula = "eee"

def run():
    b = rpn.infixtorpn(formula)
    b = rpn.rpntosolution(b)
    print("=====-----finale:")
    print(b)

if __name__ == "__main__":
    run()