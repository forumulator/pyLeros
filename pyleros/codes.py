from pyleros.types import t_decSignal, alu_op_type

# dictionary of all the codes
# codes['X'][0] is the opcode, codes['X'][1] is the list of signals
# which is set to active by twhen 'X' is decoded.
# codes['X'][2] is weather the instruction also has an immediate
# corres. instruction. codes['X'][3], if it exists, is the 
# value of alu_op_type, when 'X' is decoded.
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

# Branch
codes['BRANCH'] = [0x48, [t_decSignal.br_op], False]
codes['BRZ'] = [0x49, [t_decSignal.br_op], False]
codes['BRNZ'] = [0x4a, [t_decSignal.br_op], False]
codes['BRP'] = [0x4b, [t_decSignal.br_op], False]
codes['BRN'] = [0x4c, [t_decSignal.br_op], False]

# I/O
# codes['IN'] = [0x3c, [t_decSignal.al_ena, t_decSignal.ah_ena, t_decSignal.inp], False]
# codes['OUT'] = [0x3, [t_decSignal.al_ena, t_decSignal.ah_ena, t_decSignal.inp], False]

# LOADADDR

# LOAD/STORE INDIRECT
codes['LOADX'] = [0x60, [t_decSignal.indls, t_decSignal.ah_ena, t_decSignal.al_ena], False]
codes['STOREX'] = [0x70, [t_decSignal.indls, t_decSignal.store], False]

# Jump and link
codes['JAL'] = [0x40, [t_decSignal.jal, t_decSignal.store], False]

dlist = [t_decSignal.op, t_decSignal.al_ena, t_decSignal.ah_ena, t_decSignal.log_add, \
        t_decSignal.add_sub, t_decSignal.shr, t_decSignal.sel_imm, t_decSignal.store, \
         t_decSignal.outp, t_decSignal.inp, t_decSignal.br_op, t_decSignal.jal, \
                    t_decSignal.loadh, t_decSignal.indls]




def conv_bin(instr=None):
    if not instr:
        return

    bin_code = 0x00
    if instr == 'NOP':
        bin_code = 0x00

    elif instr == 'ADD':
        bin_code = 0x08

    elif instr == 'SUB':
        bin_code = 0x0c

    elif instr == 'SHR':
        bin_code = 0x10

    elif instr == 'AND':
        bin_code = 0x22

    elif instr == 'OR':
        bin_code = 0x24

    elif instr == 'XOR':
        bin_code = 0x26

    elif instr == 'LOAD':
        bin_code == 0x20

    elif instr == 'LOADH':
        bin_code == 0x28

    elif instr == 'STORE':
        bin_code == 0x30

    return bin_code
