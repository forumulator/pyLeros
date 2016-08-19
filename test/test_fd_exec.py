from pyleros import fedec, execute
from pyleros.codes import dlist, codes
from pyleros.types import alu_op_type, dec_op_type, IM_BITS, DM_BITS, decSignal, inpSignal
from pyleros.sim import sim

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


        pipe_dec = decSignal()

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

        self.ioin = inpSignal()
    

    @block
    def init_func(self, bin_list):
        clock, reset, pipe_dec, pipe_imme, \
            pipe_dm_addr, pipe_pc, back_acc, back_dm_data = self.signals

        self.fedec_inst = fedec.pyleros_fedec(clock, reset, back_acc, back_dm_data, self.fwd_accu, \
                                    self.pipe_alu_op, pipe_dec, pipe_imme, pipe_dm_addr, pipe_pc, filename=bin_list, debug=True)
        self.exec_inst = execute.pyleros_exec(clock, reset, self.pipe_alu_op, pipe_dec, pipe_imme, pipe_dm_addr, pipe_pc, \
                                        back_acc, back_dm_data, self.fwd_accu, self.ioin, True)
        self.simu_inst = sim.simulator(bin_list) 
        return self.fedec_inst, self.exec_inst



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
                instr_list[0] = ('NOP', 0, 0x0000)

                for i in range(len(instr_list)):
                    bin_list.append(instr_list[i][2])

                return instr_list, bin_list

            tup = tuple(['ADD', 'SUB', 'OR', 'AND', 'XOR', 'SHR', 'LOAD'])
            instr_list, bin_list = create_instr(tup)

            # Initialise signals and dut's
            clock, reset, pipe_dec, pipe_imme, \
                pipe_dm_addr, pipe_pc, back_acc, back_dm_data = self.signals

            self.init_func(bin_list)
            fedec_inst, exec_inst, simu_inst =  self.fedec_inst, self.exec_inst, self.simu_inst


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
                yield clock.posedge
                
                for addr in range(1, len(instr_list) - 1):

                    instr = instr_list[addr][0]
                    op = instr_list[addr][1]
                    instr_bin = instr_list[addr][2]

                    state = simu_inst.__next__()
                    yield delay(7)
                    assert state[0] == back_acc
                    yield clock.posedge


                    
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

                
                return instr_list, bin_list


            instr_list, bin_list = create_instr()

            # Initialise signals and dut's
            clock, reset, pipe_dec, pipe_imme, \
                pipe_dm_addr, pipe_pc, back_acc, back_dm_data = self.signals

            self.init_func(bin_list)
            fedec_inst, exec_inst, simu_inst =  self.fedec_inst, self.exec_inst, self.simu_inst


            @always(delay(10))
            def tbclk():
                clock.next = not clock

            # the alu is run once on intialization anyway, and the value
            # is set to zero(0 + 0)
            @instance
            def tbstim():
                # local accumulator var
                acc = 0
                addr = 0

                yield clock.posedge
                yield clock.posedge
                yield delay(3)
                for addr in range(1, 20):
                    state = simu_inst.__next__()
                    instr = instr_list[addr][0]
                    op = instr_list[addr][1]
                    instr_bin = instr_list[addr][2]
                    yield clock.posedge
                    assert state[0] == back_acc
                    # print("Af", addr,  back_acc)
                    # print("This is iteration " + str(addr))
                    if instr == 'ADD':
                        acc += op
                        assert (acc & 0xffff) == back_acc
                    elif instr == 'STORE':
                        acc == back_acc

                for addr in range(10):
                    mod_addr = addr + 20
                    instr = instr_list[mod_addr][0]
                    op = instr_list[mod_addr][1]
                    instr_bin = instr_list[mod_addr][2]

                    state = simu_inst.__next__()
                    yield delay(4)
                    assert state[0] == back_acc
                    if instr == 'LOAD':
                        assert addr == back_acc
                    yield clock.posedge

                    

                yield delay(10)
                assert state[0] == back_acc

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
                ('NOP', 0, False), # acc 0
                ('ADD', 10, True),  # acc 10
                ('SUB', 5, True),   # acc 5
                ('XOR', 13, True),  # acc 8
                ('STORE', 50, False), # dm[50] = 8
                ('ADD', 15, True),  # acc 23
                ('STORE', 51, False),  # dm[51] = 23 
                ('XOR', 48, True), # acc = 39
                ('LOAD', 27, True),  # back_dm_rd_data
                ('JAL', 1, False)   # 
                ]
                
                for i in range(10, 27):
                    i_list.append(('NOP', 0, False))
                i_list.append(('LOADADDR', 51, False))
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

            self.init_func(bin_list)
            fedec_inst, exec_inst, simu_inst =  self.fedec_inst, self.exec_inst, self.simu_inst           

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
                yield clock.posedge
                addr = 0
                for addr in range(12):
                    # simu_inst.__next__()
                    state = simu_inst.__next__()
                    yield clock.posedge
                    # if not addr == 6:
                    # else:
                    #     yield clock.posedge
                        # yield delay(1)
                        # pass
                    assert state[0] == back_acc
                    

                assert back_acc == 37

                raise StopSimulation

            return instances()

        inst = tb_branch()
        inst.run_sim()


    @pytest.mark.xfail
    def test_random(self):

        @block
        def tb_rand( args=None):
            """Test branches.

            """

            def create_instr():
                """Create a list of random instructions
                
                """
                instr_list = [0 for i in range(256)]
                bin_list = [0 for i in range(256)]
                op = 0
                ibit = 1

                tup = tuple(['NOP', 'ADD', 'SUB', 'OR', 'AND', 'XOR', 'SHR', 'LOAD', 'STORE', 'LOADX', 'STOREX', 'BRANCH', 'BRZ', 'BRNZ', 'BRP', 'BRN', 'JAL'])
                num = len(tup)

                instr_list[0] = ('NOP', 0, 0x0000)
                bin_list[0] = 0x0000
                instr_list[1] = ('ADD', 10, 0x0910)
                bin_list[1] = 0x0910
                addr = 1
                isim = sim.simulator(bin_list) 
                for i in range(1, 250):
                    def set_list(tup, addr):
                        instr_list[addr] = tup
                        bin_list[addr] = tup[2]
                    
                    cst = isim.__next__()
                        
                    if cst[1] > 255:
                        instr_list[addr] = ('NOP', 0, 0x0000)
                        bin_list[addr] = 0x0000
                        addr -= 1
                        break

                    addr += 1
                    ind = randrange(num)
                    instr = tup[ind]
                    if instr == 'JAL':
                        ti = 'LOAD'
                        op = randrange(256)
                        instr_bin = ((codes[ti][0] | True) << 8) | op
                        tup1 = (ti, op, instr_bin)
                        set_list(tup1, addr)
                        cst = isim.__next__()
                        op = 0x01
                    elif instr == 'LOADX' or instr == 'STOREX':
                        ti = 'LOAD'
                        op = randrange(128)
                        instr_bin = ((codes[ti][0] | True) << 8) | op
                        tup1 = (ti, op, instr_bin)
                        set_list(tup1, addr)
                        cst = isim.__next__()
                        op = randrange(128)
                    else:
                        if ind < 9:
                            op = randrange(2**8)
                        else:
                            op = randrange(10)

                    if codes[instr][2]:
                        ibit = randrange(2)
                    else:
                        ibit = 0

                    instr_bin = ((codes[instr][0] | ibit) << 8) | op
                    instr_list[addr] = (instr, op, instr_bin)
                    bin_list[addr]= instr_bin
                
                return instr_list, bin_list, addr

            instr_list, bin_list, size = create_instr()

            # Initialise signals and dut's
            clock, reset, pipe_dec, pipe_imme, \
                pipe_dm_addr, pipe_pc, back_acc, back_dm_data = self.signals

            self.init_func(bin_list)
            fedec_inst, exec_inst, simu_inst =  self.fedec_inst, self.exec_inst, self.simu_inst           

            @always(delay(10))
            def tbclk():
                clock.next = not clock

            # the alu is run once on intialization anyway, and the value
            # is set to zero(0 + 0)
            @instance
            def tbstim():
                # local accumulator var
                acc = 0
                yield clock.posedge
                yield clock.posedge
                addr = 0
                for addr in range(int(size / 2)):

                    instr = instr_list[addr + 1][0]
                    op = instr_list[addr + 1][1]
                    print(instr, op, back_acc, "PRE EXECUTION--------------------------------------------------------------")
                    # simu_inst.__next__()
                    state = simu_inst.__next__()
                    yield clock.posedge
                    print(instr, op, back_acc, "--------------------------------------------------------------")
                    assert state[0] == back_acc

                # assert 0

                raise StopSimulation

            return instances()

        inst = tb_rand()
        inst.run_sim()

