import myhdl
from myhdl import instances, block, Signal, intbv, enum, \
					always_comb, always_seq

from pyleros.types import alu_op_type, t_decSignal, IM_BITS, DM_BITS
from pyleros.codes import dlist

from pyleros import alu, ram


@block
def pyleros_exec(clk, reset, pipe_dec, pipe_imme, pipe_rd_addr, pipe_pc,
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
        pipe_rd_addr: OUT DM read addr, pipeline registerm, from fedec
        pipe_pc: IN the value of PC, pipeline register, from fedec
        back_acc: OUT Value of the acc to send back to fedec.
        back_dm_data: OUT The data read from the DM, back to fedec for
        	indls

    Parameters:
	    None

	"""




	return instances()