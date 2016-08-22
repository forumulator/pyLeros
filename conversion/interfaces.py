from myhdl import *

class Complex:
    def __init__(self, min=-2, max=2):
        self.real = Signal(bool(0))
        self.imag = Signal(intbv(0, min=min, max=max))

@block
def complex_multiply(clock, reset, a, b, c, lst):

    @always_seq(clock.posedge, reset=reset)
    def cmult():
        lst[0].next = a.real
        lst[1].next = b.imag
        c.real.next = (a.real*b.real) - (a.imag*b.imag)
        c.imag.next = (a.real*b.imag) + (a.imag*b.real)

    return cmult



a,b = Complex(-8,8), Complex(-8,8)
c = Complex(-128,128)

lst = [Signal(intbv(0)[16:]) for i in range(10)]
clock = Signal(bool(0))
reset = ResetSignal(0, active = 1, async = True)

inst = complex_multiply(clock, reset, a, b, c, lst)
inst.convert(hdl = 'VHDL')