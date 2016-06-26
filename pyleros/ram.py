from myhdl import block, intbv, instances, always_seq
from pyleros.types import DM_BITS


@block
def pyleros_dm(clk, reset, rd_addr, wr_addr, wr_data, wr_en, rd_data):
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
        None 

    """
    DM_SIZE = 2**DM_BITS
    DM = [(intbv(65)[16:]) for _ in range(DM_SIZE)]

    # convert list into tupple for automatic conversion
    # DM_array = tuple(DM)

    @always_seq(clk.posedge, reset=reset)
    def DM_rw():

        rd_data.next = DM[int(rd_addr)]

        if wr_en:
            # Write enabled
            if wr_addr >= DM_SIZE:
                raise ValueError("Write addr " + hex(wr_addr) + "out of bounds")
            else:   
                print("At {addr} : {val}".format(addr=wr_addr, val=wr_data.val))
                DM[int(wr_addr)] = intbv(wr_data.val)[16:]

    return instances()




if __name__ == "__main__":

    pass
