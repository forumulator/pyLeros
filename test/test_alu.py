from pyleros import alu, decoder, rom
from pyleros.types import IM_BITS, DM_BITS, alu_op_type, dec_op_type
from pyleros.codes import codes, dlist, conv_bin

import pytest

from myhdl import *

from rhea.utils.test import run_testbench

import random
from random import randrange
from datetime import datetime

random.seed(int(datetime.now().time().second))

# Test bench to test ALU working along with the decoder
def test_alu():
    
    @block
    def tb_alu_top(imen=False):
        """Test the alu module in pyleros

        """

        clock = Signal(bool(0))
        reset = ResetSignal(0, active=1, async=True)

        # DECODER SIGNALS
        instr_hi = Signal(intbv(0)[8:])

        dec_signal_list = [Signal(bool(0)) for sig in dlist]
        alu_op = Signal(alu_op_type.NOP)

        decode_inst = decoder.pyleros_decoder(instr_hi, alu_op, dec_signal_list)

        # ALU SIGNALS
        # dec_signal_list
        alu_acc = Signal(intbv(0)[16:])
        alu_opd = Signal(intbv(0)[16:])
        alu_res = Signal(intbv(0)[16:])

        alu_inst = alu.pyleros_alu(alu_op, dec_signal_list, alu_acc, alu_opd, alu_res)


        rd_addr = Signal(intbv(0)[IM_BITS:])
        rd_data = Signal(intbv(0)[16:])
        instr_list, bin_list = [], []
        # Create instruction memory if enabled.
        if imen:
            for instr in codes:

                for trie in range(20):

                    op1 = randrange(2**15)
                    op2 = randrange(2**15)

                    bin_code = codes[instr][0]

                    instr_list.append([instr, op1, op2])
                    bin_code = (bin_code << 8)

                    bin_list.append(bin_code)

            inst_im = rom.pyleros_im(clock, reset, rd_addr, rd_data, filename=bin_list)



        @always(delay(10))
        def tbclk():
            clock.next = not clock

        

        # def _bench_alu():
            

        @instance
        def tbstim():

            for i in range(5):
                yield clock.posedge

            if imen:

                ninstr = len(instr_list)
                for addr in range(ninstr):
                    instr, op1, op2 = instr_list[addr]

                    rd_addr.next = intbv(addr)[IM_BITS:]

                    yield clock.posedge
                    yield delay(2)

                    assert rd_data == bin_list[rd_addr]
                    upp = (int(rd_data)) >> 8
                    assert upp == codes[instr][0]
                    instr_hi.next = intbv(upp)[8:]

                    alu_acc.next = op1
                    alu_opd.next = op2

                    yield delay(33)

                    #check for correct result
                    if instr == 'NOP':
                        pass

                    elif instr == 'ADD':
                        assert alu_res == ((op1 + op2) & 0xffff)

                    elif instr == 'SUB':
                        assert alu_res == ((op1 - op2) & 0xffff)

                    elif instr == 'SHR':
                        assert alu_res == (op1 & 0xffff) >> 1

                    elif instr == 'AND':
                        assert alu_res == (op1 & op2) & 0xffff

                    elif instr == 'OR':
                        assert alu_res == (op1 | op2) & 0xffff

                    elif instr == 'XOR':
                        assert alu_res == (op1 ^ op2) & 0xffff

                    elif instr == 'LOAD':
                        assert alu_res == op2 & 0xffff


            else:

                for instr in codes:

                    for i in range(10):
                        # Choose random operands
                        op1 = randrange(2**15)
                        op2 = randrange(2**15)

                        # Set the decoder input
                        instr_op = codes[instr][0]
                        instr_hi.next = instr_op
                        
                        alu_acc.next = op1
                        alu_opd.next = op2

                        # Wait for operation
                        yield delay(33)

                        #check for correct result
                        if instr == 'NOP':
                            pass

                        elif instr == 'ADD':
                            assert alu_res == ((op1 + op2) & 0xffff)

                        elif instr == 'SUB':
                            assert alu_res == ((op1 - op2) & 0xffff)

                        elif instr == 'SHR':
                            assert alu_res == (op1 & 0xffff) >> 1

                        elif instr == 'AND':
                            assert alu_res == (op1 & op2) & 0xffff

                        elif instr == 'OR':
                            assert alu_res == (op1 | op2) & 0xffff

                        elif instr == 'XOR':
                            assert alu_res == (op1 ^ op2) & 0xffff

                        elif instr == 'LOAD':
                            assert alu_res == op2 & 0xffff


            raise StopSimulation

        return instances() #, decode_inst




# Currently failing, both with manual
# and decoder use. 


    # Just decoder and ALU
    top_inst = tb_alu_top(False)
    top_inst.run_sim()

    # Along with the instruction memory
    top_inst = tb_alu_top(True)
    top_inst.run_sim()


if __name__ == "__main__":

    test_alu()


