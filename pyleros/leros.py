from myhdl import instances, block, Signal, intbv, \
                    always_comb

from pyleros.types import alu_op_type, IM_BITS, DM_BITS
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
    back_acc = Signal(intbv(0)[16:])
    fwd_accu = Signal(intbv(0)[16:])


    # read data from DM, IN to fedec, OUT from exec
    back_dm_data = Signal(intbv(0)[16:])

    # Decoder control signals list
    d = {}
    for i in dlist:
        d[str(i)] = Signal(bool(0))

    pipe_dec = [d[str(sig)] for sig in dlist]

    # imm value encoded in instruction, 
    # OUT from fedec, IN to decode
    pipe_imm_val = Signal(intbv(0)[16:])
    pipe_alu_op = Signal(alu_op_type.NOP)
    # DM read/write addr, OUT from fedec,
    # IN to exec
    pipe_dm_addr = Signal(intbv(0)[DM_BITS:])

    # Value of PC OUT from fedec, in to execute
    pipe_pc = Signal(intbv(0)[IM_BITS:]) 
    

    inst_fedec = fedec.pyleros_fedec(clk, reset, back_acc, back_dm_data, fwd_accu, pipe_alu_op,
                                        pipe_dec, pipe_imm_val, pipe_dm_addr, pipe_pc, filename=filename)

    inst_exec = execute.pyleros_exec(clk, reset, pipe_alu_op, pipe_dec, pipe_imm_val, pipe_dm_addr, pipe_pc, back_acc, back_dm_data, fwd_accu)


    return instances()