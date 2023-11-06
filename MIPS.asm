main:
    move $fp, $sp
    li $t1, 1
    li $t2, 9
    add $t0, $t1, $t2
    move $v0, $t0
    li $v0, 10
    syscall