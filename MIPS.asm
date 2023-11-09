main:
    move $fp, $sp
    li $t0, 1
    li $t1, 1
    add $t2, $t0, $t1
    move $v0, $t0
    li $v0, 10
    syscall