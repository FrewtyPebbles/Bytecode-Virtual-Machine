from __future__ import annotations
import numpy as np

"""
endline (or send instruction) is \x00 or 0 value
Format:

{instruction}{parameter}{parameter}\x00

"""

__MAX_INSTR_INT__ = 0x32
"""
There are 50 reserved bytes

40 of these bytes are instructions.

bytes 0 to 9 are reserved for representing decimal numbers.

characters are represented as their decimal value then converted as needed

this leaves 205 bytes left for variables, instructions, etc (will change later when I think of better solution)
"""

def MAX_INSTR_guard(bt:int | list[int]):
    if isinstance(bt, int):
        if 10 < bt <= __MAX_INSTR_INT__:
            raise RuntimeError(f"The byte of value {bt} is an instruction byte and cannot be used dynamically.")
    elif isinstance(bt, list):
        for byt in bt:
            if 10 < byt <= __MAX_INSTR_INT__:
                raise RuntimeError(f"The byte of value {byt} is an instruction byte and cannot be used dynamically.")

# instruction byte values
ENDL = 0xA
ALLOCA = 0xB
STORE = 0xC
DEL = 0xD
ADD = 0xE
SUB = 0xF
MUL = 0x10
DIV = 0x11
MOD = 0x12
JUMP = 0x13
BLOCK = 0x14
COND_JUMP = 0x15
EQ = 0x16
GT = 0x17
LT = 0x18
GTE = 0x19
LTE = 0x1A
NUM = 0x1B
STDOUT = 0x1C
STDIN = 0x1D
EXP = 0x1E
STR = 0x1F
FMT = 0x20
BEGIN_SCOPE = 0x21
END_SCOPE = 0x22
NEQ = 0x23
CAST_NUM = 0x24
CAST_STR = 0x25
FMT_NUM = 0x26
START = 0x27

class ByteCode:
    def __init__(self, builder:BytecodeBuilder):
        self.bytecode = []
        self.strings:dict[int, str] = {}
        self.current = 0
        self.builder:BytecodeBuilder = builder
    
    def __next__(self):
        if self.current == len(self.bytecode):
            raise StopIteration
        cur = self.bytecode[self.current]
        self.current += 1
        if cur in self.strings.keys():
            return self.strings[cur]
        else:
            return cur
        
    def __getitem__(self, index:int):
        cur = self.bytecode[index]
        if cur in self.strings.keys():
            return self.strings[cur]
        else:
            return cur
        
    def __setitem__(self, index:int, value):
        self.bytecode[index] = value
        
    def __len__(self):
        return len(self.bytecode)
    
    def append(self, item:int | str):
        if isinstance(item, str):
            cid = self.builder.current_id
            self.strings[cid] = item
            item = cid
        self.bytecode.append(item)
    
    def extend(self, items:list[int | str]):
        for i in range(len(items)):
            if isinstance(items[i], str):
                cid = self.builder.current_id
                self.strings[cid] = items[i]
                items[i] = cid
        self.bytecode.extend(items)
    


