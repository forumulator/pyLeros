from myhdl import instances, block, Signal, enum
from pyleros.codes import alu_op_type


@block
def pyleros_decoder(clk, reset, acc, dm_data,
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
	
	@block
	def decoder():
		# Set the defaults of all signals
		

	return instances()


