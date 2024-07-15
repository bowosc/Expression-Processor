import math
#TODO
# be able to process advancedoperators (sin, ln, abs)
# process constants like e and pi
# substitute variable(s)

operators = ['+', '-', '*', '/', '^']
greateroperators = ['+', '-', '*', '/', '^', '(', ')']
advancedoperators = { # these are ordered like this because the search & replace tool goes first to last, and all the arcs will get screwed up if it replaces the basic trigs first.
        'arcsin': 'h', 
        'arccos': 'j', 
        'arctan': 'k', 
        'arcsec': 'l', 
        'arccsc': 'm', 
        'arccot': 'n', 
        'sin':'a', 
        'cos':'b', 
        'tan':'c', 
        'sec': 'd', 
        'csc': 'f', 
        'cot': 'g', 
        'exp': 'o', 
        'sqrt': 'p', 
        'ln': 'q', 
        'abs': 'r'
    }
constants = ['e', 'pi', 'π']
stack = []
result = []
topofstack = "none"
pemdas = {
        "^": 5, 
        "*": 4, 
        "/": 3, 
        "+": 2, 
        "-": 1
    }

class rpn:
    def infixtorpn(input):
        '''
        Converts string in infix form to reverse polish notation (outfix).
        Input should be a string, output will be a list of each character.
        the only variable used should be x.
        '''
        position = -1
        previous = None

        # note that input list is still a string rn
        for op in advancedoperators:
            input = input.replace(op, advancedoperators[op])
            print("replaced {} with {}".format(op, advancedoperators[op]))
            # go through string and replace single symbols for the advops

        input = list(input)

    
        # adding multiplication signs before openparens and after closedparens that dont already have multiplication signs
        for i in input:
            position += 1
            if previous:
                if i == ")" and previous == "(": # these could probably just be removed but this option is smoother imo
                    input.pop(position)
                    input.pop(position)
                elif i == "(":
                    if previous != '(' and (previous not in operators) and (previous not in advancedoperators.values()):
                        input.insert(position, "*")
                elif previous == ")":
                    if i not in operators:
                        input.insert(position, "*")
            previous = i

        
        position = -1
        ainput = input
        c = 0
        while c < len(input):
            i = input[c]

            if previous:
                if position > 0:
                    if i not in greateroperators and previous not in greateroperators:
                        ainput[c-1] = str(previous) + str(i)
                        ainput.pop(c)
                        c -= 1

            
            c += 1
            if c <= len(input):
                previous = input[c-1]


        # forgot what this was for and scared to delete
                
        '''        for i in input:
            position += 1
            print("------===------")
            print("current:" + i)
           


            if previous:
                print("previous:" + previous)
                if i not in greateroperators and previous not in greateroperators:
                    ainput[position-1] = str(previous) + str(i)
                    ainput.pop(position)
                    position -= 1
            
            previous = input[position]'''
        '''            if previous:
                print("previous:" + previous)
                if i not in greateroperators and previous not in greateroperators:
                    ainput[position-1] = (str(previous)+str(i))
                    print("combined {} and {} to make {}.".format(previous, i, ainput[position-1]))
                    ainput.pop(position)
                    position -= 1
                    print("current list:")
                    print(input)
           '''
        
        for i in input:
            print("----------------")
            if stack == []:
                topofstack = "none"
            else:
                topofstack = stack[-1]
                
            print(topofstack)
            

            if i not in operators and i not in ["(", ")"]:
                if i not in advancedoperators.values():
                    result.append(i)
                    print("appended result with numbah")
            elif i == "(":
                stack.append(i)
                print("appended stack parenthesie")
            elif i == ")":
                print("did the parenthesie thing")
                for f in reversed(stack):
                    if f == '(':
                        stack.pop()
                        break
                    else:
                        result.append(f)
                        stack.pop()
            elif i in operators or i in advancedoperators.values():
                if stack == []:
                    stack.append(i)
                    print("appended stack 1")

                elif topofstack == '(':
                    stack.append(i)
                    print("appended stack 1")

                elif i in advancedoperators.values():
                    stack.append(i)
                    print("appended stack 1.5") # if this method gets screwed up, its probably here lol

                elif pemdas.get(i) > pemdas.get(stack[-1]):
                    stack.append(i)
                    print("appended stack 2")

                elif pemdas.get(i) <= pemdas.get(stack[-1]): # somewhere around here
                    print("appended stack 3")
                    for f in reversed(stack):
                        if f == "(":
                            stack.append(i)
                        elif pemdas.get(i) <= pemdas.get(f):
                            result.append(f)
                            stack.pop()
                            print("dumb2")
                        elif pemdas.get(i) > pemdas.get(f):
                            print("dumb3")
                            stack.append(i)
                            break
                        else:
                            print("error! pemdas part is broken again.")
                        
                        if stack == []:
                            stack.append(i)
                    print(stack)
            else:
                print("-=[0][0][0] Error! Unhandled character! [0][0][0]=-") 

            print("Input: {}".format(input))
            print("Focus (i): {}".format(i))
            print("Current stack: {}".format(stack))
            print("Initial top of stack: {}".format(topofstack))
            print("Result: {}".format(result))  


        for s in reversed(stack):
            result.append(s)

        print(result)
        return result

    def rpntosolution(input):
        result = []
        for i in input:
            '''if i in advancedoperators.values():
                for key, value in advancedoperators.items():
                    if value == i:
                        i = key'''
            if i in operators:
                b = float(stack[-1])
                a = float(stack[-2])
                if i == "+":
                    m = a + b
                elif i == "-":
                    m = a - b
                elif i == "/":
                    m = a / b
                elif i == "*":
                    m = a * b
                elif i == "^":
                    m = a ** b
                print("{} {} {} = {}".format(a, i, b, m))
                stack.pop()
                stack.pop()
                stack.append(m)
                m = str(m)
            else:
                print("added to stack " + i)
                stack.append(i)
        print(stack)
        result = stack[-1]
        return result

