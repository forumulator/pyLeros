import myhdl
from myhdl import instances, block, Signal, intbv, \
                    always_comb, always_seq, ConcatSignal

from pyleros.types import alu_op_type, dec_op_type, IM_BITS, DM_BITS, decSignal
from pyleros.codes import dlist

from pyleros import decoder, rom


@block
def pyleros_fedec(clk, reset, back_acc, back_dm_data, fwd_accu, pipe_alu_op,
                 pipe_dec, pipe_imme, pipe_dm_addr, pipe_pc, filename=None, debug=False):
    """The fedec module for pyleros, that is, the fetch
    and decode pipeline stage. The modules is purely 
    combinatorial, except for the updating the pipeline 
    register. The IM is instantied and only accessed
    in this stage. The main functions done here are decoding
    of instruction, setting up branch control signals, selection
    of other control signals(including the ALU ones), selection 
    of DM address. an ALU operation on two local variables takes
    two cycles to execute and another cycle if the result needs 
    to written back to a local variable
    
    Arguments (ports):
        clk: IN Clock signal
        reset: IN Async reset signal
        back_acc: IN Acc value accessed here, not written. This is
            needed for setting the branch control signals and
            for memory addredd of JAL
        back_dm_data: IN The data read from the DM, which is needed for
            an direct add or and indirect load/ store(which follows)
        fwd_accu: IN The value of the accumulator, forwarded from the 
                execute stage to provide proper branching. Currently unused. 
        pipe_dec: OUT List of the decode signals, pass on to the execute stage
        pipe_imme: OUT Immediate value, as taken from the lower bits 
                of the instruction, pass on to execute stage
        pipe_dm_addr: OUT DM read addr, pipeline register
        pipe_pc: OUT the value of PC, pipeline register

    Parameters:

        filename: Name of the file or a list containing the instructions
        debug: Debugging mode, the processor prints various error messages

    """

    im_addr = Signal(intbv(0)[IM_BITS:])

    instr = Signal(intbv(0)[16:])
    instr_hi = Signal(intbv(0)[8:])

    branch_en = Signal(bool(0))


    # PC start from 0x00 in this design, and each instruction is executed exactly once. 
    # In the original design, PC started from 1. However, 0x00 is typically NOP
    pc = Signal(intbv(0)[IM_BITS:]) 
    pc_next = Signal(intbv(0)[IM_BITS:])
    pc_add = Signal(intbv(0)[IM_BITS:])
    pc_op = Signal(intbv(0, min = -2**(IM_BITS - 1), max = 2**(IM_BITS - 1) - 1))
    decode = decSignal()
    alu_op = Signal(alu_op_type.NOP)

    # Instantiate the instruction memory
    im_inst = rom.pyleros_im(im_addr, instr, filename, debug)

    # Instantiate the decoder
    dec_inst = decoder.pyleros_decoder(instr_hi, alu_op, decode, debug)

    @always_comb
    def sync_sig():

        # if __debug__:
        #     if debug:
        #         print("hi_bits:",instr[16:8])

        instr_hi.next = instr[16:8]
        im_addr.next = pc


    @always_comb
    def mux_dm_addr():

        offset_addr = intbv(back_dm_data + instr[8:0])[DM_BITS:]        
        
        if decode.indls:
            # Indirect Addressing(with offset) 
            # for indirect load/store
            # if __debug__:
            #     if debug:
            #         print("offset address: " + str(int(offset_addr)))

            pipe_dm_addr.next = offset_addr[DM_BITS:] 

        else:
            # Direct Addressing
            # if __debug__:
            #     if debug:
            #         print("direct address: " + str(int(instr[DM_BITS:])))
            pipe_dm_addr.next = instr[DM_BITS:]

    @always_comb
    def branch_sel():

        acc_z = True
        
        # if not reset == reset.active:
        if back_acc == 0:
            acc_z = True

        else:
            acc_z = False

        branch_en.next = 0

        if decode.br_op:
            br_type = instr[11:8]

            if br_type == 0b000:
                # BRANCH
                branch_en.next = True

            elif br_type == 0b001:
                # BRZ
                if acc_z:
                    branch_en.next = True
                else:
                    branch_en.next = False

            elif br_type == 0b010:
                # BRNZ
                if not acc_z:
                    branch_en.next = True
                else:
                    branch_en.next = False

            elif br_type == 0b011:
                # BRP
                if not back_acc[15]:
                    branch_en.next = True
                else:
                    branch_en.next = False

            elif br_type == 0b100:
                # BRN
                if back_acc[15]:
                    branch_en.next = True
                else:
                    branch_en.next = False

    # For selection of next PC address
    @always_comb
    def pc_addr():

        # if __debug__:
        #     if debug:
        #         print('start', pc, pc_op, instr, back_acc, pc_add, instr)

        if branch_en == 1:
            # Sign extend the low 8 bits
            # of instruction
            pc_op.next = instr[8:].signed()

        else:
            pc_op.next = 1

        # if __debug__:
        #     if debug:
        #         print(pc, pc_op)
        
    @always_comb
    def pc_next_set():
        pc_add.next = intbv(pc + pc_op)[IM_BITS:]


    @always_comb
    def pc_mux():
        # Add 1 or branch offset OR set the add
        # to the jump addr
        if decode.jal: 
            pc_next.next = back_acc[IM_BITS:]

        else:
            pc_next.next = pc_add

        # if __debug__:
        #     if debug:
        #         print('end', pc, pc_op, instr, back_acc, pc_add, instr)
    
    @always_seq(clk.posedge, reset)
    def intr_pipe():

        # if decode.add_sub == True:
        # Set the immediate value

        if decode.loadh:
            if __debug__:
                pipe_imme.next = intbv(0)[16:]
            pipe_imme.next[16:8] = instr[8:]
            pipe_imme.next[8:0] = intbv(0)[8:]
        else:

            pipe_imme.next = instr[8:]

        pipe_pc.next = pc_add 

        pipe_dec.al_ena.next = decode.al_ena
        pipe_dec.ah_ena.next = decode.ah_ena
        pipe_dec.log_add.next = decode.log_add
        pipe_dec.add_sub.next = decode.add_sub
        pipe_dec.shr.next = decode.shr
        pipe_dec.sel_imm.next = decode.sel_imm
        pipe_dec.store.next = decode.store
        pipe_dec.outp.next = decode.outp
        pipe_dec.inp.next = decode.inp
        pipe_dec.br_op.next = decode.br_op
        pipe_dec.jal.next = decode.jal
        pipe_dec.loadh.next = decode.loadh
        pipe_dec.indls.next = decode.indls

        pipe_alu_op.next = alu_op

        pc.next = pc_next        

    return instances()



# Sign extend an intbv or Signal to specified number of bits
def sign_extend(num, bits = 0):

    if (type(num) is intbv) or (type(num) is myhdl._Signal._Signal):
        len_n = len(num)
        sign_bit = int(num[len_n - 1])
        num = ((sign_bit << len_n) * -1) + int(num[len_n:])
        if bits != 0:
            if -2**(bits-1) <=  num <= (2**(bits-1) - 1) :
                num = num & ((1 << bits) - 1)
            else:
                raise ValueError("Value " + str(num) + " too larg e to sign extend")
        return num

    else:
        raise TypeError("Input needs to be " + str(type(Signal())) + ' or ' + str(type(intbv(0))))
