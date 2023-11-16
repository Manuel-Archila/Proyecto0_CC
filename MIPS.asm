.data
	input_prompt: .asciiz "Ingrese el numero: "
	input_number: .word 0
	stringy: .space 256
	string_buffer: .space 256
	inty: .word 4
	IO_vtable: .word in_int, out_int, in_string, out_string
	object_IO: .word 4
	Uno_vtable: .word sum, count, contar
	object_Uno: .word 4
	Uno_x: .word 4
	init: .word 4
	inil: .word 4
	initial: .word 4
	ini: .word 4
	mas: .word 4
	pas: .word 4
.text
	.globl main
IO_constructor:
	la $t0, IO_vtable
	sw $t0, object_IO
	jr $ra
Uno_constructor:
	la $t0, Uno_vtable
	sw $t0, object_Uno
	li $t0, 0
	sw $t0, Uno_x
	jr $ra
in_int:
	li $v0, 4
	la $a0, input_prompt
	syscall
	li $v0, 5
	syscall
	sw $v0, input_number
	jr $ra
out_int:
	li $v0, 1
	lw $a0, inty
	syscall
	jr $ra
in_string:
	li $v0, 8
	la $a0, string_buffer
	li $a1, 256
	syscall
	jr $ra
out_string:
	li $v0, 4
	lw $a0, string_buffer
	syscall
	jr $ra
sum:
	la $t5, init
	lw $t6, 0($t5)
	la $t7, inil
	lw $t8, 0($t7)
	sub $t0, $t6, $t8
	move $v0, $t0
	jr $ra
count:
	la $t5, initial
	lw $t6, 0($t5)
	la $t7, ini
	lw $t8, 0($t7)
	add $t0, $t6, $t8
	move $v0, $t0
	jr $ra
contar:
    jal in_int            # Llama directamente a in_int
    sw $v0, Uno_x         # Almacena el resultado en Uno_x

    lw $a0, Uno_x         # Carga el valor almacenado en Uno_x
    li $v0, 1             # Configura v0 para la llamada a syscall para imprimir
    syscall               # Imprime el valor de a0

    jr $ra                # Retorna de la función
main:
	move $fp, $sp
	jal IO_constructor
	jal Uno_constructor
	li $t1, 3
	li $t2, 3
	la $t0, mas
	sw $t1, 0($t0)
	la $t0, pas
	sw $t1, 0($t0)
	lw $t0, object_Uno
	lw $t1, 8($t0)
	jalr $t1
	move $v0, $t0
	li $v0, 10
	syscall