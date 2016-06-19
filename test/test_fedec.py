from pyleros.fedec import sign_extend, pyleros_fedec
from pyleros.codes import dlist
from pyleros.types import alu_op_type, t_decSignal, IM_BITS, DM_BITS

import pytest

from myhdl import *

from rhea.system import Clock, Reset

from rhea.utils.test import run_testbench

import random
from random import randrange
from datetime import datetime

random.seed(int(datetime.now().time().second))

@pytest.mark.xfail
def test_fedec(args=None):
	"""Test the fetch/decode module in pyleros

	"""
	clock = Signal(bool(0))
	reset = ResetSignal(1, active=1, async=True)

	acc, dm_data = [Signal(intbv(0)[16:])] * 2

	pipe_dec = [False for sig in dlist]
	pipe_dec[int(t_decSignal.op)] = alu_op_type.LD

	pipe_imme = Signal(intbv(0)[16:])
	pipe_rd_addr = Signal(intbv(0)[DM_BITS:])

	pipe_pc = Signal(intbv(0)[IM_BITS:])

	instr_array = [0 for _ in range(IM_SIZE)]

	@always(delay(10))
    def tbclk():
        clock.next = not clock


	def _bench_load():

		# instantiate the rom
		for i in range(IM_SIZE):
			# LOADI for the second half of the memory
			if i > int(IM_SIZE /2):
				imm = randrange(2**8)
				# LOADI in the first 8 bits and a random
				# imm value in the lower bits
				instr_array = [(0x2100) | (im & 0xff)]

		inst_fedec = pyleros_fedec(clock, reset, acc, dm_data,
								pipe_dec, pipe_imme, pipe_rd_addr,
								pipe_pc, filename=instr_array)

		@instance
		def tbstim():

			for i in range(5):
				yield clock.posedge

			for tryn in range(IM_SIZE):

				addr = randrange(IM_SIZE)

				rd_addr.next = addr

				for i in range(2):
					yield clock.posedge

				assert rd_data == instr_array[addr]			

				for i in range(2):
					yield clock.posedge	

			for ii in range(5):
				yield clock.posedge


			raise StopSimulation

		return tbstim, im_inst, tbclk

	for jj in range(10):
		run_testbench(_bench_dec)



def test_sign_extend(args=None):

	nbits = 0
	exbits = 0

	for ii in range(1000):
		nbits = randrange(32) + 1
		num = intbv(randrange(1 << nbits))[nbits:]

		# try for an arb. number of bits
		exbits = randrange(1, 2 * nbits)

		try:
			exnum = sign_extend(num, exbits)
			if num[nbits - 1] == True:
				# negative in 2's complement
				assert (num - 2**nbits) == (exnum - 2**exbits)
				assert sign_extend(num) == (num - 2**nbits)

			else:
				assert num == exnum
				assert sign_extend(num) == num

		except ValueError:
			assert exbits < nbits


if __name__ == "__main__":

	test_fedec()
	test_sign_extend()


