.data
    Uno_vtable: .word count, sum  # Vtable para la clase Uno
    object: .space 4              # Espacio para el objeto Uno
    inputNumber: .space 4         # Espacio para almacenar el entero leído

.text
    .globl main

# Constructor para Uno
Uno_constructor:
    # Almacenar la dirección del vtable en el objeto
    la $t0, Uno_vtable
    sw $t0, object
    jr $ra

# Método count de Uno
count:
    li $v0, 1    # syscall para imprimir un entero
    syscall
    jr $ra

# Método sum de Uno
sum:
    li $v0, 1    # syscall para imprimir un entero
    syscall
    jr $ra

# Función principal
main:
    # Crear un nuevo objeto Uno
    jal Uno_constructor

    # Leer un entero desde la entrada estándar
    li $v0, 5    # Syscall para leer un entero
    syscall
    sw $v0, inputNumber  # Almacenar el entero leído en 'inputNumber'

    # Llamar al método count de Uno
    lw $a0, inputNumber  # Cargar el valor leído en $a0
    lw $t0, object       # Cargar la dirección de la vtable de Uno
    lw $t1, 0($t0)       # Cargar la dirección de 'count'
    jalr $t1             # Llamar a count

    # Llamar al método sum de Uno con el valor 5
    li $a0, 7           # Cargar 5 en $a0
    lw $t0, object       # Cargar la dirección de la vtable de Uno
    lw $t1, 4($t0)       # Cargar la dirección de 'sum' (offset 4)
    jalr $t1             # Llamar a sum

    # Finalizar el programa
    li $v0, 10
    syscall
