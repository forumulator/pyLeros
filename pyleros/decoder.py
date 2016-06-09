from myhdl import instances, block, Signal, enum
from pyleros.codes import alu_op_type


@block
def pyleros_decoder(instr_hi, op, al_ena, ah_ena, log_add, add_sub, 
					shr, sel_imm, store, outp, inp, br_op, jal,
					loadh, indls):
	"""The decoder module for pyleros, decodes the high bits
	of the instruction and generates the control signals. The modules is
	purely combinatorial. 

	Arguments (ports):
        instr_hi: IN The high 8 bits of the instruction
        op: Indicates the type of ALU operation
        al_ena:  Enables the high bits of the accumulator
        	(Required when the value of the Acc changes)
        ah_ena: Enables the low bits of the accumulator
        	(Required when the value of the Acc changes)
        log_add: For ADD/SUB
        add_sub: Switches between addition and subtration
        shr: Signal shift right operation
		sel_imm: Signal, enabled if o bit(indicating immediate value)
			is high
		store: Signal the store operation
		outp: output in I/O
		inp: input in I/O
		br_op: Signal if the instructio is a branch
		jal: Signal if the instructio is a jump and link
		loadh: Signal if the instructio is a load high
		indls: Signal if the instructio is a indirect load/store

    Parameters:
	    None

	"""
	
	@block
	def decoder():

		# Set the defaults of all signals
		op.next = alu_op_type.LD
		al_ena.next = False
		ah_ena.next = False
		log_add.next = False
		add_sub.next = False
		shr.next = False
		sel_imm.next = False
		store.next = False
		outp.next = False
		inp.next = False
		br_op.next = False
		jal.next = False
		loadh.next = False
		indls.next = False


		# Decode

		add_sub.next = instr_hi[2]

		# the imm. bit, 0
		sel_imm.next = instr_hi[0]

		ins_ckh = instr_hi & 0xf8

		if ins_ckh == 0x00:
			# NOP
			pass

		elif ins_ckh == 0x08:
			# ADD/SUB
			al_ena.next = True
			ah_ena.next = True
			log_add.next = True

		elif ins_ckh == 0x10:			
			# SHR
			al_ena.next = True
			ah_ena.next = True
			shr.next = True

		elif ins_ckh == 0x18:
			# reserved
			pass

		elif ins_ckh == 0x20:
			# ALU_OP : ld, or, and, xor
			al_ena.next = True
			ah_ena.next = True

		elif ins_ckh == 0x28:
			# LOADH
			loadh.next = True
			ah_ena.next = True

		elif ins_ckh == 0x30:
			# STORE
			store.next = True

		elif ins_ckh == 0x38:
			# I/O
			if instr_hi[2] == False:
				# OUT
				outp.next = True
			else:
				# IN
				inp.next = True
				al_ena.next = True
				ah_ena.next = True

		elif ins_ckh == 0x40:
			# JAL
			jal.next = True
			store.next = True

		elif ins_ckh == 0x48:
			# BRANCH
			br_op.next = True

		elif ins_ckh == 0x50:
			# LOADADDR, to be implemented
			pass

		elif ins_ckh == 0x60:
			# LOAD INDIRECT
			al_ena.next = True
			ah_ena.next = True
			indls.next = True

		elif ins_ckh == 0x61:
			# STORE INDIRECT
			indls.next = True
			store.next = True



		# Setting of the signal op as the 
		# alu_op_type
		if instr_hi[2:1] == 0b00:
			# LOAD
			op.next = alu_op_type.LD

		elif instr_hi[2:1] == 0b01:
			# AND
			op.next = alu_op_type.AND

		elif instr_hi[2:1] == 0b10:
			# OR
			op.next = alu_op_type.OR

		elif instr_hi[2:1] == 0b11:
			# XOR
			op.next = alu_op_type.XOR

	return instances()


