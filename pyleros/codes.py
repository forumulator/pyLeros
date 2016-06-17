from myhdl import enum
from pyleros.types import t_decSignal, alu_op_type

# dictionary of all the codes
codes = {}
codes['NOP'] = [0x00, [], False]
codes['ADD'] = [0x08, [t_decSignal.al_ena, t_decSignal.ah_ena, t_decSignal.log_add], True]
codes['SUB'] = [0x0c, [t_decSignal.al_ena, t_decSignal.ah_ena, t_decSignal.log_add, t_decSignal.add_sub], True]
codes['SHR'] = [0x10, [t_decSignal.al_ena, t_decSignal.ah_ena, t_decSignal.shr], False]

# ALU operations
codes['LOAD'] = [0x20, [t_decSignal.al_ena, t_decSignal.ah_ena, t_decSignal.op], True, alu_op_type.LD]
codes['AND'] = [0x22, [t_decSignal.al_ena, t_decSignal.ah_ena, t_decSignal.op], True, alu_op_type.AND]
codes['OR'] = [0x24, [t_decSignal.al_ena, t_decSignal.ah_ena, t_decSignal.op], True, alu_op_type.OR]
codes['XOR'] = [0x26, [t_decSignal.al_ena, t_decSignal.ah_ena, t_decSignal.op], True, alu_op_type.XOR]

# Load high
codes['LOADH'] = [0x28, [t_decSignal.loadh, t_decSignal.ah_ena, t_decSignal.op], False, alu_op_type.LD]
codes['STORE'] = [0x30, [t_decSignal.store], False]

# I/O
# codes['IN'] = [0x3c, [t_decSignal.al_ena, t_decSignal.ah_ena, t_decSignal.inp], False]
# codes['OUT'] = [0x3, [t_decSignal.al_ena, t_decSignal.ah_ena, t_decSignal.inp], False]

# LOADADDR

# LOAD INDIRECT

dlist = [t_decSignal.op, t_decSignal.al_ena, t_decSignal.ah_ena, t_decSignal.log_add, \
		t_decSignal.add_sub, t_decSignal.shr, t_decSignal.sel_imm, t_decSignal.store, \
		 t_decSignal.outp, t_decSignal.inp, t_decSignal.br_op, t_decSignal.jal, \
					t_decSignal.loadh, t_decSignal.indls]





