
from myhdl import instances, block, intbv, \
                    always_comb, always_seq, Signal

from pyleros.types import alu_op_type, dec_op_type



@block
def pyleros_alu(alu_op, dec, acc, opd, pre_acc, debug=False):
    """The alu module for pyleros, purely combinatorial

    Arguments (ports):
        dec: IN The decoder control signals
        acc: IN The accumulator
        opd: IN Operand, based on whether the instruction is 
            immediate or not
        pre_acc: OUT The result of the ALU operation, from the acc mux

    Parameters:
        None
    """

    res_arith = Signal(intbv(0)[16:])
    res_log = Signal(intbv(0)[16:])

    # Add and Subtract module
    @always_comb
    def op_add_sub():

        if __debug__:
            print("inside alu", acc, opd)
        if dec.add_sub == 0:
            res_arith.next = intbv(acc + opd)[16:]
            if __debug__:
                if debug:
                    print(res_arith.next, acc + opd, acc, opd)
        else:
            res_arith.next = intbv(acc - opd)[16:]

    # for the logical operations
    # @always_comb
    # def op_logical():

        if alu_op == alu_op_type.LD:
            # LOAD
            res_log.next = opd

        elif alu_op == alu_op_type.AND:
            # AND
            res_log.next = acc & opd

        elif alu_op == alu_op_type.OR:
            # OR
            res_log.next = acc | opd

        elif alu_op == alu_op_type.XOR:
            # XOR
            res_log.next = acc ^ opd

    # MUX to select which result goes into the accumulator
    # based on the decoder control signals
    @always_comb
    def acc_mux():
        if dec.log_add == 1:
            # ADD/ SUB
            pre_acc.next = res_arith

        elif dec.shr == 1:
            # SHR
            pre_acc.next = intbv(acc >> 1)[16:]

        elif not (alu_op == alu_op_type.NOP):
            pre_acc.next = res_log


    return instances()