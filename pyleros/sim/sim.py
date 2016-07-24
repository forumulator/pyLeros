import sys
import os

DM_SIZE = 1024
IM_SIZE = 1024

def define_rom(instr_list=None):

    instr_mem = [0 for i in range(IM_SIZE)]
    size = 0
    if type(instr_list) is list:
        
        size = len(instr_list)
        for addr in range(size):
            instr_mem[addr] = instr_list[addr]

    return instr_mem, size


def simulator(instr_list = None, steps = 0):

    # Defining the registers and memory
    acc = 0
    instr_mem, prog_size = define_rom(instr_list)
    # Because the execution of the processor
    # also starts from the fist instruction
    pc = 1
    step = 0
    instr = 0x0000

    data_mem = [0 for i in range(DM_SIZE)]
    rd_data = 0
    back_rd_data = 0

    # The main sim loop
    while True:

        # prog size reached
        if (step == prog_size):
            yield (acc, pc, rd_data, instr, step, val)

        if (step == steps) and steps:
            yield (acc, pc, rd_data, instr, step, val)

        step += 1
        instr = instr_mem[pc]

        val = 0 

        pc_next = pc + 1
        # check the o bit to find if the operation is in the 
        # imm. category
        if ((instr >> 8) & 0x01) != 0:
            # Use the immediate value

            val = instr & 0xff

            # Sign-extend
            if (val & 0x80) != 0:
                val = val | 0xff00
        else:
            val = data_mem[instr & 0xff]
            rd_data = val


        # EXECUTE the instruction
        oper = (instr & 0xfe00)

        if oper == 0x0000:
            # NOP
            pass

        elif oper == 0x0800:
            # ADD
            acc = acc + val

        elif oper == 0x0c00:
            # SUB
            acc = acc - val

        elif oper == 0x1000:
            # This is the logical shift which can be achieved for 16 bits
            # in python by (-5 + 0x10000) >> n or (-5 & 0xffff) >> n
            # SHR (shift right  by 1)
            #acc = (acc >> 1) if (acc > 0) else (acc & 0xffff) >> 1 
            acc = (acc & 0xffff) >> 1
        elif oper == 0x2000:
            # LOAD
            acc = (val & 0xffff)


        elif oper == 0x2200:
            # AND
            acc = acc & val

        elif oper == 0x2400:
            # Or
            acc = acc | val

        elif oper == 0x2600:
            # XOR
            acc = acc ^ val

        elif oper == 0x2800:
            # LOADH (load high)
            # lowest 8 bits of the acc and 
            # high 8 from the imm value
            acc = (acc & 0xff) | (val << 8)

        elif oper == 0x3000:
            # STORE
            # only as direct
            data_mem[instr & 0x00ff] = (acc & 0xffff)

        elif oper == 0x3800:
            # OUT
            pass

        elif oper == 0x3c00:
            # IN 
            pass

        elif oper == 0x4000:
            # JAL
            st_addr = (instr & 0xff)
            data_mem[st_addr] = pc_next
            pc_next = acc

        elif oper == 0x5000:
            # LOADADDR
            pass

        elif oper == 0x6000:
            # loadind
            mp = back_rd_data + (instr & 0xff)
            acc = (data_mem[mp])

        elif oper == 0x7000:
            # STORE INDIRECT 
            data_mem[ar + (instr & 0xff)] = (acc & 0xffff)

        # case 7: // I/O (ld/st indirect)
        # break

        else:

        # BRANCH, use the immediate bit
        # to decode the type of the branch
        # branch, brz, brnz, brp, brn

            brop = instr & 0xff00

            if (brop == 0x4800):

                # BRANCH
                # Assuming 16 - bit instructions
                # with an 8 bit offset for branches
                pc_next = pc + (instr & 0x00ff)

            elif (brop == 0x4900):
                # BRZ
                if (acc_dly == 0):
                    pc_next = pc + (instr & 0x00ff)

            elif (brop == 0x4a00):
                # BRNZ
                if (acc_dly != 0):
                    pc_next = pc + (instr & 0x00ff)

            elif (brop == 0x4b00):
                # BRP (branch on positive)
                if (acc_dly & 0x8000) == 0:
                    pc_next = pc + (instr & 0x00ff)

            elif (brop == 0x4c00):
                # BRN (branch on negative)      
                if (acc_dly & 0x8000) != 0:
                    pc_next = pc + (instr & 0x00ff)

            else:
                raise ValueError("Invalid Instruction at address " + str(pc) + \
                    " : " + str(instr))

        acc = acc & 0xffff 

        pc = pc_next
        back_rd_data = rd_data

        yield (acc, pc, rd_data, instr, step, val)



def main():

    # Check for arguments
    # to be switched to python parser
    narg = len(sys.argv)
    global progSize
    usage = "Usage: python lerosSim [-qio] filename"
    if  (narg < 2):
        print(usage)
        exit(1)


    filename = sys.argv[narg - 1]

    # check for file exist
    if os.path.exists(filename) == False:
        raise FileNotFoundError('Source file does not exist')

    load_stat = instr_load(filename)
    if load_stat == 1:
        raise ValueError('File not in proper format')

    else:
        print("Instruction Memory has " + str(progSize) + " words\n")
        sim_stat = simulate()
        if sim_stat == 0:
            mem_dump(True)

    




if __name__ == '__main__':
    main()