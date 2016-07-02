import myhdl
from myhdl import instances, block, Signal, intbv, \
                    always_comb, always_seq

from pyleros.types import alu_op_type, t_decSignal, IM_BITS, DM_BITS
from pyleros.codes import dlist

from pyleros import decoder, rom


@block
def pyleros_fedec(clk, reset, acc, dm_data,
                pipe_dec, pipe_imme, pipe_dm_addr, pipe_pc, filename=None):
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
        acc: IN Acc value accessed here, not written. This is
            needed for setting the branch control signals and
            for memory addredd of JAL
        dm_data: IN The data read from the DM, which is needed for
            an direct add or and indirect load/ store(which follows)
        pipe_dec: OUT List of the decode signals, pass on to the execute stage
        pipe_imme: OUT Immediate value, as taken from the lower bits 
                of the instruction, pass on to execute stage
        pipe_dm_addr: OUT DM read addr, pipeline register
        pipe_pc: OUT the value of PC, pipeline register

    Parameters:

        filename: Name of the file or a list containing the instructions

    """

    im_addr = Signal(intbv(0)[IM_BITS:])

    instr = Signal(intbv(0)[16:])
    instr_hi = Signal(intbv(0)[8:])

    branch_en, acc_z = False, True

    pc = Signal(intbv(0)[IM_BITS:]) 
    pc_next = Signal(intbv(0)[IM_BITS:])
    pc_add = intbv(0)[IM_BITS:]

    decode = [Signal(bool(0)) for i in dlist]
    decode[int(t_decSignal.op)] = Signal(alu_op_type.LD)

    # Instantiate the instruction memory
    im_inst = rom.pyleros_im(clk, reset, im_addr, instr, filename=filename)

    # Instantiate the decoder
    dec_inst = decoder.pyleros_decoder(instr_hi, decode, True)

    @always_comb
    def sync_sig():

        # if not reset == reset.active:
        print("hi_bits:",instr[16:8])
        instr_hi.next = instr[16:8]
        im_addr.next = pc_next
        pipe_pc.next = pc_add  


    @always_comb
    def dm_addr_sel():

        # if not reset == reset.active:
        # Note ind ls adds the 8 bit immediate offset
        # to the previous value of the dm_
        # offset_addr = intbv(dm_data + instr[8:0])[16:]
        
        # Indirect Addressing(with offset) 
        # for indirect load/store
        # if decode[int(t_decSignal.indls)]:
        #     pipe_dm_addr.next = offset_addr[DM_BITS:] 

        # Direct Addressing
        # else:
        pipe_dm_addr.next = instr[DM_BITS:]

    @always_comb
    def branch_sel():

        # if not reset == reset.active:
        if acc == 0:
            acc_z = True

        else:
            acc_z = False

        branch_en = 0

        if decode[int(t_decSignal.br_op)]:
            br_type = instr[11:8]

            if br_type == 0b000:
                # BRANCH
                branch_en == 1

            elif br_type == 0b001:
                # BRZ
                branch_en = True if acc_z else False

            elif br_type == 0b010:
                # BRNZ
                branch_en = True if not acc_z else False

            elif br_type == 0b011:
                # BRP
                branch_en = True if not acc[15] else False

            elif br_type == 0b100:
                # BRN
                branch_en = True if acc[15] else False

    # For selection of next PC address
    @always_comb
    def pc_mux():

        pc_add_tmp = intbv(0)[IM_BITS:]
        pc_op = intbv(0)[IM_BITS:]
        # if not reset == reset.active:
        print("start", pc, pc_op, instr, acc, pc_add_tmp, instr)

        if branch_en:
            # Sign extend the low 8 bits
            # of instruction
            temp = instr
            pc_op[:] = sign_extend(temp, IM_BITS)

        else:
            pc_op[:] = 1
        print(pc, pc_op)

        pc_add_tmp[:] = (pc + pc_op)

        # Add 1 or branch offset OR set the add
        # to the jump addr
        if decode[int(t_decSignal.jal)]: 
            pc_next.next = acc[IM_BITS:]

        else:
            pc_next.next = pc_add_tmp
            pc_add = pc_add_tmp
        print("end", pc, pc_op, instr, acc, pc_add_tmp, instr)
    
    # Set the values on positive clock edge,
    # the only seq. part of the module
    @always_comb
    def intr_pipe():

        # if decode[int(t_decSignal.add_sub)] == True:
        # Set the immediate value
        # if decode[int(t_decSignal.loadh)]:
        #     pipe_imme.next = instr[8:] << 8

        # else:
        pipe_imme.next = instr[8:]

        # else:
        #   immr(7 downto 0) <= imout.data(7 downto 0);
        #   immr(15 downto 0) <= (others => '0');       
        # Set the control signals for the
        # pipeline register
        for sig in dlist:
            pipe_dec[int(sig)].next = decode[int(sig)]

    @always_seq(clk.posedge, reset=reset)
    def other_pipe():

        pc.next = pc_next

        


    return instances()



# Sign extend an intbv or Signal to specified number of bits
def sign_extend(num, bits = 0):

    if (type(num) is intbv) or (type(num) is myhdl._Signal._Signal):
        len_n = len(num)
        sign_bit = int(num[len_n - 1])
        num = ((sign_bit << len_n) * -1) + int(num[len_n:])
        if bits != 0:
            if -2**(bits-1) <= num <= (2**(bits-1) - 1) :
                num = num & ((1 << bits) - 1)
            else:
                raise ValueError("Value " + str(num) + " too larg e to sign extend")
        return num

    else:
        raise TypeError("Input needs to be " + str(type(Signal())) + ' or ' + str(type(intbv(0))))
