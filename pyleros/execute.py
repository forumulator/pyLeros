from myhdl import instances, block, Signal, intbv, \
                    always_comb, always_seq

from pyleros.types import t_decSignal, IM_BITS, DM_BITS

from pyleros import alu, ram


@block
def pyleros_exec(clk, reset, pipe_dec, pipe_imme, pipe_dm_addr, pipe_pc,
                 back_acc, back_dm_data):
    """The execute module for pyleros. The modules is purely 
    combinatorial, except for the updating the pipeline 
    register. The DM is instantied and only accessed
    in this stage. The main function is to execute the ALU
    operation, read the data memory, update the accumulator, 
    and feed back teh results to fedec

    Arguments (ports):
        clk: IN Clock signal
        reset: IN Async reset signal
        pipe_dec: IN List of the decode signals, from fedec
        pipe_imme: IN Immediate value, as taken from the lower bits 
                of the instruction, from fedec
        pipe_dm_addr: OUT DM read addr, pipeline registerm, from fedec
        pipe_pc: IN the value of PC, pipeline register, from fedec
        back_acc: OUT Value of the acc to send back to fedec.
        back_dm_data: OUT The data read from the DM, back to fedec for
            indls

    Parameters:
        None

    """

    # Define the Accumulator
    acc, opd, pre_accu = [Signal(intbv(0)[16:])] * 3

    # Signals to instantiate the DM
    dm_wr_addr = Signal(intbv(0)[DM_BITS:])
    dm_wr_data = Signal(intbv(0)[16:])
    dm_rd_addr = Signal(intbv(0)[DM_BITS:])
    dm_rd_data = Signal(intbv(0)[16:])
    dm_wr_en = Signal(bool(0))

    pc_dly = Signal(intbv(0)[IM_BITS:])

    dm_wr_addr_dly = Signal(intbv(0)[DM_BITS:])

    # Instantiate the ALU
    alu_inst = alu.pyleros_alu(pipe_dec, acc, opd, pre_accu)

    # Instantiate the DM
    dm_inst = ram.pyleros_dm(clk, reset, dm_rd_addr, dm_wr_addr, dm_wr_data, dm_wr_en, dm_rd_data)


    @always_comb
    def sync_sig():

        if not reset:
            back_acc.next = acc
            back_dm_data.next = dm_rd_data
            dm_rd_addr.next = pipe_dm_addr
            dm_wr_addr.next = dm_wr_addr_dly


    @always_comb
    def opd_mux():

        if not reset:
            # Mux for selecting the value of operand, that is,
            # Data Memory read/ Immediate value retrieve
            if pipe_dec[int(t_decSignal.sel_imm)]:
                # Immediate
                opd.next = pipe_imme

            else:
                opd.next = dm_rd_data


    @always_comb
    def mux_jal():

        if not reset:
            # MUX for selecting the data to be written
            # in case of jal
            if pipe_dec[int(t_decSignal.jal)]:
                temp = intbv(0)[16:]
                temp[IM_BITS:0] = pc_dly
                temp[16:IM_BITS] = 0

                dm_wr_data.next = temp

            else:
                dm_wr_data.next = acc


    
    # Set the values on positive clock edge,
    # the only seq. part of the module
    @always_seq(clk.posedge, reset=reset)
    def fedec_set():

        # Write the accumulator based on the 
        # high and low enable write control signals
        high, low = 0x00, 0x00
        if pipe_dec[int(t_decSignal.al_ena)]:
            low = 0xff
        if pipe_dec[int(t_decSignal.ah_ena)]:
            high = 0xff

        mask = (high << 8) | low

        acc.next = pre_accu | mask

        # Set the delay registers
        dm_wr_addr_dly.next = pipe_dm_addr
        pc_dly.next = pipe_pc




    return instances()