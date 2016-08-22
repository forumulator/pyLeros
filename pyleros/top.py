from myhdl import instances, block, Signal, intbv, \
                    always_comb

from pyleros.types import alu_op_type, IM_BITS, DM_BITS, decSignal, inpSignal, outpSignal
from pyleros.codes import dlist

from pyleros import fedec, execute


@block
def pyleros(clk, reset, ioin, ioout, filename=None):
    """The main pyleros module. Instantiates both the fedec 
    and execute modules corresponding to the two pipeline stages, 
    and connects them with signals

    Arguments (ports):
        clk: IN Clock signal
        reset: IN Async reset signal
        ioin: The input signal, contains a rd_data of 16 bits.
        ioout: Output signal, contains output of 16 bits, i/o addr,
            and read/write strobes. The output is given in the same cycle
            as the ioout.out_strobe, and is guaranteed to be valid for 1 cycle.
            The input strobe is given, and the input is read in the same cycle.
        
    Parameters:
        filename: The file/ list containing instructions
            to load into instruction memory.

    """

    # Data forward from exec to fedec
    back_acc = Signal(intbv(0)[16:])
    fwd_accu = Signal(intbv(0)[16:])
    back_dm_data = Signal(intbv(0)[16:])

    # Decoder Signals
    pipe_dec = decSignal()

    # Other pipeline registers/signals
    pipe_imm_val = Signal(intbv(0)[16:])
    pipe_alu_op = Signal(alu_op_type.NOP)
    pipe_dm_addr = Signal(intbv(0)[DM_BITS:])
    pipe_pc = Signal(intbv(0)[IM_BITS:])    

    inst_fedec = fedec.pyleros_fedec(clk, reset, back_acc, back_dm_data, fwd_accu, pipe_alu_op,
                                        pipe_dec, pipe_imm_val, pipe_dm_addr, pipe_pc, filename=filename)

    inst_exec = execute.pyleros_exec(clk, reset, pipe_alu_op, pipe_dec, pipe_imm_val, 
                                        pipe_dm_addr, pipe_pc, back_acc, back_dm_data, fwd_accu, ioin)

    @always_comb
    def io_write():
        ioout.rd_strobe.next = pipe_dec.inp
        ioout.wr_strobe.next = pipe_dec.outp
        ioout.wr_data.next = back_acc
        ioout.io_addr.next = pipe_imm_val


    return instances()