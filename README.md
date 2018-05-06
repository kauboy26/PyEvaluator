# PyEvaluator
I would like to call this a language, although maybe that's an exaggeration. PyEvaluator evaluates statements that are arithmetic expressions, variable assignments, or function definitions. Here are it's features:    

* Assignment statement processing  
```>>  a = 3 + 4```
* Multi character variable names  
```>>  hello = hello + world + 15```
* Pre-defined functions (you can call sin(x), etc)  
```>>  sin(22/7)```
* Finally, defining and using your own functions.  
```>>  def cos(x) = pow(1 - pow(sin(x), 2), 1/2)```  

## Usage
You need Python 2.7 on your computer. Run the following:  
```
python lex_test_script.py
```  
That should start it and you will see a prompt ```>>```. Type in whatever expressions you want, like "```a0 = 1 + 3 * 4```", etc and have a blast. Type in "```help```" if you don't know what to do.