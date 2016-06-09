from myhdl import enum

alu_op_type = enum('LD', 'AND', 'OR', 'XOR')

# dictionary of all the codes
codes = {}
codes['NOP'] = [0x00, [], False]
codes['ADD'] = [0x08, ['al_ena', 'ah_ena', 'log_add'], True]
codes['SUB'] = [0x0c, ['al_ena', 'ah_ena', 'log_add', 'add_sub'], True]
codes['SHR'] = [0x10, ['al_ena', 'ah_ena', 'shr'], False]

# ALU operations
codes['LOAD'] = [0x20, ['al_ena', 'ah_ena', 'op'], True, alu_op_type.LD]
codes['AND'] = [0x22, ['al_ena', 'ah_ena', 'op'], True, alu_op_type.AND]
codes['OR'] = [0x24, ['al_ena', 'ah_ena', 'op'], True, alu_op_type.OR]
codes['XOR'] = [0x26, ['al_ena', 'ah_ena', 'op'], True, alu_op_type.XOR]

# Load high
codes['LOADH'] = [0x28, ['al_ena', 'ah_ena', 'op'], False, alu_op_type.LD]
codes['STORE'] = [0x30, ['store'], False]

# I/O
# codes['IN'] = [0x3c, ['al_ena', 'ah_ena', 'inp'], False]
# codes['OUT'] = [0x3, ['al_ena', 'ah_ena', 'inp'], False]

# LOADADDR

# LOAD INDIRECT

dlist = ['op', 'al_ena', 'ah_ena', 'log_add', 'add_sub', \
					'shr', 'sel_imm', 'store', 'outp', 'inp', 'br_op', 'jal', \
					'loadh', 'indls']





