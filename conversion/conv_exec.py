from myhdl import Signal, intbv, ResetSignal
from pyleros.execute import pyleros_exec

from conversion_info import CONVERSION_PATH as PATH
from pyleros.types import decSignal, IM_BITS, DM_BITS, alu_op_type, inpSignal

def conv_exec():

	clock = Signal(bool(0))
	reset = ResetSignal(0, active=1, async=True)

	pipe_dec = decSignal()

	# Input Signals to Execute
	pipe_imme = Signal(intbv(0)[16:])
	pipe_dm_addr = Signal(intbv(0)[DM_BITS:])
	pipe_pc = Signal(intbv(0)[IM_BITS:])

	back_acc = Signal(intbv(0)[16:])
	back_dm_data = Signal(intbv(0)[16:])

	fwd_accu = Signal(intbv(0)[16:])
	pipe_alu_op = Signal(alu_op_type.NOP)
	ioin = inpSignal()

	exec_inst = pyleros_exec(clock, reset, pipe_alu_op, pipe_dec, pipe_imme, pipe_dm_addr, pipe_pc, \
                                        back_acc, back_dm_data, fwd_accu, ioin)
	exec_inst.convert(hdl = 'VHDL', path = PATH)




if __name__ == "__main__":
	conv_exec()