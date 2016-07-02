from myhdl import instances, block, intbv, \
                    always_comb, always_seq

from pyleros.types import alu_op_type, t_decSignal



@block
def pyleros_alu(dec, acc, opd, pre_acc, verbose=False):
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

    res_arith = intbv(0)[16:]
    res_log = intbv(0)[16:]

    # Add and Subtract module
    @always_comb
    def op_add_sub():

        if verbose:
            print("inside alu", acc, opd)
        if not dec[int(t_decSignal.add_sub)]:
            res_arith = (int(acc) + int(opd)) & 0xffff
            if verbose:
                print(res_arith, acc + opd, acc, opd)
        else:
            res_arith = (int(acc) - int(opd)) & 0xffff

    # for the logical operations
    # @always_comb
    # def op_logical():

        if dec[int(t_decSignal.op)] == alu_op_type.LD:
            # LOAD
            res_log = int(opd)

        elif dec[int(t_decSignal.op)] == alu_op_type.AND:
            # AND
            res_log = int(acc & opd)

        elif dec[int(t_decSignal.op)] == alu_op_type.OR:
            # OR
            res_log = int(acc | opd)

        elif dec[int(t_decSignal.op)] == alu_op_type.XOR:
            # XOR
            res_log = int(acc ^ opd)

    # MUX to select which result goes into the accumulator
    # based on the decoder control signals
    # @always_comb
    # def acc_mux():
        if dec[int(t_decSignal.log_add)]:
            # ADD/ SUB
            pre_acc.next = res_arith

        else:
            if dec[int(t_decSignal.shr)]:
                # SHR
                pre_acc.next = intbv(acc >> 1)[16:]

            else:
                # LOGICAL OPERATION
                if not (dec[int(t_decSignal.op)] ==  alu_op_type.NOP):
                    pre_acc.next = intbv(res_log)[16:]


    return instances()