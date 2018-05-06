## Note 1: (from parse)
I will handle the assignment operator ('=') within the parse method itself. However, all the other operators will be handled within the method perform_operation. I think this makes the code a little cleaner, and in the future, with the
addition of user defined functions, will probably make things a lot easier. Also, '=' is the only operator that can change the value of a variable. This justifiies its special treatment.

## Note 2:
Things like ```3 4 +``` will give you an output of ```7```. One idea to fix it is through a buffer. That buffer may also help with evaluating functions later on.