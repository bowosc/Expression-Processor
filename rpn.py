class rpn:
    def infixtorpn(input):
        input = list(input)
        operators = ['+', '-', '*', '/', '^']
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
    
        previous = ""

        # adding multiplication signs before openparens and after closedparens that dont already have multiplication signs
        ainput = input
        for i in ainput:
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



