from pyleros.codes import codes, dlist

from pyleros import decoder
from myhdl import 

from rhea import Clock, Reset

from rhea.utils.test import run_testbench


def test_decode(args=None):
	"""Test the decoder module in pyleros

	"""
	clock = Clock(0, frequency=50e6)
    reset = Reset(0, active=0, async=True)

    # the high 8 bits of the instruction
    instr_hi = Signal(intbv(0)[8:])

    d = {}
    for i in dlist:
    	d[i] = Signal(bool(0))


	def _bench_dec():

		# instantiate the decoder
		decode_inst = pyleros_decoder(instr_hi, d['op'], d['al_ena'], d['ah_ena'], d['log_add'], d['add_sub'], 
					d['shr'], d['sel_imm'], d['store'], d['outp'], d['inp'], d['br_op'], d['jal'],
					d['loadh'], d['indls'])

		@instance
		def tbstim():

			for instr in codes:


