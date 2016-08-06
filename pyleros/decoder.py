from myhdl import instances, block, enum, always_comb
from pyleros.types import alu_op_type, dec_op_type


@block
def pyleros_decoder(instr_hi, alu_op, out_sig, debug=False):
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
        debug: Debugging mode, the processor prints various error messages
        
    """
    
    @always_comb
    def decoder():

        if __debug__:
            if debug:
                print("Inside decoder with instruction_hi:", instr_hi)

        # Set the defaults of all signals
        alu_op.next = alu_op_type.NOP
        out_sig.al_ena.next = False
        out_sig.ah_ena.next = False
        out_sig.log_add.next = False
        out_sig.add_sub.next = False
        out_sig.shr.next = False
        out_sig.sel_imm.next = False
        out_sig.store.next = False
        out_sig.outp.next = False
        out_sig.inp.next = False
        out_sig.br_op.next = False
        out_sig.jal.next = False
        out_sig.loadh.next = False
        out_sig.indls.next = False


        # Decode
        ins_ckh = instr_hi & 0xf8

        # if the instructions are not branch
        if not (ins_ckh == 0x48):
            # the imm. bit, 0
            out_sig.sel_imm.next = instr_hi[0]

        

        if ins_ckh == 0x00:
            # NOP
            pass

        elif ins_ckh == 0x08:
            # ADD/SUB
            out_sig.al_ena.next = True
            out_sig.ah_ena.next = True
            out_sig.log_add.next = True
            out_sig.add_sub.next = instr_hi[2]

        elif ins_ckh == 0x10:           
            # SHR
            out_sig.al_ena.next = True
            out_sig.ah_ena.next = True
            out_sig.shr.next = True

        elif ins_ckh == 0x18:
            # reserved
            pass

        elif ins_ckh == 0x20:
            # ALU_OP : ld, or, and, xor
            out_sig.al_ena.next = True
            out_sig.ah_ena.next = True

        elif ins_ckh == 0x28:
            # LOADH
            out_sig.loadh.next = True
            out_sig.ah_ena.next = True

        elif ins_ckh == 0x30:
            # STORE
            out_sig.store.next = True

        elif ins_ckh == 0x38:
            # I/O
            if instr_hi[2] == False:
                # OUT
                out_sig.outp.next = True
            else:
                # IN
                out_sig.inp.next = True
                out_sig.al_ena.next = True
                out_sig.ah_ena.next = True

        elif ins_ckh == 0x40:
            # JAL
            out_sig.jal.next = True
            out_sig.store.next = True

        elif ins_ckh == 0x48:
            # BRANCH
            out_sig.br_op.next = True

        elif ins_ckh == 0x50:
            # LOADADDR, to be implemented
            pass

        elif ins_ckh == 0x60:
            # LOAD INDIRECT
            out_sig.al_ena.next = True
            out_sig.ah_ena.next = True
            out_sig.indls.next = True

        elif ins_ckh == 0x70:
            # STORE INDIRECT
            out_sig.indls.next = True
            out_sig.store.next = True



        if ins_ckh == 0x20 or ins_ckh == 0x28 or ins_ckh == 0x60:
            # Setting of the signal op as the 
            # alu_op_type
            if instr_hi[3:1] == 0b00:
                # LOAD
                alu_op.next = alu_op_type.LD
            elif instr_hi[3:1] == 0b01:
                # AND
                alu_op.next = alu_op_type.AND

            elif instr_hi[3:1] == 0b10:
                # or
                alu_op.next = alu_op_type.OR

            elif instr_hi[3:1] == 0b11:
                # XOR
                alu_op.next = alu_op_type.XOR

    return instances()


