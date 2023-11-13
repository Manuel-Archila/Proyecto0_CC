.data
	input_prompt: .asciiz "Ingrese el numero: "
	input_number: .word 0
	string_buffer: .space 256
.text
	.globl main
main:
	move $fp, $sp
	li $t0, 2
	li $t1, 6
	add $t2, $t0, $t1
	move $v0, $t0
	li $v0, 10
	syscall