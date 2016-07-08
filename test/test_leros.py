from pyleros import fedec, execute
from pyleros.codes import dlist, codes
from pyleros.types import alu_op_type, t_decSignal, IM_BITS, DM_BITS

import pytest

from myhdl import *

import random
from random import randrange
from datetime import datetime

random.seed(int(datetime.now().time().second))


class TestClass1:

	@classmethod
	@block
	def setup_class(self):

		self.clock = Signal(bool(0))
		self.reset = ResetSignal(0, active=1, async=True)

		# DECODER SIGNALS

		d = {}
		for i in dlist:
			d[str(i)] = Signal(bool(0))
		
		d['op'] = Signal(alu_op_type.LD)

		self.pipe_dec = [d[str(sig)] for sig in dlist]

		# Input Signals to Execute
		self.pipe_imme = Signal(intbv(0)[16:])
		self.pipe_dm_addr = Signal(intbv(0)[DM_BITS:])
		self.pipe_pc = Signal(intbv(0)[IM_BITS:])

		self.back_acc = Signal(intbv(0)[16:])
		self.back_dm_data = Signal(intbv(0)[16:])

		self.signals = self.clock, self.reset, self.pipe_dec, self.pipe_imme, \
			self.pipe_dm_addr, self.pipe_pc, self.back_acc, self.back_dm_data

		tup = tuple(['ADD', 'SUB', 'OR', 'AND', 'XOR', 'SHR', 'LOAD'])
		self.instr_list, bin_list = self.create_instr(self, tup)

		self.fedec_inst = fedec.pyleros_fedec(self.clock, self.reset, self.back_acc, self.back_dm_data, \
										self.pipe_dec, self.pipe_imme, self.pipe_dm_addr, self.pipe_pc, filename=bin_list)
		self.exec_inst = execute.pyleros_exec(self.clock, self.reset, self.pipe_dec, self.pipe_imme, self.pipe_dm_addr, self.pipe_pc, \
											self.back_acc, self.back_dm_data)

		return self.fedec_inst, self.exec_inst

	def create_instr(self, tup, imm=True):
		"""Create a list of random instructions
		from the list given.

		"""
		instr_list, bin_list = [], []
		op = 0

		rr = len(tup)

		for i in range(250):
			instr = tup[randrange(rr)]
			op = randrange(2**8)
			# Add Immediate
			instr_bin = codes[instr][0] | 0x01
			instr_bin = (instr_bin << 8) | intbv(op)[8:]
			instr_list.append((instr, op, instr_bin))

		for i in range(len(instr_list)):
			bin_list.append(instr_list[i][2])

		return instr_list, bin_list


	def test_arith(self):

		@block
		def tb_arith_log( args=None):
			"""Test arithametic and logical instructions

			"""
			# Initialise signals and dut's
			clock, reset, out_list, in_imm, \
				in_dm_addr, in_pc, out_acc, out_dm_data = self.signals
			inst_blks = self.fedec_inst, self.exec_inst
			
			instr_list = self.instr_list

			@always(delay(10))
			def tbclk():
				clock.next = not clock

			# the alu is run once on intialization anyway, and the value
			# is set to zero(0 + 0)
			@instance
			def tbstim():
				# local accumulator var
				acc = 0
				# yield delay(11) # or yield clock.posedge, same result.
				# yield clock.posedge
				yield clock.posedge

				for addr in range(1, len(instr_list)):

					instr = instr_list[addr][0]
					op = instr_list[addr][1]
					instr_bin = instr_list[addr][2]

					yield clock.posedge
					yield delay(3)
					print("This is iteration " + str(addr))
					if addr == 0:
						print("At 0x00:", instr, op, out_acc)
					if instr == 'ADD':
						assert ((acc + op) & 0xffff) == out_acc
						acc += op
					elif instr == 'SUB':
						assert ((acc - op) & 0xffff) == out_acc
						acc -= op
						acc &= 0xffff
					elif instr == 'OR':
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
					elif instr == 'LOAD':
						acc = op
						assert acc == out_acc

				raise StopSimulation

			return instances()

		inst = tb_arith_log()
		inst.run_sim()


