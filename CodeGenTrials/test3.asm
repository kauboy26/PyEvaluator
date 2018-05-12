; Attempting to convert " (8) "
.orig x3000
LD R6, STACK

; The result will be in R0
AND R0 , R0 , 0 ; set R0 to 8
ADD R0 , R0 , 8
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
