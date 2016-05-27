IM_SIZE = 1024
DM_SIZE = 1024

IM, DM = [], []
progSize = 0

acc = 0, pc = 0, ar = 0

# The delay values of the Acc, for the branch and jump instructions
acc_dly, acc_dly1 = 0, 0

def simulate():

	while True:

		acc_dly = acc_dly1
		acc_dly1 = acc

		instr = IM[pc]

		next_pc = pc + 1

		if (pc > progSize):
			return
		# the immediate value from the instruction
		val = 0 

		# check the o bit to find if the operation is in the 
		# imm. category
		if ((instr >> 8) & 0x01) != 0:
			# Use the immediate value

			val = inst & 0xff

			# Sign-extend
			if (val & 0x80) != 0:
				val = val | 0xff00
		else:
			val = DM[val & 0xff]


		oper = (instr & 0xfe00) >> 8

		if oper == 0x00:
			# NOP
			pass

		elif oper == 0x08:
			# ADD
			acc = acc + val

		elif oper == 0x0c:
			# SUB
			acc = acc - val

		elif oper == 0x10:
			# This is the logical shift which can be achieved for 16 bits
			# in python by (-5 + 0x10000) >> n or (-5 & 0xffff) >> n
			# SHR (shift right  by 1)
			acc = (acc >> 1) if (acc > 0) else (acc & 0xffff) >> 1 

		elif oper == 0x20:
			# LOAD
			# either immediate or direct
			acc = val

		elif oper == 0x22:
			# AND
			acc = acc & val

		elif oper == 0x24:
			# Or
			acc = acc | val

		elif oper == 0x26:
			# XOR
			acc = acc ^ val

		elif oper == 0x28:
			# LOADH (load high)
			# lowest 8 bits of the acc and 
			# high 8 from the imm value
			acc = (acc & 0xff) + (val << 8)

		elif oper == 0x30:
			# STORE
			# only as direct
			DM[instr & 0x00ff] = accu

		elif oper == 0x38:
			# OUT
			pass

		elif oper == 0x3c:
			# IN 
			pass

		elif oper == 0x40:
			
			# JAL
			pass

		elif oper == 0x50:
			# LOADADDR
			pass

		elif oper == 0x60:
			acc = dm[ar + (instr & 0xff)]

		elif oper == 0x70:
			# STORE INDIRECT 
			dm[ar + (instr & 0xff)] = acc

		# case 7: // I/O (ld/st indirect)
		# break;
		# case 8: // brl
		# break;
		# case 9: // br conditional
		# break;

		else:

		# BRANCH, use the immediate bit
		# to decode the type of the branch
		# branch, brz, brnz, brp, brn

			brop = instr & 0xff00

			if (brop == 0x4800):

				# BRANCH
				# Assuming 16 - bit instructions
				# with an 8 bit offset for branches
				next_pc = pc + (instr & 0x00ff)

			elif (brop == 0x4900):
				# BRZ
				if (acc_dly == 0):
					next_pc = pc + (instr & 0x00ff)

			elif (brop == 0x4a00):
				# BRNZ
				if (acc_dly != 0):
					next_pc = pc + (instr & 0x00ff)

			elif (brop == 0x4b00):
				# BRP (branch on positive)
				if (acc_dly & 0x8000) == 0:
					next_pc = pc + (instr & 0x00ff)

			elif (brop == 0x4c00):
				# BRN (branch on negative)		
				if (acc_dly & 0x8000) != 0:
					next_pc = pc + (instr & 0x00ff)

			else:
				raise ValueError("Invalid Instruction")