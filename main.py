import math
from rpn import rpn



def run():
    print(rpn.infixtorpn("123.456+22(5/44)"))

if __name__ == "__main__":
    run()