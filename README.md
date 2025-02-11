<h3> Mathematical Expression Processor </h3>

<p> I didn't find a module that did this in my 10-second Google search, so I built this. </p>
<i>Update: I did a 30-second Google search, found Sympy and now use that instead. Sorry, Expression-Processor.</i>
<br>
<br>
<p> This project converts a given expression from infix to outfix (Reverse Polish Notation), and then calculates the result. </p>
<p> Examples: </p>
<p> rpn.calculateInfix("(2sin(pi/2))^-1")  -->  0.5 </p>
<p> rpn.infixToRPN("(2sin(pi/2))^-1")  -->  ['2', 't', '2', '/', 'a', '*', '-1', '^']</p>
<p> # Note that "t" represents pi, and "a" represents sin() within the program. </p>


<p> rpn.py contains a little library and some tools for solving infix and outfix-notation expressions. </p>
<p> It accepts expressions, not equations, meaning there should be no "=" equals sign. </p>

<p> # Please note that this repository cannot yet handle imaginary values. </p>
