from myhdl import Signal, intbv
from pyleros.alu import pyleros_alu
from pyleros.types import decSignal, alu_op_type



def conv_alu():

	dec_sig = decSignal()
	alu_op = Signal(alu_op_type.NOP)
	acc = Signal(intbv(0)[16:])
	pre_acc = Signal(intbv(0)[16:])
	opd = Signal(intbv(0)[16:])

	inst_alu = pyleros_alu(alu_op, dec_sig, acc, opd, pre_acc)
	inst_alu.convert(hdl = 'VHDL')



if __name__ == "__main__":
	conv_alu()