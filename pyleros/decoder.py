from myhdl import instances, block, enum, always_comb
from pyleros.types import alu_op_type, t_decSignal


@block
def pyleros_decoder(instr_hi, out_sig, verbose=False):
    """The decoder module for pyleros, decodes the high bits
    of the instruction and generates the control signals. The modules is
    purely combinatorial. 

    Arguments (ports):
        instr_hi: IN The high 8 bits of the instruction
        op: Indicates the type of ALU operation
        al_ena:  Enables the high bits of the accumulator
            (Required when the value of the Acc changes)
        ah_ena: Enables the low bits of the accumulator
            (Required when the value of the Acc changes)
        log_add: For ADD/SUB
        add_sub: Switches between addition and subtration
        shr: Signal shift right operation
        sel_imm: Signal, enabled if o bit(indicating immediate value)
            is high
        store: Signal the store operation
        outp: output in I/O
        inp: input in I/O
        br_op: Signal if the instructio is a branch
        jal: Signal if the instructio is a jump and link
        loadh: Signal if the instructio is a load high
        indls: Signal if the instructio is a indirect load/store

    Parameters:
        None

    """
    
    @always_comb
    def decoder():

        if verbose:
            print("Inside decoder with instruction_hi:", instr_hi)
        # Set the defaults of all signals
        out_sig[int(t_decSignal.op)].next = alu_op_type.NOP
        out_sig[int(t_decSignal.al_ena)].next = False
        out_sig[int(t_decSignal.ah_ena)].next = False
        out_sig[int(t_decSignal.log_add)].next = False
        out_sig[int(t_decSignal.add_sub)].next = False
        out_sig[int(t_decSignal.shr)].next = False
        out_sig[int(t_decSignal.sel_imm)].next = False
        out_sig[int(t_decSignal.store)].next = False
        out_sig[int(t_decSignal.outp)].next = False
        out_sig[int(t_decSignal.inp)].next = False
        out_sig[int(t_decSignal.br_op)].next = False
        out_sig[int(t_decSignal.jal)].next = False
        out_sig[int(t_decSignal.loadh)].next = False
        out_sig[int(t_decSignal.indls)].next = False


        # Decode
        ins_ckh = instr_hi & 0xf8

        # if the instructions are not branch
        if not (ins_ckh == 0x48):
            # the imm. bit, 0
            out_sig[int(t_decSignal.sel_imm)].next = instr_hi[0]

        

        if ins_ckh == 0x00:
            # NOP
            pass

        elif ins_ckh == 0x08:
            # ADD/SUB
            out_sig[int(t_decSignal.al_ena)].next = True
            out_sig[int(t_decSignal.ah_ena)].next = True
            out_sig[int(t_decSignal.log_add)].next = True
            out_sig[int(t_decSignal.add_sub)].next = instr_hi[2]

        elif ins_ckh == 0x10:           
            # SHR
            out_sig[int(t_decSignal.al_ena)].next = True
            out_sig[int(t_decSignal.ah_ena)].next = True
            out_sig[int(t_decSignal.shr)].next = True

        elif ins_ckh == 0x18:
            # reserved
            pass

        elif ins_ckh == 0x20:
            # ALU_OP : ld, or, and, xor
            out_sig[int(t_decSignal.al_ena)].next = True
            out_sig[int(t_decSignal.ah_ena)].next = True

        elif ins_ckh == 0x28:
            # LOADH
            out_sig[int(t_decSignal.loadh)].next = True
            out_sig[int(t_decSignal.ah_ena)].next = True

        elif ins_ckh == 0x30:
            # STORE
            out_sig[int(t_decSignal.store)].next = True

        elif ins_ckh == 0x38:
            # I/O
            if instr_hi[2] == False:
                # OUT
                out_sig[int(t_decSignal.outp)].next = True
            else:
                # IN
                out_sig[int(t_decSignal.inp)].next = True
                out_sig[int(t_decSignal.al_ena)].next = True
                out_sig[int(t_decSignal.ah_ena)].next = True

        elif ins_ckh == 0x40:
            # JAL
            out_sig[int(t_decSignal.jal)].next = True
            out_sig[int(t_decSignal.store)].next = True

        elif ins_ckh == 0x48:
            # BRANCH
            out_sig[int(t_decSignal.br_op)].next = True

        elif ins_ckh == 0x50:
            # LOADADDR, to be implemented
            pass

        elif ins_ckh == 0x60:
            # LOAD INDIRECT
            out_sig[int(t_decSignal.al_ena)].next = True
            out_sig[int(t_decSignal.ah_ena)].next = True
            out_sig[int(t_decSignal.indls)].next = True

        elif ins_ckh == 0x61:
            # STORE INDIRECT
            out_sig[int(t_decSignal.indls)].next = True
            out_sig[int(t_decSignal.store)].next = True



        if ins_ckh == 0x20 or ins_ckh == 0x28:
            # Setting of the signal op as the 
            # alu_op_type
            if instr_hi[3:1] == 0b00:
                # LOAD
                out_sig[int(t_decSignal.op)].next = alu_op_type.LD

            elif instr_hi[3:1] == 0b01:
                # AND
                out_sig[int(t_decSignal.op)].next = alu_op_type.AND

            elif instr_hi[3:1] == 0b10:
                # or
                out_sig[int(t_decSignal.op)].next = alu_op_type.OR

            elif instr_hi[3:1] == 0b11:
                # XOR
                out_sig[int(t_decSignal.op)].next = alu_op_type.XOR

    return instances()


