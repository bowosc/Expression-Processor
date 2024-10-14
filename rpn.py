import math

#TODO
# Imaginary number handling
# Test more edge-case, weird notations?

operators = ['+', '-', '*', '/', '^']
greateroperators = ['+', '-', '*', '/', '^', '(', ')']
advancedoperators = {  
    # Note that advanced operators are sometimes referred to as ADVOPS 
    # in function names, variable names, and comments. 
    # These are ordered like this because the search & replace tool 
    # goes first to last, and all the inverse trig will get screwed 
    # up if it replaces the basic trig strings first. 

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
    'π': 't',
    'i': 'i'
}
pemdas = {
        "^": 5, 
        "*": 4, 
        "/": 3, 
        "+": 2, 
        "-": 1
    }

class nonrealValueError(Exception):
    '''Raised when rpn.py encounters an imaginary value, which it can't compute yet.'''
    pass

class rpn:
    '''
    A library for converting math expressions from infix to outfix (AKA reverse polish notation) to a solution.
    The expression entered should not be an equation, meaning there should be no "=" equals sign.
    No characters other than mathematical notation and numbers should be used, except for the constants e and pi, because many characters are used internally as placeholders for operations.
    OK expression: sin(pi/2)(2+e(abs(-3)/4)
    Not OK expression: skibidi(3s=3x)--2&(((
    '''

    def processAdvops(input):
        '''
        Input must be a string.
        Search and replaces all operators and constants to be single chars.
        '''
        for op in advancedoperators:
            input = input.replace(op, advancedoperators[op])
            #print("replaced any instances of {} with {}".format(op, advancedoperators[op]))
        for const in constants:
            input = input.replace(const, constants[const])
            #print("replaced any instances of {} with {}".format(const, constants[const]))
        return input

    def impMultParens(input):
        '''
        Input must be a list.
        Adds multiplication signs before openparens and after closedparens that don't already have operators.
        ''' 
        position = -1
        previous = None

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
                                #print("a put a little * at pos " + str(position))
                elif previous == ")":
                    if i not in operators and i != ")":
                        input.insert(position, "*")
            previous = i
        return input
    
    def impMultAdvops(input):
        '''
        Input must be a list.
        Adds multiplication signs before and after advancedoperators that don't already have operators.
        '''
        previous = None
        position = -1
        for i in input:
            position += 1

            if previous:
                if i in advancedoperators.values(): 
                    if previous not in operators and previous not in advancedoperators.values():
                        if previous != "(":
                            input.insert(position, "*")
                            #print("b put a little * at pos " + str(position))
                            #print(input)
                            position += 1
                    
            previous = i
        return input
    
    def impMultConstants(input):
        '''
        Input must be a list.
        Adds multiplication signs before constants that don't already have operators.
        '''
        previous = None
        position = -1
        skipthis = False
        for i in input:
            position += 1
            if skipthis == True:
                skipthis = False
            elif previous:
                if i in constants.values():
                    if previous not in operators:
                        if previous != "(":
                            input.insert(position, "*")
                            #print("c put a little * at pos " + str(position) + str(i) + str(previous))
                            position += 1
                            skipthis = True
            previous = i
        return input

    def numCombine(input):
        '''
        Input must be a list.
        Combines multiple floats (or anything without operators between them) into one element.
        '''
        previous = None
        ainput = input
        c = 0
        
        while c < len(input):
            i = input[c]

            if previous:
                if c > 0:
                    if i not in greateroperators:
                        if previous not in greateroperators:
                            ainput[c-1] = str(previous) + str(i)
                            ainput.pop(c)
                            c -= 1

            c += 1
            if c <= len(input):
                previous = input[c-1]
        return input
    
    def negativeConvert(input):
        '''
        Input must be a list.
        Converts negative numbers into a form that's more readable for the algorithm.
        '''
        previous = None
        position = -1
        skipthis = False
        for i in input:
            position += 1
            if position+1 >= len(input):
                break
            #print("---------")
            #print("p: {}, i: {}, p+1: {}, pos: {}".format(previous, i, input[position+1], position))
            if skipthis == True:
                skipthis = False
            if previous == None or previous in greateroperators:
                if i == "-":
                    #print(i)
                    #print(input[position+1])
                    
                    input[position+1] = "-" + str(input[position+1])
                    input.pop(position)
                        
                    #print("fixed up a negative " + str(input))
                    skipthis = True

            previous = i
        return input

    def infixToRPN(input):
        '''
        Input must be an already-formatted list of each character in an expression.
        Converts input from Infix notation to Reverse Polish Notation, using the Dijkstra Shunting-Yard Algorithm.
        Returns a list of each character in the expression, with substitutive symbols used in place of constants or multi-character operations such as sin() or sqrt().
        '''

        stack = []
        result = []
        topofstack = "none"

        input = rpn.infixToGoodInfix(input)

        for i in input:
            #print("----------------")
            if stack == []:
                topofstack = "none"
            else:
                topofstack = stack[-1]
                
            #print(topofstack)

            def pemdassify(i): # somewhere around here
                    #print("appended stack")
                    for f in reversed(stack): # top and back
                        if f == "(":
                            stack.append(i)
                            break
                        elif f in advancedoperators.values():
                            result.append(f)
                            stack.pop()
                            #print("dealt with advop in pemdas cycle: " + f)
                        elif pemdas.get(i) <= pemdas.get(f):
                            result.append(f)
                            stack.pop()
                        elif pemdas.get(i) > pemdas.get(f):
                            stack.append(i)
                            break
                        else:
                            print("[rpn] Error! pemdas part is broken again.")
                        
                        if stack == []:
                            stack.append(i)
                    #print(stack)            
            

            if i not in greateroperators and i not in advancedoperators.values():
                result.append(i)
            elif i == "(":
                stack.append(i)
            elif i == ")":
                for f in reversed(stack):
                    if f == '(':
                        stack.pop()
                        break
                    else:
                        result.append(f)
                        stack.pop()

            elif i in advancedoperators.values():
                    stack.append(i)
                    # if this method gets screwed up, its probably here lol

            elif i in operators:
                if stack == []:
                    stack.append(i)

                elif topofstack == '(':
                    stack.append(i)
                
                elif topofstack in advancedoperators.values():
                    pemdassify(i)
                    #print("appended stack with operator, pushed advop to result. pemdas as garfield intended")

                elif pemdas.get(i) > pemdas.get(stack[-1]):
                    stack.append(i)
                
                elif pemdas.get(i) <= pemdas.get(stack[-1]):
                    pemdassify(i)
                else:
                    print("[rpn] Error! Unhandled character after pemdassifying expression.") 
            else:
                print("[rpn] Error! Unhandled character!") 


            # useful when searching for an error
            '''print("Input: {}".format(input))
            print("Focus (i): {}".format(i))
            print("Current stack: {}".format(stack))
            print("Initial top of stack: {}".format(topofstack))
            print("Result: {}".format(result))  '''

        for s in reversed(stack):
            result.append(s)

        return(result)

    def calculateRPN(input):
        print(input)
        '''
        Input must be a list of each character in the expression, which must be formatted in Reverse Polish Notation.
        Computes a float answer to the inputted expression.
        '''
        def conkulate(a, b, i): #binary operators
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
        
        def corgulate(a, i): #unary operators
            try:
                if i == "o":
                    m = math.exp(a)
                if i == "p":
                    m = math.sqrt(a)
                if i == "q":
                    m = math.log(a)
                if i == "r":
                    m = abs(a)
                else:
                    a = math.radians(a) # math.sin() and friends accept radians input
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
                

                
            except ValueError:
                print("[rpn] Domain error!")
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
                #print("{} {} {} = {}".format(a, i, b, m))
                stack.pop()
                stack.pop()
                stack.append(m)
                m = str(m)
            elif i in advancedoperators.values(): # tan or exp or whatever
                a = float(stack[-1])
                m = corgulate(a, i)
                #print("{} of {} = {}".format(i, a, m))
                stack.pop()
                stack.append(m)
                m = str(m)
            else: # must be a number ig 
                if i in constants.values():
                    if i == "t":
                        i = math.pi
                    if i == "s":
                        i = math.exp(1) # e^1
                    if i == "i":
                        # imaginary number
                        raise nonrealValueError
                        
                #print("added to stack: " + str(i))
                stack.append(i)
        result = stack[-1]
        return result

    def infixToGoodInfix(input):
        '''
        Input must be a string expression/equation, formatted in infix (normal) notation.
        Cleans up expression so that infixToRPN() can convert it properly, and calculateRPN() can process it properly.
        Ex:
        sin(x) -> a(x)
        pi(x) -> t(x)
        (a)(b) -> (a)*(b)
        -x -> (-1*x)
        '''
        b = rpn.processAdvops(input)
        b = list(b)
        b = rpn.impMultAdvops(b)
        b = rpn.impMultParens(b)
        b = rpn.impMultConstants(b)
        b = rpn.numCombine(b)
        b = rpn.negativeConvert(b)
        return b
    
    def calculateInfix(input):
        '''
        Input must be a string expression, formatted in infix (normal) notation. No characters other than mathematical notation and numbers should be used, except for the constants e and/or pi.
        Calculates mathematical value of input.
        Ex: 2(sin(pi/2)^2) would return 2.
        '''
        try:
            input = rpn.infixToRPN(input)
            result = rpn.calculateRPN(input)
            return result
        except ValueError:
            return(print("[rpn] Syntax Error! Please double-check your expression and make sure the notation is correct."))
        except ZeroDivisionError:
            return(print("[rpn] Please don't try to divide by zero."))
        except TypeError:
            return("[rpn] TypeError. Might be my bad, but you should probably check your input just to be sure.")
        except nonrealValueError:
            return(print("[rpn] Imaginary value encountered. rpn.py cannot yet calculate imaginary values. Sorry! "))
        except:
            return(print("[rpn] Something went wrong. Double-check the formatting of your input, then make a bug report."))