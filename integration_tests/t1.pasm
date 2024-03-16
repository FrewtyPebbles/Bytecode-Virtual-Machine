# Adds the numbers 10 AND 11 and prints the result
START
# create the numbers
NUM num1 10
NUM num2 11
NUM precision 0

# add the numbers

ADD num3 num1 num2

# format the number to look like an integer

FMT_NUM fmt_num1 num3 precision

# create the message

STR str1 "10 + 11 = {}\n"

# format it

FMT fmt1 str1 fmt_num1

# print the msg

STDOUT fmt1