from myhdl import instances, block, Signal, intbv, \
                    always_comb, always_seq

from pyleros.types import alu_op_type, t_decSignal, IM_BITS, DM_BITS
from pyleros.codes import dlist

from pyleros import fedec, execute


@block
def pyleros(clk, reset, filename=None):
    """The main pyleros module. Instantiates both the fedec 
    and execute modules corresponding to the two pipeline stages, 
    and connects them with signals

    Arguments (ports):
        clk: IN Clock signal
        reset: IN Async reset signal
        
    Parameters:
        filename: The file/ list containing instructions
            to load into instruction memory.

    """

    # Accumulator, OUT from exec, IN to fedec
    acc = Signal(intbv(0)[16:])

    # read data from DM, IN to fedec, OUT from exec
    dm_data = Signal(intbv(0)[16:])

    # Decoder control signals list
    d = {}
    for i in dlist:
        d[str(i)] = Signal(bool(0))

    d['op'] = Signal(alu_op_type.LD)
    dec = [d[str(sig)] for sig in dlist]

    # imm value encoded in instruction, 
    # OUT from fedec, IN to decode
    imm_val = Signal(intbv(0)[16:])

    # DM read/write addr, OUT from fedec,
    # IN to exec
    dm_addr = Signal(intbv(0)[DM_BITS:])

    # Value of PC OUT from fedec, in to execute
    pc = Signal(intbv(0)[IM_BITS:]) 

    

    inst_fedec = fedec.pyleros_fedec(clk, reset, acc, dm_data,
                                        dec, imm_val, dm_addr, pc, filename=filename)

    inst_exec = execute.pyleros_exec(clk, reset, dec, imm_val, dm_addr, pc, acc, dm_data)


    return instances()