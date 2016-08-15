from myhdl import *
from pyleros.rom import *
from pyleros.types import IM_BITS


def conv_rom():
    instr_list = [i for i in range(2**IM_BITS)]

    clk = Signal(bool(0))
    reset = ResetSignal(0, active = 1, async =True)
    rd_addr = Signal(intbv(0)[IM_BITS:])
    rd_data = Signal(intbv(0)[16:])

    inst_rom = pyleros_im(rd_addr, rd_data, 'ex_mem.txt')

    inst_rom.convert(hdl = 'VHDL')



if __name__ == "__main__":

    conv_rom()

    # Example of ROM conversion
    @block
    def rom(dout, addr, CONTENT):
        @always_comb
        def read():
            dout.next = CONTENT[int(addr)]

        return read

    in_rm = rom(Signal(bool(0)), Signal(intbv(0)[16:]), tuple([False for i in range(256)]))
    in_rm.convert(hdl = 'VHDL')