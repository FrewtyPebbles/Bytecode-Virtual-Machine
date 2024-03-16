# Loops and prints numbers 1 to 1000
NUM ind 1
NUM max 1000
NUM inc 1
NUM precision 0
NUM divisor 2

START
    BLOCK loop_start

        # print the itteration
        STR msg_raw "itteration #{}\n"
        DIV ind_res ind divisor
        FMT_NUM current_ind ind_res precision
        FMT msg msg_raw current_ind
        STDOUT msg

        # check if ind == max
        NEQ finished ind max
        # increment
        ADD new_ind ind inc
        STORE ind new_ind
    COND_JUMP loop_start finished

    STR fin_msg "Done!\n"
    STDOUT fin_msg