from myhdl import *



@block
def pyleros_decoder(instr_hi, op, al_ena, ah_ena, log_add, add_sub, 
					shr, sel_imm, store, outp, inp, br_op, jal,
					loadh, indls):
	"""The decoder module for pyleros, decodes the high bits
	of the instruction and generates the control signals. The modules is
	purely combinatorial. 

	Arguments (ports):
        instr_hi: IN The high 8 bits of the instruction
        op: 
        al_ena:  
        ah_ena: 
        log_add:  
        add_sub:
        shr:
		sel_imm:
		store: 
		outp: 
		inp: 
		br_op: 
		jal:
		loadh:
		indls:

    Parameters:
	    None

	"""
	pass