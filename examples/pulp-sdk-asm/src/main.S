.globl main
main:

li t3, 0x0

LOOP:
    addi t3, t3, 5
    addi t3, t3, -2
    andi t3, t3, 10
    beq  zero, zero, LOOP
    nop
.end