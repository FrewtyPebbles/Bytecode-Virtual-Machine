from typing import Iterable
from VM import BytecodeBuilder, Executor

class Parser:
    def __init__(self, src:str) -> None:
        self.src = src
        self.vars:dict[str, int] = {}

    def parse_instr(self, instr:str):
        instr:Iterable[str] = iter(instr)
        str_buff = ""
        ret_inst:list[str] = []
        for c in instr:
            match c:
                case "\"":
                    ret_inst.append(self._parse_str(instr))
                case " " | "\t" | "\r" | "\n":
                    ret_inst.append(str_buff)
                    str_buff = ""
                case _:
                    str_buff += c
        if str_buff != "":
            ret_inst.append(str_buff)
            str_buff = ""
        return ret_inst


    def _parse_str(self, instr:Iterable[str]):
        escape = False
        string = ""
        for c in instr:
            match c:
                case "\\":
                    escape = True
                case "\"":
                    if escape:
                        string += "\""
                        escape = False
                    else:
                        return string
                case "n":
                    if escape:
                        string += "\n"
                        escape = False
                    else:
                        string += "n"
                case "t":
                    if escape:
                        string += "\t"
                        escape = False
                    else:
                        string += "t"
                case _:
                    string += c




    def run(self):
        instructions = self.src.splitlines()
        BB = BytecodeBuilder()
        for instr in instructions:
            instr = instr.strip()
            if instr == "" or instr.startswith("#"):
                continue
            instr_prts = self.parse_instr(instr)
            match instr_prts[0]:
                case "ALLOCA":
                    self.vars[instr_prts[1]] = BB.write_ALLOCA()
                case "STORE":
                    BB.write_STORE(self.vars[instr_prts[1]], self.vars[instr_prts[2]])
                case "NUM":
                    self.vars[instr_prts[1]] = BB.write_NUM(int(instr_prts[2]))
                case "CAST_NUM":
                    if instr_prts[1] not in self.vars.keys():
                        self.vars[instr_prts[1]] = BB.write_CAST_NUM(self.vars[instr_prts[2]])
                    else:
                        BB.write_CAST_NUM(self.vars[instr_prts[2]], self.vars[instr_prts[1]])
                case "FMT_NUM":
                    self.vars[instr_prts[1]] = BB.write_FMT_NUM(self.vars[instr_prts[2]], self.vars[instr_prts[3]])
                case "STR":
                    self.vars[instr_prts[1]] = BB.write_STR(str(instr_prts[2]))
                case "CAST_STR":
                    if instr_prts[1] not in self.vars.keys():
                        self.vars[instr_prts[1]] = BB.write_CAST_STR(self.vars[instr_prts[2]])
                    else:
                        BB.write_CAST_STR(self.vars[instr_prts[2]], self.vars[instr_prts[1]])
                case "EQ":
                    if instr_prts[1] not in self.vars.keys():
                        self.vars[instr_prts[1]] = BB.write_EQ(self.vars[instr_prts[2]], self.vars[instr_prts[3]])
                    else:
                        BB.write_EQ(self.vars[instr_prts[2]], self.vars[instr_prts[3]], self.vars[instr_prts[1]])
                case "NEQ":
                    if instr_prts[1] not in self.vars.keys():
                        self.vars[instr_prts[1]] = BB.write_NEQ(self.vars[instr_prts[2]], self.vars[instr_prts[3]])
                    else:
                        BB.write_NEQ(self.vars[instr_prts[2]], self.vars[instr_prts[3]], self.vars[instr_prts[1]])
                case "GT":
                    if instr_prts[1] not in self.vars.keys():
                        self.vars[instr_prts[1]] = BB.write_GT(self.vars[instr_prts[2]], self.vars[instr_prts[3]])
                    else:
                        BB.write_GT(self.vars[instr_prts[2]], self.vars[instr_prts[3]], self.vars[instr_prts[1]])
                case "LT":
                    if instr_prts[1] not in self.vars.keys():
                        self.vars[instr_prts[1]] = BB.write_LT(self.vars[instr_prts[2]], self.vars[instr_prts[3]])
                    else:
                        BB.write_LT(self.vars[instr_prts[2]], self.vars[instr_prts[3]], self.vars[instr_prts[1]])
                case "LTE":
                    if instr_prts[1] not in self.vars.keys():
                        self.vars[instr_prts[1]] = BB.write_LTE(self.vars[instr_prts[2]], self.vars[instr_prts[3]])
                    else:
                        BB.write_LTE(self.vars[instr_prts[2]], self.vars[instr_prts[3]], self.vars[instr_prts[1]])
                case "GTE":
                    if instr_prts[1] not in self.vars.keys():
                        self.vars[instr_prts[1]] = BB.write_GTE(self.vars[instr_prts[2]], self.vars[instr_prts[3]])
                    else:
                        BB.write_GTE(self.vars[instr_prts[2]], self.vars[instr_prts[3]], self.vars[instr_prts[1]])
                case "ADD":
                    if instr_prts[1] not in self.vars.keys():
                        self.vars[instr_prts[1]] = BB.write_ADD(self.vars[instr_prts[2]], self.vars[instr_prts[3]])
                    else:
                        BB.write_ADD(self.vars[instr_prts[2]], self.vars[instr_prts[3]], self.vars[instr_prts[1]])
                case "SUB":
                    if instr_prts[1] not in self.vars.keys():
                        self.vars[instr_prts[1]] = BB.write_SUB(self.vars[instr_prts[2]], self.vars[instr_prts[3]])
                    else:
                        BB.write_SUB(self.vars[instr_prts[2]], self.vars[instr_prts[3]], self.vars[instr_prts[1]])
                case "MUL":
                    if instr_prts[1] not in self.vars.keys():
                        self.vars[instr_prts[1]] = BB.write_MUL(self.vars[instr_prts[2]], self.vars[instr_prts[3]])
                    else:
                        BB.write_MUL(self.vars[instr_prts[2]], self.vars[instr_prts[3]], self.vars[instr_prts[1]])
                case "DIV":
                    if instr_prts[1] not in self.vars.keys():
                        self.vars[instr_prts[1]] = BB.write_DIV(self.vars[instr_prts[2]], self.vars[instr_prts[3]])
                    else:
                        BB.write_DIV(self.vars[instr_prts[2]], self.vars[instr_prts[3]], self.vars[instr_prts[1]])
                case "EXP":
                    if instr_prts[1] not in self.vars.keys():
                        self.vars[instr_prts[1]] = BB.write_EXP(self.vars[instr_prts[2]], self.vars[instr_prts[3]])
                    else:
                        BB.write_EXP(self.vars[instr_prts[2]], self.vars[instr_prts[3]], self.vars[instr_prts[1]])
                case "MOD":
                    if instr_prts[1] not in self.vars.keys():
                        self.vars[instr_prts[1]] = BB.write_MOD(self.vars[instr_prts[2]], self.vars[instr_prts[3]])
                    else:
                        BB.write_MOD(self.vars[instr_prts[2]], self.vars[instr_prts[3]], self.vars[instr_prts[1]])
                case "FMT":
                    if instr_prts[1] not in self.vars.keys():
                        self.vars[instr_prts[1]] = BB.write_FMT(self.vars[instr_prts[2]], [self.vars[arg] for arg in instr_prts[3:]])
                    else:
                        BB.write_FMT(self.vars[instr_prts[2]], [self.vars[arg] for arg in instr_prts[3:]], self.vars[instr_prts[1]])
                case "STDOUT":
                    BB.write_STDOUT(self.vars[instr_prts[1]])
                case "STDIN":
                    self.vars[instr_prts[1]] = BB.write_STDIN()
                case "BLOCK":
                    self.vars[instr_prts[1]] = BB.write_BLOCK()
                case "JUMP":
                    if instr_prts[1] in self.vars.keys():
                        BB.write_JUMP(self.vars[instr_prts[1]])
                    else:
                        BB.write_JUMP((instr_prts[1],)) # blocks that havent been created yet are wrapped in tuples
                case "START":
                    BB.write_START()
                case "COND_JUMP":
                    
                    if instr_prts[1] in self.vars.keys():
                        BB.write_COND_JUMP(self.vars[instr_prts[1]], self.vars[instr_prts[2]])
                    else:
                        BB.write_COND_JUMP((instr_prts[1],), self.vars[instr_prts[2]]) # blocks that havent been created yet are wrapped in tuples
        
        # substitute the jumps:
        for i in range(len(BB.src)):
            if isinstance(BB.src[i], tuple):
                BB.src[i] = self.vars[BB.src[i][0]]
        
        EXEC = Executor(BB.src)

        EXEC.run({})
