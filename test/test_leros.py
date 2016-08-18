from pyleros.top import pyleros
from pyleros.codes import dlist, codes
from pyleros.types import alu_op_type, dec_op_type, IM_BITS, DM_BITS, decSignal, inpSignal, outpSignal
from pyleros.sim import sim

import pytest

from myhdl import *

import random
from random import randrange
from datetime import datetime

random.seed(int(datetime.now().time().second))



@block
def clk_def(clock):

    @always(delay(10))
    def tbclk():
        clock.next = not clock

    return tbclk

class TestProcessor:

    @classmethod
    def setup_class(self):

        clock = Signal(bool(0))
        reset = ResetSignal(0, active=1, async=True)

        ioin = inpSignal()
        ioout = outpSignal()
        self.signals = clock, reset, ioin, ioout
    
    @block
    def setup_proc(self, filename):
        clock, reset, ioin, ioout = self.signals

        inst_clk = clk_def(clock)
        inst_proc = pyleros(clock, reset, ioin, ioout, filename = filename)

        return instances()


    def test_addn_io(self):

        @block
        def tb_addnio(fname=None):
            """Test io, addition, branching et.c using
            assembeled files. 

            """

            clock, reset, ioin, ioout = self.signals
            proc_inst = self.setup_proc(fname)

            @instance
            def tbstim():
                n = 15
                num_list = [n]
                num_list.extend([randrange(2**4) for i in range(n)])
                print(num_list)
                ind = 0

                while 1:
                    
                    yield clock.posedge
                    # print("CLOCK ----------------------------------------------------")
                    yield delay(4)
                    if ioout.rd_strobe == 1:
                        if ioout.io_addr == 0:
                            # print("INPUT HERE")
                            ioin.rd_data.next = num_list[ind]
                            ind += 1
                    elif ioout.wr_strobe == 1:
                        if ioout.io_addr == 1:
                            yield delay(7)
                            assert ioout.wr_data == sum(num_list[:ind]) - n
                            raise StopSimulation


            return instances()

        path = '../generated/rom/'
        test_files = ['io_test.rom', 'iot_2.rom', 'io_br.rom', 'jal.rom', 'sum_n.rom']
        for fname in test_files:
            inst = tb_addnio(path + fname)
            inst.run_sim()



    def test_sort(self):

        @block
        def tb_sort(fname=None):
            """Test bubble sort

            """

            clock, reset, ioin, ioout = self.signals
            proc_inst = self.setup_proc(fname)

            @instance
            def tbstim():
                n = randrange(40)
                num_list = [n]
                num_list.extend([randrange(2**8) for i in range(n)])
                print(num_list)
                ind = 0
                op_count = 0
                out_list = []
                while 1:
                    
                    yield clock.posedge
                    # print("CLOCK ----------------------------------------------------")
                    yield delay(4)
                    if ioout.rd_strobe == 1:
                        if ioout.io_addr == 0:
                            # print("INPUT HERE")
                            ioin.rd_data.next = num_list[ind]
                            ind += 1
                    elif ioout.wr_strobe == 1:
                        if ioout.io_addr == 1:
                            yield delay(7)
                            out_list.append(int(ioout.wr_data))
                            op_count += 1
                            if op_count == n:
                                break

                out_list.reverse()
                num_list = sorted(num_list[1:])
                print(out_list)
                for i in range(n):
                    assert out_list[i] == num_list[i]

                raise StopSimulation


            return instances()

        path = '../generated/rom/'
        test_files = ['bub_sort.rom']
        for fname in test_files:
            inst = tb_sort(path + fname)
            inst.run_sim()      