from pyleros import rom as rom
from pyleros.types import IM_BITS

from myhdl import *

from rhea.system import Clock, Reset

from rhea.utils.test import run_testbench

import random
from random import randrange
from datetime import datetime

random.seed(int(datetime.now().time().second))


def test_rom(args=None):
	"""Test the rom module in pyleros

	"""
	clock = Signal(bool(0))
	reset = Reset(0, active=1, async=True)

	rd_addr = Signal(intbv(0)[IM_BITS:])
	rd_data = Signal(intbv(0)[16:]) 

	IM_SIZE = 2**IM_BITS
	instr_array = [0 for _ in range(IM_SIZE)]


	@always(delay(10))
	def tbclk():
		clock.next = not clock

	

	def _bench_dec():

		# instantiate the rom
		for i in range(IM_SIZE):
			instr_array[i] = randrange(2**15) - 2**14
			# if i < 10:
			# 	print(instr_array[i])
		
		im_inst = rom.pyleros_im(clock, reset, rd_addr, rd_data, filename = instr_array)
		

		@instance
		def tbstim():

			for i in range(2):
				yield clock.posedge

			for tryn in range(IM_SIZE):
				
				addr = randrange(IM_SIZE)

				rd_addr.next = addr

				for i in range(1):
					yield clock.posedge

				# this delay is necessary because when on positive
				# edge, the rd_data.next attribute is changed ny the
				# IM, the actual rd_data changes in the next simulation step.
				yield delay(1)

				# for i in range(10):
				# 	print(instr_array[i])
				# print("\n")
				# print(addr)
				assert (rd_data.next & 0xffff) == (instr_array[addr] & 0xffff)



			for ii in range(5):
				yield clock.posedge


			raise StopSimulation

		return tbclk, tbstim, im_inst

	for jj in range(10):
		run_testbench(_bench_dec)



if __name__ == "__main__":

	test_rom()


