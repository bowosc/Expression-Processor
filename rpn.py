import math


operators = ['+', '-', '*', '/', '^']
greateroperators = ['+', '-', '*', '/', '^', '(', ')']
advancedoperators = { # these are ordered like this because the search & replace tool goes first to last, and all the inverse trig will get screwed up if it replaces the basic trigs first.
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
constants = {
    'e': 's',
    'pi': 't',
    'π': 't'
}
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
        the only variable used should be x. many other characters are used internally as placeholders for operations.
        '''
        position = -1
        previous = None

        # search and replace all operators and constants to be single-chars, to make processing easier
        for op in advancedoperators:
            input = input.replace(op, advancedoperators[op])
            print("replaced any instances of {} with {}".format(op, advancedoperators[op]))
        for const in constants:
            input = input.replace(const, constants[const])
            print("replaced any instances of {} with {}".format(const, constants[const]))

        input = list(input)

        print("got there 1")
        # adding multiplication signs before openparens and after closedparens that dont already have operators 
        for i in input:
            position += 1

            if previous:
                if i == ")" and previous == "(": # removes bubbles: O -> 0 -> () -> * -> input.pop
                    input.pop(position - 2)
                    input.pop(position - 2)
                elif i == "(":
                    if previous != '(':
                        if previous not in operators:
                            if previous not in advancedoperators.values():
                                input.insert(position, "*")
                                print("a put a little * at pos " + str(position))
                elif previous == ")":
                    if i not in operators and i != ")":
                        input.insert(position, "*")
            previous = i
        
        previous = None
        position = -1
        # adding multiplication signs before advops that don't already have operators
        for i in input:
            position += 1

            if previous:
                if i in advancedoperators.values(): 
                    if previous not in operators and previous not in advancedoperators.values():
                        if previous != "(":
                            input.insert(position, "*")
                            print("b put a little * at pos " + str(position))
                            print(input)
                            position += 1
                    
            previous = i
        
        # adding multiplication signs before constants that don't already have operators
        previous = None
        position = -1
        for i in input:
            position += 1
            if previous:
                if i in constants.values():
                    if previous not in operators:
                        if previous != "(": # previous != i is a dumb fix, there exists a safer one
                            input.insert(position, "*")
                            print("c put a little * at pos " + str(position) + str(i) + str(previous))
                            position += 1
            previous = i


        position = -1
        previous = None
        ainput = input
        c = 0
        # combining multiple number elements (technically combines anything without * between them) into one element
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

            def pemdassify(i): # somewhere around here
                    print("appended stack 3")
                    for f in reversed(stack): # top and back
                        if f == "(":
                            stack.append(i)
                            break
                        elif f in advancedoperators.values():
                            result.append(f)
                            stack.pop()
                            print("dealt with advop in pemdas cycle: " + f)
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
            

            if i not in greateroperators and i not in advancedoperators.values():
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

            elif i in advancedoperators.values():
                    stack.append(i)
                    print("appended stack 1.5") # if this method gets screwed up, its probably here lol

            elif i in operators:
                if stack == []:
                    stack.append(i)
                    print("appended stack 1")

                elif topofstack == '(':
                    stack.append(i)
                    print("appended stack 1")
                
                elif topofstack in advancedoperators.values():
                    pemdassify(i)
                    print("appended stack with operator, pushed advop to result. pemdas as garfield intended")

                elif pemdas.get(i) > pemdas.get(stack[-1]):
                    stack.append(i)
                    print("appended stack 2")
                

                elif pemdas.get(i) <= pemdas.get(stack[-1]):
                    pemdassify(i)
                else:
                    print("unhandled character after pemdasing") 
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

        def conkulate(a, b, i):
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
            return m
        
        def corgulate(a, i):
            try:
                if i == "h":
                    m = math.asin(a)
                if i == "j":
                    m = math.acos(a)
                if i == "k":
                    m = math.atan(a)
                if i == "l":
                    m = math.acos(1/a) # arcsec
                if i == "m":
                    m = math.acsc(1/a) # arccsc
                if i == "n":
                    m = math.atan(1/a) # arctan
                if i == "a":
                    m = math.sin(a)
                if i == "b":
                    m = math.cos(a)
                if i == "c":
                    m = math.tan(a)
                if i == "d":
                    m = 1 / math.cos(a) # sec
                if i == "f":
                    m = 1 / math.sin(a) # csc
                if i == "g":
                    m = 1 / math.tan(a) # cot
                if i == "o":
                    m = math.exp(a)
                if i == "p":
                    m = math.sqrt(a)
                if i == "q":
                    m = math.log(a)
                if i == "r":
                    m = abs(a)
            except ValueError:
                print("Domain error!")
            return m

        result = []
        stack = []
        for i in input:
            '''if i in advancedoperators.values():
                for key, value in advancedoperators.items():
                    if value == i:
                        i = key'''
            if i in operators:
                b = float(stack[-1])
                a = float(stack[-2])
                m = conkulate(a, b, i)
                print("{} {} {} = {}".format(a, i, b, m))
                stack.pop()
                stack.pop()
                stack.append(m)
                m = str(m)

            elif i in advancedoperators.values(): # tan or exp or something
                a = float(stack[-1])
                m = corgulate(a, i)
                print("{} of {} = {}".format(i, a, m))
                stack.pop()
                stack.append(m)
                m = str(m)

            else: # must be a number ig 
                if i in constants.values():
                    if i == "t":
                        i = math.pi
                    if i == "s":
                        i = math.exp(1) # e^1
                print("added to stack: " + str(i))
                stack.append(i)
        print(stack)
        result = stack[-1]
        return result

