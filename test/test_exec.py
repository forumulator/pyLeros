from pyleros import decoder, execute
from pyleros.codes import dlist
from pyleros.types import alu_op_type, t_decSignal, IM_BITS, DM_BITS

import pytest

from myhdl import *

import random
from random import randrange
from datetime import datetime

random.seed(int(datetime.now().time().second))

@block
def main(args=None):
	"""Test the execute module in pyleros

	"""
	clock = Signal(bool(0))
	reset = ResetSignal(0, active=1, async=True)

	# DECODER SIGNALS
	instr_hi = Signal(intbv(0)[8:])

	d, e = {}, {}
	for i in dlist:
		d[str(i)] = Signal(bool(0))
	
	d['op'] = Signal(alu_op_type.LD)

	out_list = [d[str(sig)] for sig in dlist]

	decode_inst = decoder.pyleros_decoder(instr_hi, out_list)

	# Input Signals to Execute
	in_imm = Signal(intbv(0)[16:])
	in_dm_addr = Signal(intbv(0)[DM_BITS:])
	in_pc = Signal(intbv(0)[IM_BITS:])

	out_acc = Signal(intbv(0)[16:])
	out_dm_data = Signal(intbv(0)[16:])

	exec_inst = execute.pyleros_exec(clock, reset, out_list, in_imm, in_dm_addr, in_pc, \
										out_acc, out_dm_data)

	@always(delay(10))
	def tbclk():
		clock.next = not clock

	@instance
	def tbstim():
		
		yield delay(10)
		assert True

		raise StopSimulation

	return instances()


def test_exec():

	inst_ex = main()
	inst_ex.run_sim()


if __name__ == "__main__":

	test_exec()
	

