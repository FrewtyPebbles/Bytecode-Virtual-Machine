import sys
from . import bytecodes as bc
import numpy as np

class ScopeStack:
    def __init__(self) -> None:
        self.stack:list[dict[int, int | float | str | bool]] = [{}]

    @property
    def top(self):
        return self.stack[-1]
    
    def new_scope(self):
        self.stack.append({})
    
    def alloca(self, key:int):
        self.top[key] = None
    
    def set(self, key:int, val:any):
        self.top[key] = val
    
    def get(self, key:int):
        for scope in reversed(self.stack):
            if key in scope.keys():
                return scope[key]
        raise RuntimeError(f"Unknown memory {key} referenced.")
    
    def remove(self, key:int):
        for scope in reversed(self.stack):
            if key in scope.keys():
                del scope[key]
                return
        raise RuntimeError(f"Tried to delete memory {key} which does not exist.")
    
    def pop_scope(self):
        self.stack.pop()

class ByteCursor:
    def __init__(self, src:bc.ByteCode) -> None:
        self.src = src
        self.cursor = -1

    def next(self):
        if self.finished:
            self.cursor = -1
            raise StopIteration
        self.cursor += 1
        
        return self.src[self.cursor]
    
    def __getitem__(self, ind):
        self.cursor = ind
        ret = self.src[ind]
        return ret

    def __next__(self):
        return self.next()
    
    def prev(self):
        self.cursor -= 1
        return self.src[self.cursor]
    
    def jump(self, ind:int):
        self.cursor = ind

    @property
    def current(self):
        return self.src[self.cursor]
    
    @property
    def finished(self):
        return self.cursor+1 == len(self.src)

