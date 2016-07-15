from pyleros.types import dec_op_type, alu_op_type

# dictionary of all the codes
# codes['X'][0] is the opcode, codes['X'][1] is the list of signals
# which is set to active by twhen 'X' is decoded.
# codes['X'][2] is weather the instruction also has an immediate
# corres. instruction. codes['X'][3], if it exists, is the 
# value of alu_op_type, when 'X' is decoded.
codes = {}
codes['NOP'] = [0x00, [], False]
codes['ADD'] = [0x08, [dec_op_type.al_ena, dec_op_type.ah_ena, dec_op_type.log_add], True]
codes['SUB'] = [0x0c, [dec_op_type.al_ena, dec_op_type.ah_ena, dec_op_type.log_add, dec_op_type.add_sub], True]
codes['SHR'] = [0x10, [dec_op_type.al_ena, dec_op_type.ah_ena, dec_op_type.shr], False]

# ALU operations
codes['LOAD'] = [0x20, [dec_op_type.al_ena, dec_op_type.ah_ena, dec_op_type.op], True, alu_op_type.LD]
codes['AND'] = [0x22, [dec_op_type.al_ena, dec_op_type.ah_ena, dec_op_type.op], True, alu_op_type.AND]
codes['OR'] = [0x24, [dec_op_type.al_ena, dec_op_type.ah_ena, dec_op_type.op], True, alu_op_type.OR]
codes['XOR'] = [0x26, [dec_op_type.al_ena, dec_op_type.ah_ena, dec_op_type.op], True, alu_op_type.XOR]

# Load high
codes['LOADH'] = [0x28, [dec_op_type.loadh, dec_op_type.ah_ena, dec_op_type.op], False, alu_op_type.LD]
codes['STORE'] = [0x30, [dec_op_type.store], False]

# Branch
codes['BRANCH'] = [0x48, [dec_op_type.br_op], False]
codes['BRZ'] = [0x49, [dec_op_type.br_op], False]
codes['BRNZ'] = [0x4a, [dec_op_type.br_op], False]
codes['BRP'] = [0x4b, [dec_op_type.br_op], False]
codes['BRN'] = [0x4c, [dec_op_type.br_op], False]

# I/O
# codes['IN'] = [0x3c, [dec_op_type.al_ena, dec_op_type.ah_ena, dec_op_type.inp], False]
# codes['OUT'] = [0x3, [dec_op_type.al_ena, dec_op_type.ah_ena, dec_op_type.inp], False]

# LOADADDR

# LOAD/STORE INDIRECT
codes['LOADX'] = [0x60, [dec_op_type.indls, dec_op_type.ah_ena, dec_op_type.al_ena], False]
codes['STOREX'] = [0x70, [dec_op_type.indls, dec_op_type.store], False]

# Jump and link
codes['JAL'] = [0x40, [dec_op_type.jal, dec_op_type.store], False]

dlist = [dec_op_type.op, dec_op_type.al_ena, dec_op_type.ah_ena, dec_op_type.log_add, \
        dec_op_type.add_sub, dec_op_type.shr, dec_op_type.sel_imm, dec_op_type.store, \
         dec_op_type.outp, dec_op_type.inp, dec_op_type.br_op, dec_op_type.jal, \
                    dec_op_type.loadh, dec_op_type.indls]




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
