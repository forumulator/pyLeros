import sys
import os


IM_SIZE = 1024
DM_SIZE = 1024

IM, DM = [0 for i in range(IM_SIZE)], [0 for i in range(DM_SIZE)]
progSize = 0

acc = 0; pc = 0; ar = 0

# The delay values of the Acc, for the branch and jump instructions
acc_dly, acc_dly1 = 0, 0
executedInstr = 0


# The simulate function simulates the behaviour of the
# CPU by interpreting from the list of instructions (the IM)
# and loading and storing from the data memory using a variable for 
# the accumulator. Note that the processor is only suppposed to work 
# on 16-bit binary registers. However, the length of integers in python
# is often dynamic and as needed; this is addressed by ensuring that
# the loads and stores only store and load the last 16 bits by 
# using a bitwise and with the number 0xffff. In the input and output, then,
# the stored results can be interpreted as required.
def simulate():

	global acc, pc, ar, acc_dly, acc_dly1, executedInstr
	while True:

		acc_dly = acc_dly1
		acc_dly1 = acc

		instr = IM[pc]

		next_pc = pc + 1

		if (pc > progSize):
			print("Executed = " + str(executedInstr))
			return 0
		# the immediate value from the instruction
		val = 0 

		# check the o bit to find if the operation is in the 
		# imm. category
		if ((instr >> 8) & 0x01) != 0:
			# Use the immediate value

			val = instr & 0xff

			# Sign-extend
			if (val & 0x80) != 0:
				val = val | 0xff00
		else:
			val = DM[val & 0xff]


		# get the opcode and 
		# EXECUTE the instruction
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
			acc = (val & 0xffff)

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
			DM[instr & 0x00ff] = (acc & 0xffff)

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
			acc = (DM[ar + (instr & 0xff)] & 0xffff)

		elif oper == 0x70:
			# STORE INDIRECT 
			DM[ar + (instr & 0xff)] = (acc & 0xffff)

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
				raise ValueError("Invalid Instruction at address " + str(pc) + \
					" : " + str(instr))

		executedInstr += 1
		acc = acc & 0xff 

		ar = DM[instr & 0xff]

		pc = next_pc



def instr_load(filename):

	global progSize
	src_file = open(filename,"rb")
	if not src_file:
		i = 1
	for line in src_file:

		# Comments and empty lines
		if len(line) == 0:
			continue
		if line[0] == '#':
			continue


		instr_bin = line.split()[0]
		
		if len(instr_bin) != 16:
			return 1

		try:
			instr_int = int(instr_bin, 2)
			IM[i] = instr_int
			i = i + 1

		except ValueError:
			return 1

	src_file.close()

	progSize = i
	return 0

def mem_dump(succ):

	global progSize, pc, acc

	f = open("mem_dmp", "wb")
	if succ == True:
		print("Simulation Successful\n", file = f)
		print("Program Size = " + progSize + "\n\n", file = f)
		print("Executed instructions = " + executedInstr + "\n\n", file = f)
		
		print("A " + bin(acc)[2:].zfill(16) + "   " + str(acc) + "\n", file = f)
		print("PC " + bin(pc)[2:].zfill(16) + "   " + str(pc) + "\n\n", file = f)

		print("Data Memory\n", file = f)
		for i in range(257):
			print(str(i) + " " + bin(DM[i])[2:].zfill(16) + "   " + str(DM[i]) + "\n", file = f)

		print("\n\n", file = f)

		print("Instruction Memory\n", file = f)
		for i in range(progSize):
			print(str(i + 1) + " " + bin(IM[i + 1])[2:].zfill(16) + "   " + str(IM[i + 1]) + "\n", file = f)


def main():

	# Check for arguments
	# to be switched to python parser
	narg = len(sys.argv)
	global progSize
	usage = "Usage: python lerosSim [-qio] filename"
	if  (narg < 2):
		print(usage)
		exit(1)


	filename = sys.argv[narg - 1]

	# check for file exist
	if os.path.exists(filename) == False:
		raise FileNotFoundError('Source file does not exist')

	load_stat = instr_load(filename)
	if load_stat == 1:
		raise ValueError('File not in proper format')

	else:
		print("Instruction Memory has " + str(progSize) + " words\n")
		sim_stat = simulate()
		if sim_stat == 0:
			mem_dump(True)

	




if __name__ == '__main__':
	main()