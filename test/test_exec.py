from pyleros import decoder, execute
from pyleros.codes import dlist, codes
from pyleros.types import alu_op_type, t_decSignal, IM_BITS, DM_BITS

import pytest

from myhdl import *

import random
from random import randrange
from datetime import datetime

random.seed(int(datetime.now().time().second))


def test_add():

	@block
	def tb_exec_add(args=None):
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

		op = 0
		instr_list = []
		for i in range(30):
			op = randrange(2**8)
			# Add Immediate
			instr_bin = codes['ADD'][0] | 0x01
			instr_bin = (instr_bin << 8) | intbv(op)[8:]
			instr_list.append(('ADD', op, instr_bin))


		@always(delay(10))
		def tbclk():
			clock.next = not clock

		@instance
		def tbstim():
			# local accumulator var
			acc = 0
			for i in range(10):
				print(instr_list[i])
			
			yield delay(5)

			for addr in range(len(instr_list)):

				op = instr_list[addr][1]
				instr_bin = instr_list[addr][2]
				instr_hi.next = instr_bin[16:8]


				in_imm.next = instr_bin & 0xff
				# yield delay(2)
				# print("Imm val",in_imm)

				yield clock.posedge
				yield delay(10)

				assert ((acc + op) & 0xffff) == out_acc
				acc += op

				# if (addr == 9):
				# 	assert False
			raise StopSimulation

		return instances()


	# Run sim to test
	inst_ex = tb_exec_add()
	inst_ex.run_sim()


if __name__ == "__main__":

	test_add()
	

