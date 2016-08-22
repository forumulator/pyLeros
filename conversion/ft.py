from myhdl import block, always_seq, Signal, intbv, ResetSignal


@block
def first_func(clock, reset, inp, outp):

	@always_seq(clock.posedge, reset)
	def dff():
		outp.next = inp

	return dff

inp = Signal(bool(0))
outp = Signal(bool(0))
clk = Signal(bool(0))
rst = ResetSignal(0, active = 1, async = True)
inst = first_func(clk, rst, inp, outp)
inst.convert(hdl='VHDL')
