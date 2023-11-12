.data
	input_prompt: .asciiz "Ingrese el numero: "
	input_number: .word 0
	string_buffer: .space 256
	 Uno_vtable: .word count
	 object_Uno: .word 4
.text
	.globl main
Uno_constructor:
	la $t0, Uno_vtable
	sw $t0, object_Uno
	jr $ra
count:
	li $t0, 1
	add $t1, $initial, $t0
	move $v0, $t0
	jr $ra
li $v0, 9
li $a0, 4
syscall
move $t0, $v0
la $t0, Uno_vtable
sw $t0, 0($t0)
main:
	move $fp, $sp
	li $t1, 5
	move $v0, $t0
	li $v0, 10
	syscall