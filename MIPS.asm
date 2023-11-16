.data
	input_prompt: .asciiz "Ingrese el numero: "
	input_number: .word 0
	stringy: .space 256
	string_buffer: .space 256
	inty: .word 4
	IO_vtable: .word in_int, out_int, in_string, out_string
	object_IO: .word 4
	Uno_vtable: .word prueba, suma, contar
	object_Uno: .word 12
	Uno_x: .word 4
	Uno_y: .word 4
	Uno_z: .word 4
	initial: .word 4
	ini: .word 4
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
	li $t0, 0
	sw $t0, Uno_y
	li $t0, 0
	sw $t0, Uno_z
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
prueba:
	lw $t0, object_IO
	lw $t1, 0($t0)
	jalr $t1
	lw $t0, input_number
	sw $t0, Uno_x
	lw $t0, object_IO
	lw $t1, 0($t0)
	jalr $t1
	lw $t0, input_number
	sw $t0, Uno_y
	lw $t0, object_IO
	lw $t1, 0($t0)
	jalr $t1
	lw $t0, input_number
	sw $t0, Uno_z
	la $t5, Uno_x
	lw $t6, 0($t5)
	la $t7, Uno_y
	lw $t8, 0($t7)
	add $t3, $t6, $t8
	jr $ra
suma:
	la $t5, initial
	lw $t6, 0($t5)
	la $t7, ini
	lw $t8, 0($t7)
	add $t0, $t6, $t8
	jr $ra
contar:
	lw $t0, object_IO
	lw $t1, 0($t0)
	jalr $t1
	lw $t0, input_number
	sw $t0, Uno_x
	lw $t0, Uno_x
	sw $t0, inty
	lw $a0, inty
	lw $t0, object_IO
	lw $t1, 4($t0)
	jalr $t1
	jr $ra
main:
	move $fp, $sp
	jal IO_constructor
	jal Uno_constructor
	lw $t0, object_Uno
	lw $t1, 0($t0)
	jalr $t1
	li $v0, 10
	syscall