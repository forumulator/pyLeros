from myhdl import enum, Signal


class decSignal():
    def __init__(self):
        self.ah_ena = Signal(bool(0))
        self.al_ena = Signal(bool(0))
        self.log_add = Signal(bool(0))
        self.add_sub = Signal(bool(0))
        self.shr = Signal(bool(0))
        self.sel_imm = Signal(bool(0))
        self.store = Signal(bool(0))
        self.outp = Signal(bool(0))
        self.inp = Signal(bool(0))
        self.br_op = Signal(bool(0))
        self.jal = Signal(bool(0))
        self.loadh = Signal(bool(0))
        self.indls = Signal(bool(0))
        self.signals = [self.al_ena, self.ah_ena, self.log_add, self.add_sub, self.shr, self.sel_imm, \
                        self.store, self.outp, self.inp, self.br_op, self.jal, self.loadh, self.indls]



dec_op_type = enum('al_ena', 'ah_ena', 'log_add', 'add_sub',
                    'shr', 'sel_imm', 'store', 'outp', 'inp', 'br_op', 'jal',
                    'loadh', 'indls')

alu_op_type = enum('NOP', 'LD', 'AND', 'OR', 'XOR')

IM_BITS = 9
DM_BITS = 8 