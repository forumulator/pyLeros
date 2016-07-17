from pyleros.codes import codes, dlist
from pyleros.types import alu_op_type, dec_op_type

from pyleros import decoder
from myhdl import *


@block
def tb_dec_top(args=None):
	"""Test the decoder module in pyleros

	"""
	clock = Signal(bool(0))
	reset = ResetSignal(0, active=0, async=True)

	# the high 8 bits of the instruction
	instr_hi = Signal(intbv(0)[8:])

	dec_signal_list = [Signal(bool(0)) for sig in dlist]
	alu_op = Signal(alu_op_type.NOP)

	@always(delay(10))
	def tbclk():
		clock.next = not clock



	# instantiate the decoder
	decode_inst = decoder.pyleros_decoder(instr_hi, alu_op, dec_signal_list)

	@instance
	def tbstim():

		for i in range(5):
			yield clock.posedge

		for instr in codes:

			# set the input to the decoder
			instr_op = codes[instr][0]
			instr_hi.next = instr_op
			yield delay(33)

			# check for correct decode
			for cs in dlist:
				if cs in codes[instr][1]:
					assert dec_signal_list[int(cs)] == True
				else:
					assert dec_signal_list[int(cs)] == False


			yield delay(33)

			if codes[instr][2] == True:

				instr_imm = instr_op | 0x01
				instr_hi.next = instr_imm
				yield delay(33)

				# check for correct decode
				for cs in dlist:

					if (cs in codes[instr][1]) or (cs == dec_op_type.sel_imm):
						assert dec_signal_list[int(cs)] == True
					else:
						assert dec_signal_list[int(cs)] == False

			for ii in range(5):
				yield clock.posedge


		raise StopSimulation

	return instances()


def test_decoder():

	inst_top = tb_dec_top()
	inst_top.run_sim()

if __name__ == "__main__":

	test_decoder()



