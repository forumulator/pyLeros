from pyleros import ram
from pyleros.types import DM_BITS

from myhdl import *

import pytest

import random
from random import randrange
from datetime import datetime

random.seed(int(datetime.now().time().second))

@block
def testbench_ram(args=None):
    """Test the data memory module in pyleros

    """
    clock = Signal(bool(0))
    reset = ResetSignal(0, active=1, async=True)

    rd_addr, wr_addr = [Signal(intbv(0)[DM_BITS:])] * 2
    rd_data, wr_data = [Signal(intbv(0)[16:])] * 2
    wr_en = Signal(bool(0))

    DM_SIZE = 2**DM_BITS
    data_array = [0 for _ in range(DM_SIZE)]

    @always(delay(10))
    def tbclk():
        clock.next = not clock

    dm_inst = ram.pyleros_dm(clock, reset, rd_addr, wr_addr, wr_data, wr_en, rd_data)

    
    for i in range(DM_SIZE):
        data_array[i] = randrange(2**15) - 2**14

    @instance
    def tbstim():

        # reset.next = 0
        # yield delay(33)
        
        # for i in range(5):
        yield clock.posedge

        # write all the data
        for addr in range(DM_SIZE):
            print(data_array[addr])

        for addr in range(DM_SIZE):

            wr_addr.next = intbv(addr)[DM_BITS:]
            wr_data.next = intbv(data_array[addr])[16:]
            wr_en.next = True
            
            yield clock.posedge

            yield delay(1)

            wr_en.next = False

        for i in range(5):
            yield clock.posedge 

        # Verify the written data
        for tryn in range(DM_SIZE):
            print(tryn)
            addr = randrange(DM_SIZE)
            rd_addr.next = addr

            yield clock.posedge

            yield delay(1)

            # if not rd_data == 0:
            assert (rd_data & 0xffff) == (data_array[addr] & 0xffff)


        raise StopSimulation

    return instances()


def test_ram():
    tb_inst = testbench_ram()
    tb_inst.run_sim()



if __name__ == "__main__":

    test_ram()


