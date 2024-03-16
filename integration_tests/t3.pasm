# Prompts for 2 numbers then evaluates num1**num2 and prints
START
NUM precision 0

# num1 prompt
STR prompt1 "Enter a num:"
STDOUT prompt1
STDIN num1in
CAST_NUM num1 num1in

# num2 prompt
STR prompt2 "Enter a num:"
STDOUT prompt2
STDIN num2in
CAST_NUM num2 num2in

# exponent
EXP num3 num1 num2
STR result "{}^{} = {}\n"

#FMT THE NUMS
    FMT_NUM fmt_num1 num1 precision
    FMT_NUM fmt_num2 num2 precision
    FMT_NUM fmt_num3 num3 precision

FMT fmt_result result fmt_num1 fmt_num2 fmt_num3
STDOUT fmt_result