class Executor:
    """Runs the supplied bytecode."""
    def __init__(self, bytecode:list[int | str]) -> None:
        self.blocks:dict[int, int] = {}
        """
        Each block name is associated with an integer which
        tells the bytecode parser where to jump to.
        """
        self.bytecode = ByteCursor(bytecode)
        """
        This is the raw bytecode that is interpreted by the executor.
        """
        self.stack = ScopeStack()

    def run(self, metadata:dict):
        """
        Runs the bytecode contained within the executor.
        
        metadata is the cli args and related things.

        """
        for byt in self.bytecode:
            if byt == bc.BLOCK:
                self._block()
        
        self.bytecode.cursor = -1
        
        start = False
        while not self.bytecode.finished:
            byt = self.bytecode.next()
            if start:
                match byt:
                    case bc.ENDL:
                        pass
                    case bc.ALLOCA:
                        self._alloca()
                    case bc.STORE:
                        self._store()
                    case bc.DEL:
                        self._del()
                    case bc.EQ:
                        self._eq()
                    case bc.GT:
                        self._gt()
                    case bc.GTE:
                        self._gte()
                    case bc.LT:
                        self._lt()
                    case bc.LTE:
                        self._lte()
                    case bc.NEQ:
                        self._neq()
                    case bc.ADD:
                        self._add()
                    case bc.SUB:
                        self._sub()
                    case bc.MUL:
                        self._mul()
                    case bc.DIV:
                        self._div()
                    case bc.MOD:
                        self._mod()
                    case bc.EXP:
                        self._exp()
                    case bc.NUM:
                        self._num()
                    case bc.STR:
                        self._str()
                    case bc.FMT:
                        self._fmt()
                    case bc.STDOUT:
                        self._stdout()
                    case bc.STDIN:
                        self._stdin()
                    case bc.BEGIN_SCOPE:
                        self.stack.new_scope()
                    case bc.END_SCOPE:
                        self.stack.pop_scope()
                    case bc.BLOCK:
                        self._block()
                    case bc.JUMP:
                        self._jump()
                    case bc.COND_JUMP:
                        self._cond_jump()
                    case bc.CAST_STR:
                        self._cast_str()
                    case bc.CAST_NUM:
                        self._cast_num()
                    case bc.FMT_NUM:
                        self._fmt_num()
                    case _:
                        pass
            else:
                match byt:
                    case bc.ALLOCA:
                        self._alloca()
                    case bc.NUM:
                        self._num()
                    case bc.STR:
                        self._str()
                    case bc.START:
                        start = True
    
    def _alloca(self):
        self.stack.alloca(next(self.bytecode))
        next(self.bytecode)

    def _store(self):
        self.stack.set(next(self.bytecode), self.stack.get(next(self.bytecode)))
        next(self.bytecode)

    def _del(self):
        self.stack.remove(next(self.bytecode))
        next(self.bytecode)
    
    def _eq(self):
        self.stack.set(next(self.bytecode), self.stack.get(next(self.bytecode)) == self.stack.get(next(self.bytecode)))
        next(self.bytecode)

    def _gt(self):
        self.stack.set(next(self.bytecode), self.stack.get(next(self.bytecode)) > self.stack.get(next(self.bytecode)))
        next(self.bytecode)

    def _lt(self):
        self.stack.set(next(self.bytecode), self.stack.get(next(self.bytecode)) < self.stack.get(next(self.bytecode)))
        next(self.bytecode)

    def _gte(self):
        self.stack.set(next(self.bytecode), self.stack.get(next(self.bytecode)) >= self.stack.get(next(self.bytecode)))
        next(self.bytecode)
    
    def _lte(self):
        self.stack.set(next(self.bytecode), self.stack.get(next(self.bytecode)) <= self.stack.get(next(self.bytecode)))
        next(self.bytecode)
    
    def _neq(self):
        self.stack.set(next(self.bytecode), self.stack.get(next(self.bytecode)) != self.stack.get(next(self.bytecode)))
        next(self.bytecode)

    def _add(self):
        cid = next(self.bytecode)
        var1 = self.stack.get(next(self.bytecode))
        var2 = self.stack.get(next(self.bytecode))
        self.stack.set(cid, var1 + var2)
        next(self.bytecode)
    
    def _sub(self):
        self.stack.set(next(self.bytecode), self.stack.get(next(self.bytecode)) - self.stack.get(next(self.bytecode)))
        next(self.bytecode)

    def _mul(self):
        self.stack.set(next(self.bytecode), self.stack.get(next(self.bytecode)) * self.stack.get(next(self.bytecode)))
        next(self.bytecode)
    
    def _div(self):
        self.stack.set(next(self.bytecode), self.stack.get(next(self.bytecode)) / self.stack.get(next(self.bytecode)))
        next(self.bytecode)

    def _mod(self):
        self.stack.set(next(self.bytecode), self.stack.get(next(self.bytecode)) % self.stack.get(next(self.bytecode)))
        next(self.bytecode)

    def _exp(self):
        self.stack.set(next(self.bytecode), self.stack.get(next(self.bytecode)) ** self.stack.get(next(self.bytecode)))
        next(self.bytecode)
    
    def _stdin(self):
        cid = next(self.bytecode)
        self.stack.set(cid, input())
        next(self.bytecode)
    
    def _stdout(self):
        sys.stdout.write(str(self.stack.get(next(self.bytecode))))
        next(self.bytecode)

    def _num(self):
        cid = next(self.bytecode)
        num = ""
        while (byt := next(self.bytecode)) != bc.ENDL:
            num += f"{byt}"
        
        self.stack.set(cid, float(num))
    
    def _str(self):
        cid = next(self.bytecode)
        self.stack.set(cid, next(self.bytecode))
        next(self.bytecode) # endl
    
    def _cast_num(self):
        cid = next(self.bytecode)
        self.stack.set(cid, float(self.stack.get(next(self.bytecode))))
        next(self.bytecode) # endl

    def _fmt_num(self):
        cid = next(self.bytecode)
        num = self.stack.get(next(self.bytecode))
        precision = int(self.stack.get(next(self.bytecode)))
        if precision == 0:
            self.stack.set(cid, f"{int(num)}")
        else:
            self.stack.set(cid, f"%.{precision}f" % num)
        next(self.bytecode) # endl

    def _cast_str(self):
        cid = next(self.bytecode)
        self.stack.set(cid, str(self.stack.get(next(self.bytecode))))
        next(self.bytecode) # endl

    def _fmt(self):
        cid = next(self.bytecode)
        string:str = self.stack.get(next(self.bytecode))
        fmt_args = []
        while (byt := next(self.bytecode)) != bc.ENDL:
            fmt_args.append(self.stack.get(byt))
        self.stack.set(cid, string.format(*fmt_args))

    def _block(self):
        self.blocks[next(self.bytecode)] = self.bytecode.cursor
        next(self.bytecode)
    
    def _jump(self):
        self.bytecode.jump(self.blocks[next(self.bytecode)])

    def _cond_jump(self):
        block = next(self.bytecode)
        cond = self.stack.get(next(self.bytecode))
        if cond:
            self.bytecode.jump(self.blocks[block])
        else:
            next(self.bytecode)
    
    
