from pyleros.codes import codes, dlist
from pyleros.types import alu_op_type, t_decSignal

from pyleros import decoder
from myhdl import *

from rhea.system import Clock, Reset

from rhea.utils.test import run_testbench


def test_decode(args=None):
	"""Test the decoder module in pyleros

	"""
	clock = Signal(bool(0))
	reset = Reset(0, active=0, async=True)

	# the high 8 bits of the instruction
	instr_hi = Signal(intbv(0)[8:])

	d = {}
	for i in dlist:
		d[str(i)] = Signal(bool(0))

	d['op'] = Signal(alu_op_type.LD)

	out_list = [d[str(sig)] for sig in dlist]

	@always(delay(10))
	def tbclk():
		clock.next = not clock


	def _bench_dec():


		# instantiate the decoder
		decode_inst = decoder.pyleros_decoder(instr_hi, out_list)

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
					if not cs == t_decSignal.op:
						if cs in codes[instr][1]:
							try:
								assert d[str(cs)] == True
							except Exception as e:
								print(instr)
								print(cs)
								raise e

						else:
							try:
								assert d[str(cs)] == False
							except Exception as e:
								print(instr)
								print(cs)
								raise e

					else:
						if cs in codes[instr][1]:
							assert d[str(cs)] == codes[instr][3]

				yield delay(33)

				if codes[instr][2] == True:

					instr_imm = instr_op | 0x01
					instr_hi.next = instr_imm
					yield delay(33)

					# check for correct decode
					for cs in dlist:
						if not ((cs == t_decSignal.op) or (cs == t_decSignal.sel_imm)):
							if cs in codes[instr][1]:
								try:
									assert d[str(cs)] == True
								except Exception as e:
									print(instr)
									print(cs)
									raise e								
							else:
								
								assert d[str(cs)] == False

						else:
							if cs in codes[instr][1]:
								assert d[str(cs)] == codes[instr][3]

						assert d['sel_imm'] == True

				for ii in range(5):
					yield clock.posedge


			raise StopSimulation

		return tbstim, decode_inst, tbclk

	run_testbench(_bench_dec)


if __name__ == "__main__":

	test_rom()



