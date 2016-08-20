-- TestBench Template 
  
LIBRARY ieee;
USE ieee.std_logic_1164.all;
USE ieee.std_logic_unsigned.all;
use IEEE.numeric_std.all;

-- use work.pck_myhdl_10.all;
-- entity declaration for your testbench.Dont declare any ports here
ENTITY test_tb IS
END test_tb;

ARCHITECTURE behavior OF test_tb IS
   -- Component Declaration for the Unit Under Test (UUT)
    COMPONENT pyleros
    port (
        clk: in std_logic;
        reset: in std_logic;
        ioout_wr_strobe: out std_logic;
        ioout_rd_strobe: out std_logic;
        ioout_io_addr: out unsigned(15 downto 0);
        ioout_wr_data: out unsigned(15 downto 0);
        pyleros_exec_0_pyleros_alu_0_ioin_rd_data: in unsigned(15 downto 0)
    );
    END COMPONENT;
   --declare inputs and initialize them
   signal clk : std_logic := '0';
   signal reset : std_logic := '0';
	signal ioout_wr_strobe : std_logic := '0';
	signal ioout_rd_strobe : std_logic := '0';
	signal ioout_io_addr: unsigned(15 downto 0) := (others => '0');
	signal ioout_wr_data: unsigned(15 downto 0) := (others => '0');
	signal ioin_rd_data: unsigned(15 downto 0) := (others => '0');
   --declare outputs and initialize them
   signal count : std_logic_vector(3 downto 0);
	signal sig_t : unsigned(15 downto 0) := (others => '0');
	signal sig_t1 : unsigned(7 downto 0) := (others => '0');

   -- Clock period definitions
   constant clk_period : time := 1 us;
BEGIN
    -- Instantiate the Unit Under Test (UUT)
   uut: pyleros PORT MAP ( clk, reset, ioout_wr_strobe, ioout_rd_strobe, ioout_io_addr,  ioout_wr_data, ioin_rd_data);
	

   -- Clock process definitions( clock with 50% duty cycle is generated here.
   clk_process :process
   begin
			for Z in 1 to 800
			loop
				wait for clk_period/2;  --for 0.5 ns signal is '0'.
				clk <= not clk;
				-- wait for clk_period/2;  --for next 0.5 ns signal is '1'.
			end loop;
			wait;
   end process;
	
	
   -- Stimulus process
  stim_proc: process
  type A_TYPE1 is array (0 to 16) of unsigned(15 downto 0);
  type A_TYPE2 is array (0 to 16) of integer;
  variable idx : integer := 0;
  variable num_arr : A_TYPE1 ;
  variable int_arr : A_TYPE2 := (15, 15, 14, 13, 12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1, 120); 
  
  begin 
	 for ind in 0 to 16
	 loop
		num_arr(ind) := to_unsigned(int_arr(ind), 16);
	 end loop;
--	 reset <= '1';
--	 for i in 0 to 1
--	 loop
--	 wait until clk = '1';
--	 end loop;
--	 reset <= '0';
	 L: loop
		wait until clk = '1';
		wait for 0.5 us;
		if ioout_rd_strobe = '1'
		then
			if ioout_io_addr = 0
			then
				ioin_rd_data <= num_arr(idx);
				idx := idx + 1;
			end if;
		elsif ioout_wr_strobe = '1'
		then
			if ioout_io_addr = 1
			then
				wait for 0.5 us;
				assert ioout_wr_data = 121
					report "Simulation Ended"
					severity failure;
				
				
			end if;
		end if;
	
	 end loop;
  end process;

END;
