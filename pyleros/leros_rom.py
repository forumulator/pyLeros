from myhdl import block, Signal, intbv, instances, always_seq
import sys


@block
def pyleros_im(clk, reset, rd_addr, rd_data, filename = None):
	"""Definition of the instruction memory, or the ROM for
	pyleros. Reading is synchronous with the rising edge of the
	clock. Writing is not enabled.

	Arguments (ports):
        clk: The clock signal
        reset: The reset signal #Async?
        rd_addr: IN Read address
        rd_data: OUT The data at IM address

    Parameters:
	    None 

	"""
	IM_SIZE = 1024
	IM = [(intbv(0)[16:]) for _ in range(IM_SIZE)]

	# Fill up the memory registers
	define_rom(IM, IM_SIZE, filename)

	# convert list into tupple for automatic conversion
	IM_array = tuple(IM)

	@always_seq(clk.posedge, reset=reset)
	def IM_read():

			rd_data.next = IM[int(rd_addr)]

	return instances()




