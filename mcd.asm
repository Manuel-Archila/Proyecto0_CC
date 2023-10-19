.data
    num1: .word 60        # Primer número
    num2: .word 48        # Segundo número
    message1: .asciiz "El MCD de los numeros "
    message2: .asciiz " y "
    end_message: .asciiz " es "
    newline: .asciiz "\n"

.text
.globl main

main:
    # Cargar los números en registros
    lw $t0, num1         # Cargar num1 en $t0
    lw $t1, num2         # Cargar num2 en $t1

    # Imprimir el primer mensaje
    li $v0, 4            # Cargar el código de la llamada al sistema para imprimir cadena
    la $a0, message1     # Cargar la dirección del primer mensaje en $a0
    syscall

    # Imprimir num1
    li $v0, 1            # Cargar el código de la llamada al sistema para imprimir entero
    move $a0, $t0        # Cargar num1 en $a0
    syscall

    # Imprimir el mensaje de intermedio
    li $v0, 4            # Cargar el código de la llamada al sistema para imprimir cadena
    la $a0, message2     # Cargar la dirección del mensaje intermedio en $a0
    syscall

    # Imprimir num2
    li $v0, 1            # Cargar el código de la llamada al sistema para imprimir entero
    move $a0, $t1        # Cargar num2 en $a0
    syscall

calculate_gcd:
    beq $t1, $zero, done   # Si $t1 es cero, $t0 tiene el MCD
    div $t0, $t1           # Dividir $t0 por $t1. Cociente en LO, Residuo en HI
    mfhi $t2               # Cargar el residuo en $t2
    move $t0, $t1          # Mover $t1 a $t0
    move $t1, $t2          # Mover el residuo a $t1
    j calculate_gcd        # Volver al inicio del ciclo


done:
    # El resultado (MCD) está en $t0

    # Imprimir el mensaje final
    li $v0, 4            # Cargar el código de la llamada al sistema para imprimir cadena
    la $a0, end_message  # Cargar la dirección del mensaje final en $a0
    syscall

    # Imprimir el MCD
    li $v0, 1            # Cargar el código de la llamada al sistema para imprimir entero
    move $a0, $t0        # Cargar el MCD en $a0
    syscall

    # Imprimir un carácter de nueva línea
    li $v0, 4            # Cargar el código de la llamada al sistema para imprimir cadena
    la $a0, newline      # Cargar la dirección de la cadena en $a0
    syscall

    # Salir del programa
    li $v0, 10           # Cargar el código de la llamada al sistema para salir del programa
    syscall
