# About
Just generates assembly (LC3) for an infix expression that consists of only parentheses, multiplication and addition.
Although the main parts of PyEval can do a lot more, here I was just trying some experiments out.

## Usage
Ensure that your expression is valid:  
```
python lp.py <your expression within double quotes>  >  <file name.asm>
```  
For example,  
```
python lp.py "8 + (8 * 7 + 33) * (90 + 10)" > test20.asm
```  
Then you can load and run ```test20.asm``` on any lc3 simulator such as [COMPLX](https://github.com/TricksterGuy/complx)  
```
complx test20.asm
```  
Expect to see the result in R0