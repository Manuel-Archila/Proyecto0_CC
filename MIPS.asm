.data
	input_prompt: .asciiz "Ingrese el numero: "
	input_number: .word 0
	stringy: .space 256
	string_buffer: .space 256
	inty: .word 4
	IO_vtable: .word in_int, out_int, in_string, out_string
	object_IO: .word 4
	Dos_vtable: .word count
	object_Dos: .word 4
	initial: .word 4
	Uno_vtable: .word 0
	object_Uno: .word 4
.text
	.globl main
IO_constructor:
	la $t0, IO_vtable
	sw $t0, object_IO
	jr $ra
Dos_constructor:
	la $t0, Dos_vtable
	sw $t0, object_Dos
	jr $ra
Uno_constructor:
	la $t0, Uno_vtable
	sw $t0, object_Uno
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
count:
	lw $t0, initial
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
	li $t1, 5
	la $t0, initial
	sw $t1, 0($t0)
	lw $t0, object_Uno
	lw $t1, 0($t0)
	jalr $t1
	li $v0, 10
	syscall