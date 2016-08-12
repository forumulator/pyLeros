from pyleros import fedec, alu
from pyleros.fedec import sign_extend
from pyleros.codes import dlist, codes, conv_bin
from pyleros.types import alu_op_type, t_decSignal, IM_BITS, DM_BITS

import pytest

from myhdl import *

import random
from random import randrange
from datetime import datetime

random.seed(int(datetime.now().time().second))

# Test with immediate instructions.
@pytest.mark.xfail
def test_fedec_imm():
	
	@block
	def tb_fedec_top():
		"""Test the alu module in pyleros

		"""

		clock = Signal(bool(0))
		reset = ResetSignal(0, active=1, async=True)

		# FEDEC SIGNALS
		in_acc, in_dm_data = [Signal(intbv(0)[16:])] * 2
		out_imme = Signal(intbv(0)[16:])
		out_dm_addr = Signal(intbv(0)[DM_BITS:])
		out_pc = Signal(intbv(0)[IM_BITS:])

		d, e = {}, {}
		for i in dlist:
			d[str(i)] = Signal(bool(0))
			
		d['op'] = Signal(alu_op_type.LD)

		out_dec = [d[str(sig)] for sig in dlist]
	


		# ALU SIGNALS
		# out_list
		alu_acc, alu_opd, alu_res = [Signal(intbv(0)[16:])] * 3
		

		alu_inst = alu.pyleros_alu(out_dec, alu_acc, alu_opd, alu_res)


	
		instr_list, bin_list = [], []


		for instr in codes:
			if codes[instr][2] == False:
				continue

			for trie in range(3):

				op1 = randrange(2**16)
				# 8-bit imm opd
				op2 = randrange(2**8)

				bin_code = conv_bin(instr)
				# Immediate version
				bin_imme = bin_code | 0x01

				instr_list.append([instr, op1, op2])

				#Add operand op2 to instr
				bin_code = (bin_code << 8) | (op2 & 0xff)

				bin_list.append(bin_code)


		fedec_inst = fedec.pyleros_fedec(clock, reset, in_acc, in_dm_data, \
										out_dec, out_imme, out_dm_addr, out_pc, filename=bin_list)


		@always(delay(10))
		def tbclk():
			clock.next = not clock		

			

		@instance
		def tbstim():

			# To start the fetch/decoding
			# reset.next = not reset.active
			# yield delay(12)

			

			# In the first cycle nothing happens since
			# only the instuction is updated, and the 
			# decoder, the output from fedec doesn't change 
			# till after the second cycle.
			yield clock.posedge

			raise Exception

			ninstr = len(instr_list)
			for addr in range(ninstr):


				# for the alu, op1 signifies the acc adn
				# op2 the opd
				instr, op1, op2 = instr_list[addr]

				yield clock.posedge
				yield delay(1)

				alu_acc.next = op1
				alu_opd.next = out_imme

				yield delay(33)

				#check for correct result
				if instr == 'NOP':
					pass

				elif instr == 'ADD':
					assert alu_res == ((op1 + op2) & 0xffff)

				elif instr == 'SUB':
					assert alu_res == ((op1 - op2) & 0xffff)

				elif instr == 'SHR':
					assert alu_res == (op1 & 0xffff) >> 1

				elif instr == 'AND':
					assert alu_res == (op1 & op2) & 0xffff

				elif instr == 'OR':
					assert alu_res == (op1 | op2) & 0xffff

				elif instr == 'XOR':
					assert alu_res == (op1 ^ op2) & 0xffff

				elif instr == 'LOAD':
					assert alu_res == op2 & 0xffff


			


			raise StopSimulation

		return instances()


	# Just decoder and ALU
	top_inst = tb_fedec_top()
	top_inst.run_sim()






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

	test_alu()
	test_sign_extend()