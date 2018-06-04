# PyEvaluator
I would like to call this a language, although maybe that's an exaggeration. PyEvaluator evaluates statements that are arithmetic expressions, variable assignments, or function definitions. Here are its features:    

* Assignment statement processing  
```>>  a = 3 + 4```
* Multi character variable names  
```>>  hello = hello + world + 15```
* Pre-defined functions (you can call sin(x), etc)  
```>>  sin(22/7)```
* Finally, defining and using your own functions.  
```>>  def cos(x) = pow(1 - pow(sin(x), 2), 1/2)```  

## Usage
You need Python 2.7 on your computer. Run the following, within the directory containing ```lex_test_script.py```:  
```
python lex_test_script.py
```  
That should start it and you will see a prompt ```>>```. Type in whatever expressions you want, like "```>>  a0 = 1 + 3 * 4```", etc and have a blast. Type in "```help```" if you don't know what to do.

## Oddities
These work:  
* ```>>  3 4 +```
In general, you can misplace arguments, put commas in the wrong place (it depends), etc. In this implementation, only the number of arguments is verified(counting the args and then counting the commas), not the exact position of the arguments. I will fix
this later if time permits.

## Running Tests
Run this command:  
```python lex_tests.py```   
All tests should pass. Ignore the other messages that are printed to console, they are messages from the parser.