class TestClass2:

	@classmethod
	@block
	def setup_class(self):

		self.clock = Signal(bool(1))
		self.reset = ResetSignal(0, active=1, async=True)

		# DECODER SIGNALS

		d = {}
		for i in dlist:
			d[str(i)] = Signal(bool(0))
		
		d['op'] = Signal(alu_op_type.LD)

		self.pipe_dec = [d[str(sig)] for sig in dlist]

		# Input Signals to Execute
		self.pipe_imme = Signal(intbv(0)[16:])
		self.pipe_dm_addr = Signal(intbv(0)[DM_BITS:])
		self.pipe_pc = Signal(intbv(0)[IM_BITS:])

		self.back_acc = Signal(intbv(0)[16:])
		self.back_dm_data = Signal(intbv(0)[16:])

		self.signals = self.clock, self.reset, self.pipe_dec, self.pipe_imme, \
			self.pipe_dm_addr, self.pipe_pc, self.back_acc, self.back_dm_data

		self.instr_list, bin_list = self.create_instr(self)

		self.fedec_inst = fedec.pyleros_fedec(self.clock, self.reset, self.back_acc, self.back_dm_data, \
										self.pipe_dec, self.pipe_imme, self.pipe_dm_addr, self.pipe_pc, filename=bin_list)
		self.exec_inst = execute.pyleros_exec(self.clock, self.reset, self.pipe_dec, self.pipe_imme, self.pipe_dm_addr, self.pipe_pc, \
											self.back_acc, self.back_dm_data)

		return self.fedec_inst, self.exec_inst

	def create_instr(self, imm=False):
		"""Create a list of random instructions
		from the list given.

		"""
		instr_list, bin_list = [], []
		op = 0
		flg = 1
		for i in range( 100):
			# STORE current value
			instr = 'STORE'
			addr = i
			instr_bin = codes[instr][0]
			instr_bin = (instr_bin << 8) | intbv(addr)[8:]
			instr_list.append((instr, addr, instr_bin))

			# ADD 1
			instr = 'ADD'
			op = 1
			instr_bin = ((codes[instr][0] | flg) << 8) | intbv(op)[8:]
			instr_list.append((instr, op, instr_bin))
			flg = 0

		for i in range(100):
			instr = 'LOAD'	
			addr = i
			instr_bin = (codes[instr][0] << 8) | intbv(addr)[8:]
			instr_list.append((instr, addr, instr_bin))

		for i in range(len(instr_list)):
			bin_list.append(instr_list[i][2])

		print(len(bin_list))

		return instr_list, bin_list


	def test_arith(self):

		@block
		def tb_arith_log( args=None):
			"""Test arithametic and logical instructions.

			"""
			# Initialise signals and dut's
			clock, reset, out_list, in_imm, \
				in_dm_addr, in_pc, out_acc, out_dm_data = self.signals
			inst_blks = self.fedec_inst, self.exec_inst
			
			instr_list = self.instr_list

			@always(delay(10))
			def tbclk():
				clock.next = not clock

			# the alu is run once on intialization anyway, and the value
			# is set to zero(0 + 0)
			@instance
			def tbstim():
				# local accumulator var
				acc = 0
				# yield delay(11) # or yield clock.posedge, same result.
				yield clock.posedge
				yield delay(1)
				addr = 0
				for addr in range(1, 200):

					instr = instr_list[addr][0]
					op = instr_list[addr][1]
					instr_bin = instr_list[addr][2]
					# print("Bf", addr, out_acc)
					yield clock.posedge

					yield delay(1)
					# print("Af", addr,  out_acc)
					# print("This is iteration " + str(addr))
					if instr == 'ADD':
						acc += op
						assert (acc & 0xffff) == out_acc
					elif instr == 'STORE':
						acc == out_acc

				for addr in range(100):
					mod_addr = addr + 200
					instr = instr_list[mod_addr][0]
					op = instr_list[mod_addr][1]
					instr_bin = instr_list[mod_addr][2]

					yield clock.posedge
					yield delay(1)

					if instr == 'LOAD':
						assert addr == out_acc

				raise StopSimulation

			return instances()

		inst = tb_arith_log()
		inst.run_sim()