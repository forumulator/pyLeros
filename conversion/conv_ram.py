from myhdl import Signal, ResetSignal
from pyleros.ram import *
from pyleros.types import DM_BITS
from conversion_info import CONVERSION_PATH as PATH

def conv_ram():
	# Siggals
	clk = Signal(bool(0)) 
	reset = ResetSignal(0, active = 1, async = True)
	rd_addr = Signal(intbv(0)[DM_BITS:])
	wr_addr = Signal(intbv(0)[DM_BITS:])
	wr_data = Signal(intbv(0)[16:])
	wr_en = Signal(bool(0))
	rd_data = Signal(intbv(0)[16:])


	inst_ram = pyleros_dm(clk, reset, rd_addr, wr_addr, wr_data, wr_en, rd_data)
	inst_ram.convert(hdl = 'VHDL', path = PATH)



if __name__ == "__main__":

	conv_ram()