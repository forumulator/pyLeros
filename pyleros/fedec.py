import myhdl
from myhdl import instances, block, Signal, enum

from pyleros.codes import alu_op_type, t_decSignal, IM_BITS, DM_BITS
from pyleros.codes import dlist

from pyleros import decoder, rom


@block
def pyleros_fedec(clk, reset, acc, dm_data,
				pipe_dec, pipe_instr, pipe_rd_addr, pipe_pc):
	"""The fedec module for pyleros, that is, the fetch
	and decode pipeline stage. The modules is purely 
	combinatorial, except for the updating the pipeline 
	register. The IM is instantied and only accessed
	in this stage. The main functions done here are decoding
	of instruction, setting up branch control signals, selection
	of other control signals(including the ALU ones), selection 
	of DM address. an ALU operation on two local variables takes
	two cycles to execute and another cycle if the result needs 
	to written back	to a local variable

	Arguments (ports):
        clk: IN Clock signal
        reset: IN Async reset signal
        acc: IN Acc value accessed here, not written. This is
        	needed for setting the branch control signals and
        	for memory addredd of JAL
        dm_data: IN The data read from the DM, which is needed for
        	an direct add or and indirect load/ store(which follows)
        pipe_dec: OUT List of the decode signals, pass on to the execute stage
        pipe_instr: OUT Instruction, pass on to execute stage
        pipe_rd_addr: OUT DM read addr, pipeline register
        pipe_pc: OUT the value of PC, pipeline register

    Parameters:
	    None

	"""

	im_addr = Signal[intbv(0)[IM_BITS:]]

	instr = Signal[intbv(0)[16:]]
	instr_hi = Signal[intbv(0)[8:]]

	branch_en, acc_z = False, True

	pc, pc_next = Signal[intbv(0)[IM_BITS:]] * 2
	pc_op, pc_next = intbv(0)[IM_BITS:]

	decode = [Signal(Bool(0)) for i in dlist]
	decode[int(t_decSignal.op)] = Signal(alu_op_type.LD)

	# Instantiate the instruction memory
	im_inst = rom.pyleros_im(clk, reset, im_addr, instr)

	# Instantiate the decoder
	dec_inst = decoder.pyleros_decoder()

	@always_comb
	def sync_sig():

		instr_hi.next = instr[16:8]
		im_addr.next = pc_next
		pipe_pc.next = pc_add

	@always_comb
	def dm_addr_sel():

		offset_addr = intbv(dm_data + instr[8:0])[16:]
		
		# Indirect Addressing(with offset) 
		# for indirect load/store
		if decode[t_decSignal.indls] == True:
			pipe_rd_addr.next = offset_addr[DM_BITS:] 

		# Direct Addressing
		else:
			pipe_rd_addr.next = instr[DM_BITS:]

	



	return instances()


	# Sign extend an intbv or Signal to specified number of bits
	def sign_extend(num, bits = 0):

		if (type(num) is intbv) or (type(num) is myhdl._Signal._Signal):
			len_n = len(num) - 1 
			num = (int(num[len_n]) << (len_n) ) * -1 + int(num[len_n:])
			if bits != 0:
				if -2**(bits-1) < num < (2**(bits-1) - 1) :
					num = num & ((1 << bits) - 1)
				else:
					raise ValueError("Value " + str(num) + " too large to sign extend")
			return num

		else:
			raise TypeError("Input needs to be " + str(type(Signal())) + ' or ' + str(type(intbv(0))))
