.data
prompt1: .asciiz "Introduce el primer numero: "
prompt2: .asciiz "Introduce el segundo numero: "
resultMsg: .asciiz "El MCD es: "

.text
.globl main

main:
    # Solicitar el primer número
    li $v0, 4
    la $a0, prompt1
    syscall

    # Leer el primer número
    li $v0, 5
    syscall
    move $a0, $v0

    # Solicitar el segundo número
    li $v0, 4
    la $a0, prompt2
    syscall

    # Leer el segundo número
    li $v0, 5
    syscall
    move $a1, $v0

    # Llamada a la función GCD
    jal GCD

    # Imprimir "El MCD es: "
    li $v0, 4
    la $a0, resultMsg
    syscall

    # Imprimir resultado
    move $a0, $v0
    li $v0, 1
    syscall

    # Salir del programa
    li $v0, 10
    syscall

GCD:
    addi $sp, $sp, -12
    sw $ra, 0($sp)
    sw $s0, 4($sp)
    sw $s1, 8($sp)

    move $s0, $a0
    move $s1, $a1

    beq $s1, $zero, returnn1

    move $a0, $s1
    div $s0, $s1
    mfhi $a1 # $a1 ahora tiene el residuo de la división

    move $s0, $s1
    move $s1, $a1
    jal GCD

exitGCD:
    lw $ra, 0($sp)
    lw $s0, 4($sp)
    lw $s1, 8($sp)
    addi $sp, $sp, 12
    jr $ra

returnn1:
    move $v0, $s0
    j exitGCD
