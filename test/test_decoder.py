from pyleros.codes import codes, dlist, alu_op_type

from pyleros import decoder
from myhdl import *

from rhea.system import Clock, Reset

from rhea.utils.test import run_testbench


def test_decode(args=None):
	"""Test the decoder module in pyleros

	"""
	clock = Clock(0, frequency=50e6)
	reset = Reset(0, active=0, async=True)

	# the high 8 bits of the instruction
	instr_hi = Signal(intbv(0)[8:])

	d = {}
	for i in dlist:
		d[i] = Signal(bool(0))

	d['cs'] = Signal(alu_op_type.LD)


	def _bench_dec():

		# instantiate the decoder
		decode_inst = decoder.pyleros_decoder(instr_hi, d['op'], d['al_ena'], d['ah_ena'], d['log_add'], d['add_sub'], 
					d['shr'], d['sel_imm'], d['store'], d['outp'], d['inp'], d['br_op'], d['jal'],
					d['loadh'], d['indls'])

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
					if not cs == 'op':
						if cs in codes[instr][1]:
							assert d[cs] == True

						else:
							assert d[cs] == False

					else:
						if cs in codes[instr][1]:
							assert d[cs] == codes[instr][3]

				yield delay(33)

				if codes[instr][2] == True:

					instr_imm = instr_op | 0x01
					instr_hi.next = instr_op
					yield delay(33)

					# check for correct decode
					for cs in dlist:
						if not cs == 'op':
							if cs in codes[instr][1]:
								assert d[cs] == True

							else:
								assert d[cs] == False

						else:
							if cs in codes[instr][1]:
								assert d[cs] == codes[instr][3]

						assert d['sel_imm'] == True

				for ii in range(5):
					yield clock.posedge


			raise StopSimulation

		return tbstim, decode_inst

	run_testbench(_bench_dec)






