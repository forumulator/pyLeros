from myhdl import block, intbv, instances, always_seq, Signal
from pyleros.types import DM_BITS


@block
def pyleros_dm(clk, reset, rd_addr, wr_addr, wr_data, wr_en, rd_data, debug=False):
    """Definition of the data memory for pyleros. 
    Reading is synchronous with the rising edge of the
    clock. Writing is also done on the clock rising edge if 
    the enable signal wr_en is high. 

    Arguments (ports):
        clk: The clock signal
        reset: The reset signal #Async?
        rd_addr: IN Read address
        wr_addr: IN Write address
        wr_data: IN Write data
        wr_en: IN Write enable
        rd_data: OUT The data at DM address rd_addr
        

    Parameters:
        debug: Debugging mode, the processor prints various error messages
        
    """
    DM_SIZE = 2**DM_BITS
    DM = [Signal(intbv(0)[16:]) for _ in range(DM_SIZE)]

    @always_seq(clk.negedge, reset=reset)
    def read_write():
        # if __debug__:
        #     if debug:

        rd_data.next = DM[int(rd_addr)]

        if wr_en:
            # Write enabled

            if __debug__:
                if wr_addr >= DM_SIZE:
                    raise ValueError("Write addr " + hex(wr_addr) + "out of bounds")  
                
                if debug:
                    print("Writing to DM at " + str(wr_addr) + " " + str(int(wr_data.val)))
            
            DM[int(wr_addr)].next = wr_data
            if (wr_addr == 17):
                for i in range(20):
                    print ("At DM address", i, "data", DM[i])

    return read_write




if __name__ == "__main__":

    pass
