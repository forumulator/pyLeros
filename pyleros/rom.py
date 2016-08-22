from myhdl import block, Signal, intbv, instances, always_seq, always_comb
from pyleros.types import IM_BITS
import sys


@block
def pyleros_im(rd_addr, rd_data, IM_array = None, debug = False):
    """Definition of the instruction memory, or the ROM for
    pyleros. Reading is synchronous with the rising edge of the
    clock. Writing is not enabled.

    Arguments (ports):
        clk: The clock signal
        reset: The reset signal #Async?
        rd_addr: IN Read address
        rd_data: OUT The data at IM address

    Parameters:
        rfile: Name of the file or a list containing the instructions
        debug: Debugging mode, the processor prints various error messages
        
    """
    IM_SIZE = 2**IM_BITS
    
    if not type(IM_array) is tuple:
        # Fill up the memory registers
        IM_array = define_rom(IM_SIZE, IM_array)

    @always_comb
    def read():
        if __debug__:
            if debug:
                print("\nReading instr mem at:", rd_addr)
                print("Instruction", IM_array[int(rd_addr)])
        rd_data.next = IM_array[int(rd_addr)]

    return read




def define_rom(IM_SIZE=1024, rfile = None):

    IM = [0 for _ in range(IM_SIZE)]

    if rfile:
        if type(rfile) is list:
            rfile.extend([0 for i in range(5)])
            return tuple(rfile)

        else:
            with open(rfile, "r") as f:
                addr = 0

                for line in f:
                    line = line.split('//')[0]
                    full = ''
                    for part in line.split():
                        full += part

                    line = full
                    if line:
                        if not (line.isdigit() and (len(line) == 16)):
                            raise Exception

                        else:
                            try:
                                instr = int(line, 2)
                                IM[addr] = instr
                                addr += 1
                            except:
                                raise Exception

                # for i in range(addr, IM_SIZE):

                #     IM[i] = intbv(0x0000)[16:]
                IM.extend([0 for _ in range(5)])
                return tuple(IM)


    else:
        # Put the actual instructions here
        instruction_list = [ \
        "0x0000", 
        "0x0000", 
        "0x0000", 
        "0x0000", 
        "0x0000", 
        "0x0000", 
        "0x0000", 
        "0x0000", 
        "0x0000", 
        "0x0000", 
        "0x0000", 
        "0x0000", 
        "0x0000", 
        "0x0000", 
        "0x0000", 
        ]

        for i in range(len(instruction_list)):
            IM[i] = (intbv(int(instruction_list[i],16))[16:])

        for i in range(len(instruction_list), IM_SIZE):
            IM[i] = (intbv(0x0000)[16:])

        return tuple(IM)


if __name__ == "__main__":

    pass
    # if len(sys.argv) == 1:
    #     rfile = None

    # else:
    #     rfile = sys.argv[1]

    # IM_SIZE = 1024
    # IM = [(intbv(0)[16:]) for _ in range(IM_SIZE)]


    # # Fill up the memory registers
    # define_rom(IM, IM_SIZE, rfile)

    # IM_array = tuple(IM)
    
    # for addr in range(IM_SIZE):
    #     print(str(addr) + " : " + hex(IM[addr]))
