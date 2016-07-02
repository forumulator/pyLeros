from pyleros import decoder, execute
from pyleros.codes import dlist, codes
from pyleros.types import alu_op_type, t_decSignal, IM_BITS, DM_BITS

import pytest

from myhdl import *

import random
from random import randrange
from datetime import datetime

random.seed(int(datetime.now().time().second))


class TestClass:

	@classmethod
	@block
	def setup_class(self):

		self.clock = Signal(bool(0))
		self.reset = ResetSignal(0, active=1, async=True)

		# DECODER SIGNALS
		self.instr_hi = Signal(intbv(0)[8:])

		d = {}
		for i in dlist:
			d[str(i)] = Signal(bool(0))
		
		d['op'] = Signal(alu_op_type.LD)

		self.out_list = [d[str(sig)] for sig in dlist]

		# Input Signals to Execute
		self.in_imm = Signal(intbv(0)[16:])
		self.in_dm_addr = Signal(intbv(0)[DM_BITS:])
		self.in_pc = Signal(intbv(0)[IM_BITS:])

		self.out_acc = Signal(intbv(0)[16:])
		self.out_dm_data = Signal(intbv(0)[16:])

		self.signals = self.clock, self.reset, self.instr_hi, self.out_list, self.in_imm, \
			self.in_dm_addr, self.in_pc, self.out_acc, self.out_dm_data

		self.decode_inst = decoder.pyleros_decoder(self.instr_hi, self.out_list)
		self.exec_inst = execute.pyleros_exec(self.clock, self.reset, self.out_list, self.in_imm, self.in_dm_addr, self.in_pc, \
											self.out_acc, self.out_dm_data)

		return self.decode_inst, self.exec_inst

	def create_instr(self, tup, imm=True):
		"""Create a list of random instructions
		from the list given.

		"""
		instr_list = []
		op = 0

		rr = len(tup)

		for i in range(250):
			instr = tup[randrange(rr)]
			op = randrange(2**8)
			# Add Immediate
			instr_bin = codes[instr][0] | 0x01
			instr_bin = (instr_bin << 8) | intbv(op)[8:]
			instr_list.append((instr, op, instr_bin))

		return instr_list


	def test_arith(self):

		@block
		def tb_arith( args=None):
			"""Test arithametic alu instructions ADD, SUB

			"""
			# Initialise signals and dut's
			clock, reset, instr_hi, out_list, in_imm, \
				in_dm_addr, in_pc, out_acc, out_dm_data = self.signals
			inst_blks = self.decode_inst, self.exec_inst
			
			instr_list = self.create_instr(('ADD', 'SUB'))

			@always(delay(10))
			def tbclk():
				clock.next = not clock

			# the alu is run once on intialization anyway, and the value
			# is set to zero(0 + 0)
			@instance
			def tbstim():
				# local accumulator var
				acc = 0
				yield delay(11) # or yield clock.posedge, same result.

				for addr in range(len(instr_list)):

					instr = instr_list[addr][0]
					op = instr_list[addr][1]
					instr_bin = instr_list[addr][2]
					instr_hi.next = instr_bin[16:8]

					in_imm.next = instr_bin & 0xff
					yield clock.posedge

					if instr == 'ADD':
						assert ((acc + op) & 0xffff) == out_acc
						acc += op
					elif instr == 'SUB':
						assert ((acc - op) & 0xffff) == out_acc
						acc -= op
						acc &= 0xffff	

				raise StopSimulation

			return instances()

		inst = tb_arith()
		inst.run_sim()


	def test_logical(self):

		@block
		def tb_log(args=None):
			"""Test logical alu instructions OR, AND, XOR, SHR

			"""
			# Initialise signals and dut's
			clock, reset, instr_hi, out_list, in_imm, \
				in_dm_addr, in_pc, out_acc, out_dm_data = self.signals
			inst_blks = self.decode_inst, self.exec_inst

			instr_list = self.create_instr(('OR', 'AND', 'XOR', 'SHR'))

			@always(delay(10))
			def tbclk():
				clock.next = not clock

			@instance
			def tbstim():
				# local accumulator var
				acc = 0
				yield delay(11)

				for addr in range(len(instr_list)):

					instr = instr_list[addr][0]
					op = instr_list[addr][1]
					instr_bin = instr_list[addr][2]
					instr_hi.next = instr_bin[16:8]

					in_imm.next = instr_bin & 0xff
					# these two together constitute clock.negedge
					yield clock.posedge

					if instr == 'OR':
						assert ((acc | op) & 0xffff) == out_acc
						acc |= op
					elif instr == 'AND':
						assert ((acc & op) & 0xffff) == out_acc
						acc &= op
					elif instr == 'XOR':
						assert ((acc ^ op) & 0xffff) == out_acc
						acc ^= op
					elif instr == 'SHR':
						acc = ((acc & 0xffff) >> 1)
						assert acc == out_acc
							
					# if addr == 9:
					# 	raise Exception

				raise StopSimulation

			return instances()

		inst = tb_log()
		inst.run_sim()



	# @pytest.mark.skip
	def test_ls(self):

		@block
		def tb_ls(args=None):
			"""Test load store instructions LOAD/ STORE

			"""
			# Initialise signals and dut's
			clock, reset, instr_hi, out_list, in_imm, \
				in_dm_addr, in_pc, out_acc, out_dm_data = self.signals
			inst_blks = self.decode_inst, self.exec_inst

			@always(delay(10))
			def tbclk():
				clock.next = not clock

			@instance
			def tbstim():
				# local accumulator var
				acc = 0
				# reset.next = reset.active
				# yield delay(3)
				# reset.next = not reset.active
				yield delay(2)

				# Test 1: store and read consecutive 256 values
				# store
				for addr in range(256):

					instr_bin = intbv((codes['STORE'][0] << 8) | (addr & 0xff))[16:]
					instr_hi.next = instr_bin[16:8]

					in_dm_addr.next = addr
					in_imm.next = 0
					yield clock.posedge
					# yield delay(2)
					instr_bin = intbv(0x0901)[16:]
					instr_hi.next = instr_bin[16:8]
					in_imm.next = 1
					yield clock.negedge
					# delay(2)
					instr_hi.next = 0x00
					
				instr_hi.next = 0x00
				yield delay(5)

				for addr in range(256):

					instr_bin = intbv(((codes['LOAD'][0] << 8) | 0x01) | (addr & 0xff))[16:]
					instr_hi.next = instr_bin[16:8]

					in_dm_addr.next = addr
					in_imm.next = 0
					yield clock.posedge

					yield clock.posedge
					assert addr == out_acc
					
							
				# raise Exception
				raise StopSimulation

			return instances()

		inst = tb_ls()
		inst.run_sim()



