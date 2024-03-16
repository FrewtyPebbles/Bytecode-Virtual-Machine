import sys
from ASM_LANG import Parser
import time

with open(sys.argv[1], "r") as srcf:
    t1 = time.time_ns()
    Parser(srcf.read()).run()
    print(f"finished:{(time.time_ns() - t1)/1_000_000} ms")