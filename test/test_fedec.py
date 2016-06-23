from pyleros import fedec, alu, decoder
from pyleros.fedec import sign_extend
from pyleros.codes import dlist, codes, conv_bin
from pyleros.types import alu_op_type, t_decSignal, IM_BITS, DM_BITS

import pytest

from myhdl import *

import random
from random import randrange
from datetime import datetime

random.seed(int(datetime.now().time().second))

# Test with immediate instructions
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
			e[str(i)] = Signal(bool(0))
			
		d['op'] = Signal(alu_op_type.LD)
		e['op'] = Signal(alu_op_type.LD)

		out_dec = [d[str(sig)] for sig in dlist]
		test_dec = [e[str(sig)] for sig in dlist]
	
		instr_hi = Signal(intbv(0)[8:])
		dec_inst = decoder.pyleros_decoder(instr_hi, test_dec)

		# ALU SIGNALS
		# out_list
		alu_acc = Signal(intbv(0)[16:])
		alu_opd = Signal(intbv(0)[16:])
		alu_res = Signal(intbv(0)[16:])
		

		alu_inst = alu.pyleros_alu(out_dec, alu_acc, alu_opd, alu_res)


	
		instr_list, bin_list = [], []


		for instr in codes:
			if (not codes[instr][2]) or (instr == 'NOP') or (instr == 'LOADH') or (instr == 'STORE'):
				continue

			for trie in range(30):

				op1 = randrange(2**15)
				# 8-bit imm opd
				op2 = randrange(2**7)

				bin_code = codes[instr][0]
				# Immediate version
				bin_imme = bin_code | 0x01

				instr_list.append([instr, op1, op2])

				#Add operand op2 to instr
				bin_code = (bin_imme << 8) | (op2 & 0xff)

				bin_list.append(bin_code)


		fedec_inst = fedec.pyleros_fedec(clock, reset, in_acc, in_dm_data, \
										out_dec, out_imme, out_dm_addr, out_pc, filename=bin_list)


		@always(delay(100))
		def tbclk():
			clock.next = not clock		

			

		@instance
		def tbstim():

			# To start the fetch/decoding
			# reset.next = not reset.active
			

			print("bin_list")
			for i in range(10):
				print(bin_list[i], instr_list[i][2])

			# In the first cycle nothing happens since
			# only the instuction is updated, and the 
			# decoder, the output from fedec doesn't change 
			# till after the second cycle.
			yield delay(12)

			ninstr = len(instr_list)
			for addr in range(1,ninstr):

				# if addr == 10:
				# 	raise StopSimulation
				print(addr)
				# for the alu, op1 signifies the acc adn
				# op2 the opd
				instr, op1, op2 = instr_list[addr]
				instr_hi.next = (codes[instr][0] | 0x01)

				yield clock.posedge
				yield delay(1)
				yield delay(1)

				for sig in dlist:
					print(str(sig))
					assert test_dec[int(sig)] == out_dec[int(sig)]

				print("Cmp Imm", op2, out_imme)
				alu_acc.next = op1
				alu_opd.next = out_imme
				yield delay(20)
				print("alu ops", op1, alu_acc, out_imme, alu_opd)
				print("alu types", type(op1), type(alu_acc), type(out_imme), type(alu_opd))
				print(out_dec[int(t_decSignal.add_sub)], out_dec[int(t_decSignal.log_add)])
				for i in range(2):
					yield delay(33)

				#check for correct result
				if instr == 'NOP':
					pass

				elif instr == 'ADD':
					assert alu_res == int(op1) + int(op2)

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