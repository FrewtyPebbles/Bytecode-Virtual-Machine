# Calculates numbers with unordered operations.
NUM result 0
NUM curr_val 0

STR eq_disp ""

STR add_str "+"
STR sub_str "-"
STR mul_str "*"
STR div_str "/"
STR eq_str "="
STR input ""
STR op ""

# Helper blocks
BLOCK add
    ADD result result curr_val
JUMP get_operation

BLOCK sub
    SUB result result curr_val
JUMP get_operation

BLOCK mul
    MUL result result curr_val
JUMP get_operation

BLOCK div
    DIV result result curr_val
JUMP get_operation

BLOCK get_operation
    STDOUT eq_disp
    STDIN op
    EQ eq_cond op eq_str
    COND_JUMP eq eq_cond
    ADD eq_disp eq_disp op
JUMP get_input_num

BLOCK get_input_num
    STDOUT eq_disp
    STDIN input
    ADD eq_disp eq_disp input
    CAST_NUM curr_val input
JUMP conds

START
    STDIN original_val
    ADD eq_disp eq_disp original_val
    CAST_NUM result original_val
    
    JUMP get_operation

    BLOCK conds
        # Operators
        ## add
        EQ add_cond op add_str
        COND_JUMP add add_cond

        ## sub
        EQ sub_cond op sub_str
        COND_JUMP sub sub_cond

        ## mul
        EQ mul_cond op mul_str
        COND_JUMP mul mul_cond

        ## div
        EQ div_cond op div_str
        COND_JUMP div div_cond

    BLOCK eq
        STR str_result "{} = {}\n"
        FMT str_result str_result eq_disp result
        STDOUT str_result