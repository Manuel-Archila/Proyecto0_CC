.data
	input_prompt: .asciiz "Ingrese el numero: "
	input_number: .word 0
	string_buffer: .space 256
	Uno_vtable: .word count
	object_Uno: .word 4
	initial: .word 4
.text
	.globl main
Uno_constructor:
	la $t0, Uno_vtable
	sw $t0, object_Uno
	jr $ra
count:
	li $t0, 4
	la $t5, initial
	lw $t6, 0($t5)
	add $t1, $t6, $t0
	move $v0, $t0
	jr $ra
main:
	move $fp, $sp
	jal Uno_constructor
	li $t1, 2
	la $t0, initial
	sw $t1, 0($t0)
	lw $t0, object_Uno
	lw $t1, 0($t0)
	jalr $t1
	move $v0, $t0
	li $v0, 10
	syscall