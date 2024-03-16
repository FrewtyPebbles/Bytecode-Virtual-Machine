# Prompts for name then says hello
START
# the prompt
STR prompt "Enter your Name:"
STDOUT prompt
STDIN name

STR greeting "Hello {}!\n"
FMT fmt_greeting greeting name
STDOUT fmt_greeting