from pyleros import rom as rom

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
	clock = Clock(0, frequency=50e6)
	reset = Reset(0, active=0, async=True)

	rd_addr, rd_data = [Signal(intbv(0)[16:])] * 2

	IM_SIZE = 1024
	instr_array = [0 for _ in range(IM_SIZE)]

	def _bench_dec():

		# instantiate the rom
		for i in range(IM_SIZE):
			instr_array[i] = randrange(2**15) - 2**14

		im_inst = rom.pyleros_im(clock, reset, rd_addr, rd_data, filename = instr_array)

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

		return tbstim, im_inst

	for jj in range(10):
		run_testbench(_bench_dec)



if __name__ == "__main__":

	test_rom()


