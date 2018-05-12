; Evaluate the string:
; (9 + 8) * (2 + 7) + 3
.orig x3000
    LD R6, STACK


    AND R0, R0, 0   ; set r0, 9
    ADD R0, R0, 9
    AND R1, R1, 0   ; set r1, 8
    ADD R1, R1, 8
    ADD R0, R0, R1  ; ADD
    
    ADD R6, R6, -1   ; push res
    STR R0, R6, 0

    AND R0, R0, 0   ; set r0, 2
    ADD R0, R0, 2
    AND R1, R1, 0   ; set r1, 7
    ADD R1, R1, 7
    ADD R0, R0, R1  ; ADD
    
    ADD R6, R6, -1   ; push res
    STR R0, R6, 0

    LDR R0, R6, 0   ; pop R0
    ADD R6, R6, 1
    LDR R1, R6, 0   ; pop R1
    ADD R6, R6, 1
    JSR MULT        ; MULT

    ADD R6, R6, -1   ; push res
    STR R0, R6, 0

    LDR R0, R6, 0   ; pop R0
    ADD R6, R6, 1
    AND R1, R1, 0   ; set r1, 3
    ADD R1, R1, 3
    ADD R0, R0, R1  ; ADD
    
    ADD R6, R6, -1   ; push res
    STR R0, R6, 0

    ; THE RESULT IS IN R0

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