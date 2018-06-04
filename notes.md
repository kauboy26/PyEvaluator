## Note 1: (from parse)
I will handle the assignment operator ('=') within the parse method itself. However, all the other operators will be handled within the method perform_operation. I think this makes the code a little cleaner, and in the future, with the
addition of user defined functions, will probably make things a lot easier. Also, '=' is the only operator that can change the value of a variable. This justifiies its special treatment.

## Note 2:
Things like ```3 4 +``` will give you an output of ```7```. One idea to fix it is through a buffer. That buffer may also help with evaluating functions later on.

## Note 3:
*Warning: This is outdated. A modified version is in Note 5.*  
The "a = -2" problem is basically that this parser couldn't handle things like "a = -2" (hence the name), since it wouldn't realize that the "-" sign can act on a single operand (it acts on 2 in this case, turning it into -2). The parser expected two operands, since generally, the minus sign acts on two operands (it performs subtraction).  
In general, the minus sign acts on the operand on its right whenever the operator stack has a length equal to that of the num stack, WITHIN THE SPACE WHERE THESE OPERATORS ACT. What is the "space" I speak of? The space the extent to which an expression extends. To clarify: (2 + 1, 3) is 2 spaces, since the 1 and 3 cannot mingle. 2 + (3 - 1) is, as a whole, onespace. BUT, since the 2 and 3 cannot mingle directly, this is two spaces. There is no really strict idea of a space, since the term was made up just now, but in a textbook you can surely find a better, formal word for it.  
Anyway, on entering a new space, we reset both stack lengths, since we can guarantee that everything before it was already taken care of. SEE NOTE 5

## Note 4:
On encountering an extra left paren, the program would try to pop it off the op_stack and then fetch operands for it. Of course, the left paren doesn't actually act on some number of operands. Because of this, self.args_needed[left_paren] would throw an exception. To get around this, that line had to be added.

## Note 5:
In the original fix, when the two stack lengths are equal, a minus sign knows it needs to act as a unary operator. This is sensible when we only have standard operators, i.e, operators that that take two operands and return one number as a result. However, with functions, this model isn't strictly followed, since a function can take zero to *n* arguments, and will return one number as the result. To get around this, a proposed idea is to keep track of the total effect an operator or function has on the number of operators. For example, "-" has an effect of "-1", since it takes two, but returns only one. A function "f" that takes 5 arguments will have an effect of "-4", since it takes 5 but returns only one.  
Whenever the total effect is 0, the minus sign will know that it needs to act as a unary minus.  
The other half of the solution is regarding the new stack that has been introduced. On entering a new space due to a comma, the total effect for this frame needs to be reset. However on entering a new space due to a paren, we need to add a new frame to the stack, and keep track of things in this new frame. Basically it needs to be isolated.