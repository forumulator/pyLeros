from myhdl import Signal, intbv
from pyleros.alu import pyleros_alu
from pyleros.types import decSignal, alu_op_type, inpSignal
from conversion_info import CONVERSION_PATH as PATH



def conv_alu():

	dec_sig = decSignal()
	alu_op = Signal(alu_op_type.NOP)
	acc = Signal(intbv(0)[16:])
	pre_acc = Signal(intbv(0)[16:])
	opd = Signal(intbv(0)[16:])
	ioin = inpSignal()

	inst_alu = pyleros_alu(alu_op, dec_sig, acc, opd, pre_acc, ioin)
	inst_alu.convert(hdl = 'VHDL', path = PATH)



if __name__ == "__main__":
	conv_alu()