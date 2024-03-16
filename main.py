import time
from VM import BytecodeBuilder, Executor
from ASM_LANG import Parser

BB = BytecodeBuilder()

var1 = BB.write_NUM(66)
var2 = BB.write_NUM(77)
expr = BB.write_MUL(var1, BB.write_ADD(var1, BB.write_MOD(var1, var2)))
BB.write_STDOUT(BB.write_FMT(BB.write_STR("66 * (66 + (66 % 77)) = {}\n"), [expr]))

EXEC = Executor(BB.src)

t1 = time.time_ns()

EXEC.run({})

print(f"time:{(time.time_ns() - t1)/1_000_000}")

print(f"BYTES:\n{BB.src}")


print("Python Equivalent:")

t2 = time.time_ns()

print(f"66 * (66 + (66 % 77)) = {66 * (66 + (66 % 77))}")

print(f"time:{(time.time_ns() - t2)/1_000_000} ms")