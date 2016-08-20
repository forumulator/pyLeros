from myhdl import instances, block, Signal, intbv, \
                    always_comb, always_seq

from pyleros.types import dec_op_type, IM_BITS, DM_BITS

from pyleros import alu, ram


@block
def pyleros_exec(clk, reset, pipe_alu_op, pipe_dec, pipe_imme, pipe_dm_addr, pipe_pc,
                 back_acc, back_dm_data, fwd_accu, ioin, debug=False):
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
        pipe_dm_addr: OUT DM read addr, pipeline register, from fedec
        pipe_pc: IN the value of PC, pipeline register, from fedec
        back_acc: OUT Value of the acc to send back to fedec.
        back_dm_data: OUT The data read from the DM, back to fedec for
            indls

    Parameters:
        debug: Debugging mode, the processor prints various error messages
        
    """

    # Define the Accumulator
    acc = Signal(intbv(0)[16:])
    opd = Signal(intbv(0)[16:])
    pre_accu = Signal(intbv(0)[16:])

    # Signals to instantiate the DM
    dm_wr_addr = Signal(intbv(0)[DM_BITS:])
    dm_wr_data = Signal(intbv(0)[16:])
    dm_rd_addr = Signal(intbv(0)[DM_BITS:])
    dm_rd_data = Signal(intbv(0)[16:])
    dm_wr_en = Signal(bool(0))

    pc_dly = Signal(intbv(0)[IM_BITS:])
  
    dm_wr_addr_dly = Signal(intbv(0)[DM_BITS:])

    # Instantiate the ALU
    alu_inst = alu.pyleros_alu(pipe_alu_op, pipe_dec, acc, opd, pre_accu, ioin, debug)

    # Instantiate the DM
    dm_inst = ram.pyleros_dm(clk, reset, dm_rd_addr, dm_wr_addr, dm_wr_data, dm_wr_en, dm_rd_data, debug)


    @always_comb
    def back_sig():

        # back_x Signals are used for data forwarding, thus
        # they aren't set on clock.posedge
        back_dm_data.next = dm_rd_data
        dm_rd_addr.next = pipe_dm_addr


    @always_comb
    def opd_mux():

        # if not reset:
        # Mux for Data Memory read/ Immediate value retrieve
        if pipe_dec.sel_imm == True:
            # Immediate
            opd.next = pipe_imme

        else:
            opd.next = dm_rd_data



    @always_comb
    def mux_write_dm():
  
        # print(acc)
        if pipe_dec.store == True:
            dm_wr_en.next = True
        else:
            dm_wr_en.next = False

        # Used to ensure that address for 
        # stores don't get affected by the next instruction fetch and
        # decode
        dm_wr_addr.next = dm_wr_addr_dly

        # MUX for selecting the data to be written
        # in case of jal
        if pipe_dec.jal == True:
            # dm_wr_data.next = intbv(0)[16:]
            dm_wr_data.next = pipe_pc

        else:
            dm_wr_data.next = acc
   

    @always_comb
    def comb_set_sig():

        # delay PC, needed to link in JAL
        pc_dly.next = pipe_pc


    @always_seq(clk.posedge, reset=reset)
    def seq_set_sig():

        # Write the accumulator based on the 
        # high and low enable write control signals
        if pipe_dec.ah_ena == True:
            acc.next[16:8] = pre_accu[16:8]
        if pipe_dec.al_ena == True:
            acc.next[8:0] = pre_accu[8:0]
            if __debug__:
                if debug:
                    print("Next value of the accumulator " + str(int(pre_accu)))
        dm_wr_addr_dly.next = pipe_dm_addr

    @always_comb
    def fwd_acc_set():

        if pipe_dec.ah_ena == True:
            back_acc.next[16:8] = pre_accu[16:8]
            fwd_accu.next[16:8] = pre_accu[16:8]
        if pipe_dec.al_ena == True:
            back_acc.next[8:0] = pre_accu[8:0]
            fwd_accu.next[8:0] = pre_accu[8:0]
       
    return instances()