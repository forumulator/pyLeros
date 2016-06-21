import myhdl
from myhdl import instances, block, Signal, intbv, enum, \
					always_comb, always_seq

from pyleros.types import alu_op_type, t_decSignal, IM_BITS, DM_BITS



@block
def pyleros_alu(dec, acc, opd, pre_acc):
	"""The alu module for pyleros, purely combinatorial

	Arguments (ports):
        dec: IN The decoder control signals
        acc: IN The accumulator
        opd: IN Operand, based on whether the instruction is 
        	immediate or not
        pre_acc: OUT The result of the ALU operation, from the acc mux

    Parameters:
	    None
	"""

	res_arith, res_log = intbv(0)[16:], intbv(0)[16:]

	# Add and Subtract module
	@always_comb
	def op_add_sub():

		if dec[int(t_decSignal.add_sub)] == False:
			res_arith = int((acc + opd) & 0xffff)
		else:
			res_arith = int((acc - opd) & 0xffff)

	# for the logical operations
	# @always_comb
	# def op_logical():

		if dec[int(t_decSignal.op)] == alu_op_type.LD:
			# LOAD
			res_log = int(opd)

		elif dec[int(t_decSignal.op)] == alu_op_type.AND:
			# AND
			res_log = int(acc & opd)

		elif dec[int(t_decSignal.op)] == alu_op_type.OR:
			# OR
			res_log = int(acc | opd)

		elif dec[int(t_decSignal.op)] == alu_op_type.XOR:
			# XOR
			res_log = int(acc ^ opd)

	# MUX to select which result goes into the accumulator
	# based on the decoder control signals
	# @always_comb
	# def acc_mux():
		if dec[int(t_decSignal.log_add)] == True:
			# ADD/ SUB
			pre_acc.next = res_arith

		else:
			if dec[int(t_decSignal.shr)] == True:
				# SHR
				pre_acc.next = intbv(acc >> 1)[16:]

			else:
				# LOGICAL OPERATION
				pre_acc.next = intbv(res_log)[16:]


	return instances()



# Sign extend an intbv or Signal to specified number of bits
def sign_extend(num, bits = 0):

	if (type(num) is intbv) or (type(num) is myhdl._Signal._Signal):
		len_n = len(num)
		sign_bit = int(num[len_n - 1])
		num = ((sign_bit << len_n) * -1) + int(num[len_n:])
		if bits != 0:
			if -2**(bits-1) <= num <= (2**(bits-1) - 1) :
				num = num & ((1 << bits) - 1)
			else:
				raise ValueError("Value " + str(num) + " too large to sign extend")
		return num

	else:
		raise TypeError("Input needs to be " + str(type(Signal())) + ' or ' + str(type(intbv(0))))
