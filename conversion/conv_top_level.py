from myhdl import Signal, intbv, ResetSignal
from pyleros.top import pyleros

from pyleros.types import inpSignal, outpSignal
from conversion_info import CONVERSION_PATH, ROM_PATH

import sys



def conv_top_level(rom_file = 'sum_n.rom'):
	""" Conversion for the top level module pyleros.top 

	"""

	clock = Signal(bool(0))
	reset = ResetSignal(0, active =1 , async = True)
	ioin = inpSignal()
	ioout = outpSignal()

	inst_proc = pyleros(clock, reset, ioin, ioout, filename = ROM_PATH + rom_file)
	inst_proc.convert(hdl = 'VHDL', path = CONVERSION_PATH)



if __name__ == "__main__":
	if len(sys.argv) > 1:
		rom_file = sys.argv[1]
		conv_top_level(rom_file)