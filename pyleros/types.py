from myhdl import enum

t_decSignal = enum('op', 'al_ena', 'ah_ena', 'log_add', 'add_sub', \
					'shr', 'sel_imm', 'store', 'outp', 'inp', 'br_op', 'jal', \
					'loadh', 'indls')

alu_op_type = enum('NOP', 'LD', 'AND', 'OR', 'XOR')

IM_BITS = 9
DM_BITS = 8 