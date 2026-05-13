# simulators.py

# This file contains two simplified CPU architecture simulators:
#   1. CISC Simulator  → x86-style architecture
#   2. RISC Simulator  → MIPS-style architecture
#
# The purpose of these simulators is educational.
# They demonstrate how different instruction set architectures execute
# instructions, access memory, and consume CPU cycles.
#
# CISC = Complex Instruction Set Computer
# RISC = Reduced Instruction Set Computer
# =============================================================================

class CISC:
    # CISC instructions have variable lengths and cycle costs depending on complexity.
    # Operations touching memory (or complex math) logically take more cycles.
    """x86-style CISC simulator — supports memory operands in most instructions"""
    CYCLE_COST = {'MOV':2,'ADD':3,'SUB':3,'IMUL':4,'INC':1,'DEC':1,'PUSH':2,'POP':2,'NOP':1}

    def __init__(self):
        self.R = {'EAX':0,'EBX':0,'ECX':0,'EDX':0,'ESI':0,'EDI':0}
        self.M = {}
        self.cycles = 0
        self.log = []

    def _get(self, tok):
        tok = tok.strip().rstrip(',')
        if tok.startswith('[') and tok.endswith(']'):
            addr = int(tok[1:-1]) if tok[1:-1].lstrip('-').isdigit() else self.R.get(tok[1:-1],0)
            return ('m', addr, self.M.get(addr, 0))
        if tok.lstrip('-').isdigit(): return ('i', int(tok), int(tok))
        if tok in self.R: return ('r', tok, self.R[tok])
        return ('i', 0, 0)

    def _set(self, tok, val):
        tok = tok.strip().rstrip(',')
        if tok.startswith('[') and tok.endswith(']'):
            addr = int(tok[1:-1]) if tok[1:-1].lstrip('-').isdigit() else self.R.get(tok[1:-1],0)
            self.M[addr] = val
        elif tok in self.R:
            self.R[tok] = val

    def run(self, src):
        self.__init__()
        instrs, n = 0, 0
        lines = [l.strip() for l in src.splitlines()]
        for line in lines:
            if not line or line.startswith(';'): continue
            if line.endswith(':'): continue
            tok = line.split(None, 2)
            op = tok[0].upper()
            cost = self.CYCLE_COST.get(op, 2)
            try:
                if op == 'DATA':
                    a,v = int(tok[1].rstrip(',')), int(tok[2])
                    self.M[a] = v
                    self.log.append(f'  init  MEM[{a}] ← {v}')
                elif op == 'MOV' and len(tok)>=3:
                    _,dv = self._get(tok[1]), self._get(tok[2])
                    self._set(tok[1], dv[2])
                    self.log.append(f'  MOV   {tok[1].rstrip(",")} ← {dv[2]}')
                    self.cycles += cost; instrs += 1
                elif op == 'ADD' and len(tok)>=3:
                    dkind,dk,dv = self._get(tok[1])
                    skind,sk,sv = self._get(tok[2])
                    result = dv + sv
                    self._set(tok[1], result)
                    self.log.append(f'  ADD   {tok[1].rstrip(",")} = {dv} + {sv} → {result}')
                    self.cycles += cost; instrs += 1
                elif op == 'SUB' and len(tok)>=3:
                    dkind,dk,dv = self._get(tok[1])
                    skind,sk,sv = self._get(tok[2])
                    result = dv - sv
                    self._set(tok[1], result)
                    self.log.append(f'  SUB   {tok[1].rstrip(",")} = {dv} - {sv} → {result}')
                    self.cycles += cost; instrs += 1
                elif op == 'IMUL' and len(tok)>=3:
                    dkind,dk,dv = self._get(tok[1])
                    skind,sk,sv = self._get(tok[2])
                    result = dv * sv
                    self._set(tok[1], result)
                    self.log.append(f'  IMUL  {tok[1].rstrip(",")} = {dv} × {sv} → {result}')
                    self.cycles += cost; instrs += 1
                elif op == 'INC':
                    _,_,v = self._get(tok[1])
                    self._set(tok[1], v+1)
                    self.log.append(f'  INC   {tok[1]} → {v+1}')
                    self.cycles += cost; instrs += 1
                elif op == 'DEC':
                    _,_,v = self._get(tok[1])
                    self._set(tok[1], v-1)
                    self.log.append(f'  DEC   {tok[1]} → {v-1}')
                    self.cycles += cost; instrs += 1
                elif op == 'NOP':
                    self.log.append('  NOP')
                    self.cycles += 1; instrs += 1
            except Exception as e:
                self.log.append(f'  ERR   {line}: {e}')
        return instrs, self.cycles, self.R, self.M, self.log


class RISC:
    # RISC instructions are designed to generally complete in 1 cycle,
    # except for memory accesses which typically take more (here, modeled as 2).
    """MIPS-style RISC simulator — load/store architecture"""
    CYCLE_COST = {'MOV':1,'LOAD':2,'STORE':2,'ADD':1,'SUB':1,'MUL':1,'AND':1,'OR':1,'NOP':1}

    def __init__(self):
        self.R = {f'R{i}':0 for i in range(8)}
        self.M = {}
        self.cycles = 0
        self.log = []

    def _reg(self, t): return self.R.get(t.strip().rstrip(','), 0)

    def run(self, src):
        self.__init__()
        instrs = 0
        for line in src.splitlines():
            line = line.strip()
            if not line or line.startswith('#'): continue
            tok = line.split()
            op = tok[0].upper()
            cost = self.CYCLE_COST.get(op, 1)
            try:
                if op == 'DATA':
                    a,v = int(tok[1].rstrip(',')), int(tok[2])
                    self.M[a] = v
                    self.log.append(f'  init  MEM[{a}] ← {v}')
                elif op == 'MOV':
                    v = int(tok[2].lstrip('#'))
                    self.R[tok[1].rstrip(',')] = v
                    self.log.append(f'  MOV   {tok[1].rstrip(",")} ← #{v}')
                    self.cycles += cost; instrs += 1
                elif op == 'LOAD':
                    addr = int(tok[2])
                    v = self.M.get(addr, 0)
                    self.R[tok[1].rstrip(',')] = v
                    self.log.append(f'  LOAD  {tok[1].rstrip(",")} ← MEM[{addr}] = {v}')
                    self.cycles += cost; instrs += 1
                elif op == 'STORE':
                    addr = int(tok[2])
                    v = self._reg(tok[1])
                    self.M[addr] = v
                    self.log.append(f'  STORE MEM[{addr}] ← {tok[1].rstrip(",")} = {v}')
                    self.cycles += cost; instrs += 1
                elif op in ('ADD','SUB','MUL','AND','OR'):
                    rd = tok[1].rstrip(',')
                    a, b = self._reg(tok[2]), self._reg(tok[3])
                    result = {'ADD':a+b,'SUB':a-b,'MUL':a*b,'AND':a&b,'OR':a|b}[op]
                    self.R[rd] = result
                    sym = {'ADD':'+','SUB':'-','MUL':'×','AND':'&','OR':'|'}[op]
                    self.log.append(f'  {op:<5} {rd} = {a} {sym} {b} → {result}')
                    self.cycles += cost; instrs += 1
                elif op == 'NOP':
                    self.log.append('  NOP')
                    self.cycles += 1; instrs += 1
            except Exception as e:
                self.log.append(f'  ERR   {line}: {e}')
        return instrs, self.cycles, self.R, self.M, self.log