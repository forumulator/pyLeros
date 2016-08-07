from pyleros import rom as rom
from pyleros.types import IM_BITS

from myhdl import *

import random
from random import randrange
from datetime import datetime

random.seed(int(datetime.now().time().second))


@block
def top_block(args=None):
	"""Test the rom module in pyleros

	"""
	clock = Signal(bool(0))
	reset = ResetSignal(0, active=1, async=True)

	rd_addr = Signal(intbv(0)[IM_BITS:])
	rd_data = Signal(intbv(0)[16:]) 

	IM_SIZE = 2**IM_BITS
	instr_array = [0 for _ in range(IM_SIZE)]


	@always(delay(10))
	def tbclk():
		clock.next = not clock

	
	# instantiate the rom
	for i in range(IM_SIZE):
		instr_array[i] = (randrange(2**15) - 2**14) & 0xffff
		# if i < 10:
		# 	print(instr_array[i])
	
	im_inst = rom.pyleros_im(rd_addr, rd_data, IM_array = instr_array)
	

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

	return instances()


def test_rom():

	for ii in range(10):
		inst_block = top_block()
		inst_block.run_sim()

if __name__ == "__main__":

	test_rom()