class BytecodeBuilder:
    def __init__(self) -> None:
        self._current_id = __MAX_INSTR_INT__
        self.existing_ids:set = set()
        self.src = ByteCode(self)
    
    @property
    def current_id(self):
        self._current_id += 0x1
        while self._current_id in self.existing_ids:
            self._current_id += 0x1
        return self._current_id
    
    def add_id(self, id:int):
        if id in self.existing_ids:
            raise RuntimeError(f"The dynamic id {id} was instantiated twice.")
        self.existing_ids.add(id)
    
    def remove_id(self, id:int):
        if id in self.existing_ids:
            raise RuntimeError(f"The dynamic id {id} was deleted twice.")
        self.existing_ids.remove(id)
    
    def write_EQ(self, lhs:int, rhs:int, cid = None):
        MAX_INSTR_guard([lhs, rhs])
        cid = self.current_id if cid == None else cid

        self.src.extend([EQ, cid, lhs, rhs, ENDL])
        return cid

    def write_GT(self, lhs:int, rhs:int, cid = None):
        MAX_INSTR_guard([lhs, rhs])
        cid = self.current_id if cid == None else cid

        self.src.extend([GT, cid, lhs, rhs, ENDL])
        return cid

    def write_LT(self, lhs:int, rhs:int, cid = None):
        MAX_INSTR_guard([lhs, rhs])
        cid = self.current_id if cid == None else cid

        self.src.extend([LT, cid, lhs, rhs, ENDL])
        return cid

    def write_GTE(self, lhs:int, rhs:int, cid = None):
        MAX_INSTR_guard([lhs, rhs])
        cid = self.current_id if cid == None else cid

        self.src.extend([GTE, cid, lhs, rhs, ENDL])
        return cid

    def write_LTE(self, lhs:int, rhs:int, cid = None):
        MAX_INSTR_guard([lhs, rhs])
        cid = self.current_id if cid == None else cid

        self.src.extend([LTE, cid, lhs, rhs, ENDL])
        return cid
    
    def write_NEQ(self, lhs:int, rhs:int, cid = None):
        MAX_INSTR_guard([lhs, rhs])
        cid = self.current_id if cid == None else cid

        self.src.extend([NEQ, cid, lhs, rhs, ENDL])
        return cid

    def write_ALLOCA(self, id:int = None, cid = None):
        if id != None:
            MAX_INSTR_guard(id)
            self.add_id(id)

            self.src.extend([ALLOCA, id, ENDL])
            return id
        else:
            cid = self.current_id if cid == None else cid
            self.src.extend([ALLOCA, cid, ENDL])
            return cid
            

    def write_STORE(self, id:int, value:int):
        MAX_INSTR_guard([id, value])

        self.src.extend([STORE, id, value, ENDL])
        return id

    def write_DEL(self, id:int):
        MAX_INSTR_guard(id)
        self.remove_id(id)
        
        self.src.extend([DEL, id, ENDL])
        return id

    def write_ADD(self, lhs:int, rhs:int, cid:int = None):
        MAX_INSTR_guard([lhs, rhs])
        cid = self.current_id if cid == None else cid

        self.src.extend([ADD, cid, lhs, rhs, ENDL])
        return cid

    def write_SUB(self, lhs:int, rhs:int, cid = None):
        MAX_INSTR_guard([lhs, rhs])
        cid = self.current_id if cid == None else cid

        self.src.extend([SUB, cid, lhs, rhs, ENDL])
        return cid

    def write_MUL(self, lhs:int, rhs:int, cid = None):
        MAX_INSTR_guard([lhs, rhs])
        cid = self.current_id if cid == None else cid

        self.src.extend([MUL, cid, lhs, rhs, ENDL])
        return cid

    def write_DIV(self, lhs:int, rhs:int, cid = None):
        MAX_INSTR_guard([lhs, rhs])
        cid = self.current_id if cid == None else cid

        self.src.extend([DIV, cid, lhs, rhs, ENDL])
        return cid
    
    def write_EXP(self, lhs:int, rhs:int, cid = None):
        MAX_INSTR_guard([lhs, rhs])
        cid = self.current_id if cid == None else cid

        self.src.extend([EXP, cid, lhs, rhs, ENDL])
        return cid

    def write_MOD(self, lhs:int, rhs:int, cid = None):
        MAX_INSTR_guard([lhs, rhs])
        cid = self.current_id if cid == None else cid

        self.src.extend([MOD, cid, lhs, rhs, ENDL])
        return cid

    def write_JUMP(self, block:int):
        MAX_INSTR_guard(block)

        self.src.extend([JUMP, block])
        return block

    def write_COND_JUMP(self, block:int, cond:int):

        self.src.extend([COND_JUMP, block, cond, ENDL])
        return block

    def write_BLOCK(self, cid = None):
        cid = self.current_id if cid == None else cid
        
        self.src.extend([BLOCK, cid, ENDL])
        return cid
    
    def write_BEGIN_SCOPE(self):
        self.src.append(BEGIN_SCOPE)
    
    def write_START(self):
        self.src.append(START)

    def write_END_SCOPE(self):
        self.src.append(END_SCOPE)
    
    def write_NUM(self, num:int, cid = None):
        num = [int(i) for i in str(num)]

        cid = self.current_id if cid == None else cid
        
        self.src.extend([NUM, cid, *num, ENDL])
        return cid
    
    def write_CAST_NUM(self, id:int, cid = None):

        cid = self.current_id if cid == None else cid
        
        self.src.extend([CAST_NUM, cid, id, ENDL])
        return cid
    
    def write_CAST_STR(self, id:int, cid = None):

        cid = self.current_id if cid == None else cid
        
        self.src.extend([CAST_STR, cid, id, ENDL])
        return cid
    
    def write_STR(self, string:str, cid = None):

        cid = self.current_id if cid == None else cid
        
        self.src.extend([STR, cid, string, ENDL])
        return cid
    
    def write_FMT(self, string:int, items:list, cid = None):
        """
        string looks like "words{}words"

        items are placed in the {}s
        """

        cid = self.current_id if cid == None else cid
        
        self.src.extend([FMT, cid, string, *items, ENDL])
        return cid

    def write_FMT_NUM(self, num:int, precision:int, cid = None):
        """
        string looks like "words{}words"

        items are placed in the {}s
        """

        cid = self.current_id if cid == None else cid
        
        self.src.extend([FMT_NUM, cid, num, precision, ENDL])
        return cid
    
    def write_STDOUT(self, out:int):
        self.src.extend([STDOUT, out, ENDL])

    def write_STDIN(self, cid = None):

        cid = self.current_id if cid == None else cid
        
        self.src.extend([STDIN, cid, ENDL])
        return cid

