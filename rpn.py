
class rpn:
    def infixtorpn(input):
        '''
        Converts string in infix form to reverse polish notation (outfix).
        Input should be a string, output will be a list of each character.
        '''
        input = list(input)
        operators = ['+', '-', '*', '/', '^']
        greateroperators = ['+', '-', '*', '/', '^', '(', ')']
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
        position = -1
    
        previous = None

        # adding multiplication signs before openparens and after closedparens that dont already have multiplication signs

        for i in input:
            position += 1
            if previous:
                if i == ")" and previous == "(": # these could probably just be removed but this option is smoother imo
                    input.insert(position - 1, "1*1")
                elif i == "(":
                    if previous != '(' and previous not in operators:
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
                if i not in greateroperators and previous not in greateroperators:
                    ainput[c-1] = str(previous) + str(i)
                    ainput.pop(c)
                    c -= 1

            
            c += 1
            if c <= len(input):
                previous = input[c-1]

        return input
    
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
            elif i in operators:
                if stack == []:
                    stack.append(i)
                    print("appended stack 1")

                elif topofstack == '(':
                    stack.append(i)
                    print("appended stack 1")

                elif pemdas.get(i) > pemdas.get(stack[-1]):
                    stack.append(i)
                    print("appended stack 2")

                elif pemdas.get(i) <= pemdas.get(stack[-1]):
                    print("appended stack 3")
                    for f in reversed(stack):
                        if f == "(":
                            break
                        if pemdas.get(i) <= pemdas.get(f):
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
            print("Stack: {}".format(stack))
            print("Initial top of stack: {}".format(topofstack))
            print("Result: {}".format(result))  


        for s in reversed(stack):
            result.append(s)

        return result



rpn.infixtorpn("33+22(5)")
