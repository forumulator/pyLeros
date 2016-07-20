from pyleros import fedec, execute
from pyleros.codes import dlist, codes
from pyleros.types import alu_op_type, dec_op_type, IM_BITS, DM_BITS

import pytest

from myhdl import *

import random
from random import randrange
from datetime import datetime

random.seed(int(datetime.now().time().second))


class TestClass:

    @classmethod
    def setup_class(self):

        clock = Signal(bool(0))
        reset = ResetSignal(0, active=1, async=True)

        # DECODER SIGNALS


        pipe_dec = [Signal(bool(0)) for sig in dlist]

        # Input Signals to Execute
        pipe_imme = Signal(intbv(0)[16:])
        pipe_dm_addr = Signal(intbv(0)[DM_BITS:])
        pipe_pc = Signal(intbv(0)[IM_BITS:])

        back_acc = Signal(intbv(0)[16:])
        back_dm_data = Signal(intbv(0)[16:])

        self.signals = clock, reset, pipe_dec, pipe_imme, \
            pipe_dm_addr, pipe_pc, back_acc, back_dm_data

        self.fwd_accu = Signal(intbv(0)[16:])
        self.pipe_alu_op = Signal(alu_op_type.NOP)
    


    def test_arith(self):

        @block
        def tb_arith_log( args=None):
            """Test arithametic and logical instructions

            """

            def create_instr(tup, imm=True):
                """Create a list of random instructions
                from the list given.

                """
                instr_list, bin_list = [], []
                op = 0

                rr = len(tup)

                for i in range(250):
                    instr = tup[randrange(rr)]
                    op = randrange(2**8)
                    # Add Immediate
                    instr_bin = codes[instr][0] | 0x01
                    instr_bin = (instr_bin << 8) | intbv(op)[8:]
                    instr_list.append((instr, op, instr_bin))

                for i in range(len(instr_list)):
                    bin_list.append(instr_list[i][2])

                return instr_list, bin_list

            tup = tuple(['ADD', 'SUB', 'OR', 'AND', 'XOR', 'SHR', 'LOAD'])
            instr_list, bin_list = create_instr(tup)

            # Initialise signals and dut's
            clock, reset, pipe_dec, pipe_imme, \
                pipe_dm_addr, pipe_pc, back_acc, back_dm_data = self.signals
            back_dm_data, back_acc = back_dm_data, back_acc
            
            fedec_inst = fedec.pyleros_fedec(clock, reset, back_acc, back_dm_data, self.fwd_accu, \
                                        self.pipe_alu_op, pipe_dec, pipe_imme, pipe_dm_addr, pipe_pc, filename=bin_list, debug=True)
            exec_inst = execute.pyleros_exec(clock, reset, self.pipe_alu_op, pipe_dec, pipe_imme, pipe_dm_addr, pipe_pc, \
                                            back_acc, back_dm_data, self.fwd_accu, True)

            @always(delay(10))
            def tbclk():
                clock.next = not clock

            # the alu is run once on intialization anyway, and the value
            # is set to zero(0 + 0)
            @instance
            def tbstim():
                # local accumulator var
                acc = 0
                # yield delay(11) # or yield clock.posedge, same result.
                # yield clock.posedge
                yield clock.posedge

                for addr in range(1, len(instr_list)):

                    instr = instr_list[addr][0]
                    op = instr_list[addr][1]
                    instr_bin = instr_list[addr][2]

                    yield clock.posedge
                    yield delay(3)
                    print("This is iteration " + str(addr))
                    if addr == 0:
                        print("At 0x00:", instr, op, back_acc)
                    if instr == 'ADD':
                        assert ((acc + op) & 0xffff) == back_acc
                        acc += op
                    elif instr == 'SUB':
                        assert ((acc - op) & 0xffff) == back_acc
                        acc -= op
                        acc &= 0xffff
                    elif instr == 'OR':
                        assert ((acc | op) & 0xffff) == back_acc
                        acc |= op
                    elif instr == 'AND':
                        assert ((acc & op) & 0xffff) == back_acc
                        acc &= op
                    elif instr == 'XOR':
                        assert ((acc ^ op) & 0xffff) == back_acc
                        acc ^= op
                    elif instr == 'SHR':
                        acc = ((acc & 0xffff) >> 1)
                        assert acc == back_acc
                    elif instr == 'LOAD':
                        acc = op
                        assert acc == back_acc

                raise StopSimulation

            return instances()

        inst = tb_arith_log()
        inst.run_sim()   


    def test_ls(self):

        @block
        def tb_ls( args=None):
            """Test load/store instructions

            """
            def create_instr(imm=False):
                """Create a list of instructions.

                """
                instr_list, bin_list = [], []
                op = 0
                flg = 1
                for i in range( 10):
                    # STORE current value
                    instr = 'STORE'
                    addr = i
                    instr_bin = codes[instr][0]
                    instr_bin = (instr_bin << 8) | intbv(addr)[8:]
                    instr_list.append((instr, addr, instr_bin))

                    # ADD 1
                    instr = 'ADD'
                    op = 1
                    instr_bin = ((codes[instr][0] | flg) << 8) | intbv(op)[8:]
                    instr_list.append((instr, op, instr_bin))
                    #flg = 0

                for i in range(10):
                    instr = 'LOAD'  
                    addr = i
                    instr_bin = (codes[instr][0] << 8) | intbv(addr)[8:]
                    instr_list.append((instr, addr, instr_bin))

                for i in range(len(instr_list)):
                    bin_list.append(instr_list[i][2])

                print(len(bin_list))

                return instr_list, bin_list


            instr_list, bin_list = create_instr()

            # Initialise signals and dut's
            clock, reset, pipe_dec, pipe_imme, \
                pipe_dm_addr, pipe_pc, back_acc, back_dm_data = self.signals
            
            fedec_inst = fedec.pyleros_fedec(clock, reset, back_acc, back_dm_data, self.fwd_accu, \
                                        self.pipe_alu_op, pipe_dec, pipe_imme, pipe_dm_addr, pipe_pc, filename=bin_list, debug=True)
            exec_inst = execute.pyleros_exec(clock, reset, self.pipe_alu_op, pipe_dec, pipe_imme, pipe_dm_addr, pipe_pc, \
                                            back_acc, back_dm_data, self.fwd_accu, True)


            @always(delay(10))
            def tbclk():
                clock.next = not clock

            # the alu is run once on intialization anyway, and the value
            # is set to zero(0 + 0)
            @instance
            def tbstim():
                # local accumulator var
                acc = 0
                # yield delay(11) # or yield clock.posedge, same result.
                yield clock.posedge
                yield delay(1)

                addr = 0
                for addr in range(1, 20):

                    instr = instr_list[addr][0]
                    op = instr_list[addr][1]
                    instr_bin = instr_list[addr][2]
                    # print("Bf", addr, back_acc)
                    yield clock.posedge

                    yield delay(1)
                    # print("Af", addr,  back_acc)
                    # print("This is iteration " + str(addr))
                    if instr == 'ADD':
                        acc += op
                        assert (acc & 0xffff) == back_acc
                    elif instr == 'STORE':
                        acc == back_acc

                yield clock.posedge
                yield delay(1)
                for addr in range(10):
                    mod_addr = addr + 20
                    instr = instr_list[mod_addr][0]
                    op = instr_list[mod_addr][1]
                    instr_bin = instr_list[mod_addr][2]

                    yield clock.posedge
                    yield delay(1)

                    if instr == 'LOAD':
                        assert addr == back_acc

                raise StopSimulation

            return instances()

        inst = tb_ls()
        inst.run_sim()


    def test_branch(self):

        @block
        def tb_branch( args=None):
            """Test branches.

            """

            def create_instr(imm=False):
                """Create a list of random instructions
                from the list given.

                """
                instr_list, bin_list = [], []
                op = 0
                flg = 1

                # list of instructions, that finally yield the value
                # 37
                i_list = [
                ('NOP', 0, False),
                ('ADD', 10, True),
                ('SUB', 5, True),
                ('XOR', 13, True),
                ('STORE', 50, False),
                ('ADD', 15, True),
                ('STORE', 51, False),
                ('XOR', 48, True),
                ('LOAD', 27, True),
                ('JAL', 1, False),
                ]
                
                for i in range(10, 27):
                    i_list.append(('NOP', 0, False))
                i_list.append(('LOAD', 51, False))
                i_list.append(('LOADX', 27, False))
                i_list.append(('XOR', 45, True))

                for i in i_list:
                    instr, val, imme = i
                    instr_bin = ((codes[instr][0] | imme) << 8) | intbv(val)[8:]
                    instr_list.append((instr, val, instr_bin))

                for i in range(len(instr_list)):
                    bin_list.append(instr_list[i][2])

                return instr_list, bin_list

            instr_list, bin_list = create_instr()

            # Initialise signals and dut's
            clock, reset, pipe_dec, pipe_imme, \
                pipe_dm_addr, pipe_pc, back_acc, back_dm_data = self.signals

            fedec_inst = fedec.pyleros_fedec(clock, reset, back_acc, back_dm_data, self.fwd_accu, \
                                        self.pipe_alu_op, pipe_dec, pipe_imme, pipe_dm_addr, pipe_pc, filename=bin_list, debug=True)
            exec_inst = execute.pyleros_exec(clock, reset, self.pipe_alu_op, pipe_dec, pipe_imme, pipe_dm_addr, pipe_pc, \
                                            back_acc, back_dm_data, self.fwd_accu, True)

            @always(delay(10))
            def tbclk():
                clock.next = not clock

            # the alu is run once on intialization anyway, and the value
            # is set to zero(0 + 0)
            @instance
            def tbstim():
                # local accumulator var
                acc = 0
                # yield delay(11) # or yield clock.posedge, same result.
                yield clock.posedge
                yield delay(1)
                addr = 0
                for addr in range(15):

                    yield clock.posedge

                assert back_acc == 37

                raise StopSimulation

            return instances()

        inst = tb_branch()
        inst.run_sim()