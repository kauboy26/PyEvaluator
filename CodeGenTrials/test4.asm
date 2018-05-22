; Attempting to convert " 8 * (9 + 90) "
.orig x3000
LD R6, STACK

; The result will be in R0
AND R0 , R0 , 0 ; set R0 to 90
ADD R0 , R0 , 15
ADD R0 , R0 , 15
ADD R0 , R0 , 15
ADD R0 , R0 , 15
ADD R0 , R0 , 15
ADD R0 , R0 , 15
AND R1 , R1 , 0 ; set R1 to 9
ADD R1 , R1 , 9
ADD R0 , R0 , R1 ; ADD
ADD R6 , R6 , -1 ; push value in R0 to stack
STR R0 , R6 , 0
LDR R0 , R6 , 0 ; pop into R0
ADD R6 , R6 , 1
AND R1 , R1 , 0 ; set R1 to 8
ADD R1 , R1 , 8
JSR MULT
ADD R6 , R6 , -1 ; push value in R0 to stack
STR R0 , R6 , 0
LDR R0 , R6 , 0 ; pop into R0
ADD R6 , R6 , 1
HALT
STACK .fill xF000

    ; Take in args in r0 and r1, non neg nums only
    MULT       AND R2, R2, 0       ; use R3 to accumlate the result
        
                ADD R1, R1, 0
    MLOOP      BRnz MULT_RET
                ADD R2, R2, R0
                ADD R1, R1, -1
                BR MLOOP

    MULT_RET    ADD R0, R2, 0

                RET
    
.end
