from myhdl import Signal, intbv
from pyleros.decoder import pyleros_decoder
from pyleros.types import decSignal, alu_op_type


def conv_decoder():

	dec_sig = decSignal()
	alu_op = Signal(alu_op_type.NOP)
	instr_hi = Signal(intbv(0)[8:])

	inst_dec = pyleros_decoder(instr_hi, alu_op, dec_sig)

	inst_dec.convert(hdl = 'VHDL')




if __name__ == "__main__":
	conv_decoder()