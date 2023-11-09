abort:
    jr $ra
type_name:
    jr $ra
copy:
    jr $ra
length:
    jr $ra
concat:
    jr $ra
substr:
    jr $ra
out_string:
    jr $ra
out_int:
    jr $ra
out_int:
    jr $ra
in_string:
    jr $ra
in_int:
    jr $ra
count:
    li $t1, 1
    jr $ra
main:
    move $fp, $sp
    li $t1, 5
    move $v0, $t0
    li $v0, 10
    syscall