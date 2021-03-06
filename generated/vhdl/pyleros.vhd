-- File: ../generated/vhdl/pyleros.vhd
-- Generated by MyHDL 1.0dev
-- Date: Sat Aug 20 00:23:32 2016


library IEEE;
use IEEE.std_logic_1164.all;
use IEEE.numeric_std.all;
use std.textio.all;

-- use work.pck_myhdl_10.all;

entity pyleros is
    port (
        clk: in std_logic;
        reset: in std_logic;
        ioout_wr_strobe: out std_logic;
        ioout_rd_strobe: out std_logic;
        ioout_io_addr: out unsigned(15 downto 0);
        ioout_wr_data: out unsigned(15 downto 0);
        pyleros_exec_0_pyleros_alu_0_ioin_rd_data: in unsigned(15 downto 0)
    );
end entity pyleros;
-- The main pyleros module. Instantiates both the fedec 
-- and execute modules corresponding to the two pipeline stages, 
-- and connects them with signals
-- 
-- Arguments (ports):
--     clk: IN Clock signal
--     reset: IN Async reset signal
--     ioin: The input signal, contains a rd_data of 16 bits.
--     ioout: Output signal, contains output of 16 bits, i/o addr,
--         and read/write strobes. The output is given in the same cycle
--         as the ioout.out_strobe, and is guaranteed to be valid for 1 cycle.
--         The input strobe is given, and the input is read in the same cycle.
--     
-- Parameters:
--     filename: The file/ list containing instructions
--         to load into instruction memory.

architecture MyHDL of pyleros is


type t_enum_alu_op_type_1 is (
    NOP,
    OP_LD,
    OP_AND,
   OP_OR,
    OP_XOR
);

--signal reset: std_logic := '0';

signal pipe_alu_op: t_enum_alu_op_type_1 := NOP;
signal pipe_dec_outp: std_logic := '0';
signal back_acc: unsigned(15 downto 0) := (others => '0');
signal pipe_pc: unsigned(8 downto 0):= (others => '0');
signal pipe_dm_addr: unsigned(7 downto 0):= (others => '0');
signal pipe_imm_val: unsigned(15 downto 0):= (others => '0');
signal back_dm_data: unsigned(15 downto 0):= (others => '0');
signal pipe_dec_inp: std_logic:= '0';
signal fwd_accu: unsigned(15 downto 0):= (others => '0');
signal pyleros_exec_0_pipe_dec_store: std_logic:= '0';
signal pyleros_exec_0_dm_wr_en: std_logic:= '0';
signal pyleros_exec_0_pipe_dec_al_ena: std_logic:= '0';
signal pyleros_exec_0_pipe_dec_sel_imm: std_logic:= '0';
signal pyleros_exec_0_dm_rd_data: unsigned(15 downto 0):= (others => '0');
signal pyleros_exec_0_opd: unsigned(15 downto 0):= (others => '0');
signal pyleros_exec_0_pipe_dec_jal: std_logic:= '0';
signal pyleros_exec_0_pre_accu: unsigned(15 downto 0):= (others => '0');
signal pyleros_exec_0_pc_dly: unsigned(8 downto 0) := (others => '0');
signal pyleros_exec_0_dm_wr_data: unsigned(15 downto 0) := (others => '0');
signal pyleros_exec_0_pipe_dec_ah_ena: std_logic:= '0';
signal pyleros_exec_0_dm_wr_addr: unsigned(7 downto 0) := (others => '0');
signal pyleros_exec_0_acc: unsigned(15 downto 0) := (others => '0');
signal pyleros_exec_0_dm_rd_addr: unsigned(7 downto 0) := (others => '0');
signal pyleros_exec_0_dm_wr_addr_dly: unsigned(7 downto 0) := (others => '0');
signal pyleros_exec_0_pyleros_alu_0_res_log: unsigned(15 downto 0) := (others => '0');
signal pyleros_exec_0_pyleros_alu_0_dec_add_sub: std_logic := '0';
signal pyleros_exec_0_pyleros_alu_0_dec_shr: std_logic := '0';
signal pyleros_exec_0_pyleros_alu_0_dec_log_add: std_logic := '0';
signal pyleros_exec_0_pyleros_alu_0_res_arith: unsigned(15 downto 0) := (others => '0');
signal pyleros_fedec_0_branch_en: std_logic := '0';
signal pyleros_fedec_0_pc_next: unsigned(8 downto 0) := (others => '0');
signal pyleros_fedec_0_decode_add_sub: std_logic := '0';
signal pyleros_fedec_0_decode_loadh: std_logic := '0';
signal pyleros_fedec_0_alu_op: t_enum_alu_op_type_1 := NOP;
signal pyleros_fedec_0_pc_op: unsigned(8 downto 0) := (others => '0');
signal pyleros_fedec_0_decode_store: std_logic := '0';
signal pyleros_fedec_0_decode_shr: std_logic := '0';
signal pyleros_fedec_0_decode_al_ena: std_logic := '0';
signal pyleros_fedec_0_pipe_dec_br_op: std_logic := '0';
signal pyleros_fedec_0_pipe_dec_indls: std_logic := '0';
signal pyleros_fedec_0_pipe_dec_loadh: std_logic := '0';
signal pyleros_fedec_0_instr: unsigned(15 downto 0) := (others => '0');
signal pyleros_fedec_0_decode_indls: std_logic := '0';
signal pyleros_fedec_0_decode_ah_ena: std_logic := '0';
signal pyleros_fedec_0_decode_inp: std_logic := '0';
signal pyleros_fedec_0_pc: unsigned(8 downto 0) := (others => '0');
signal pyleros_fedec_0_decode_log_add: std_logic := '0';
signal pyleros_fedec_0_decode_sel_imm: std_logic := '0';
signal pyleros_fedec_0_pc_add: unsigned(8 downto 0) := (others => '0');
signal pyleros_fedec_0_decode_jal: std_logic := '0';
signal pyleros_fedec_0_instr_hi: unsigned(7 downto 0) := (others => '0');
signal pyleros_fedec_0_decode_outp: std_logic := '0';
signal pyleros_fedec_0_im_addr: unsigned(8 downto 0) := (others => '0');
signal pyleros_fedec_0_decode_br_op: std_logic := '0';
type t_array_pyleros_exec_0_pyleros_dm_0_DM is array(0 to 256-1) of unsigned(15 downto 0);
signal pyleros_exec_0_pyleros_dm_0_DM: t_array_pyleros_exec_0_pyleros_dm_0_DM := (others =>(others => '0'));

begin


PYLEROS_PYLEROS_EXEC_0_SEQ_SET_SIG: process (clk, reset) is
begin
    if (reset = '1') then
        pyleros_exec_0_acc <= to_unsigned(0000, 16);
        pyleros_exec_0_dm_wr_addr_dly <= to_unsigned(00, 8);
    elsif rising_edge(clk) then
        if (pyleros_exec_0_pipe_dec_ah_ena = '1') then
            pyleros_exec_0_acc(16-1 downto 8) <= pyleros_exec_0_pre_accu(16-1 downto 8);
        end if;
        if (pyleros_exec_0_pipe_dec_al_ena = '1') then
            pyleros_exec_0_acc(8-1 downto 0) <= pyleros_exec_0_pre_accu(8-1 downto 0);
            
        end if;
        pyleros_exec_0_dm_wr_addr_dly <= pipe_dm_addr;
    end if;
end process PYLEROS_PYLEROS_EXEC_0_SEQ_SET_SIG;


PYLEROS_PYLEROS_EXEC_0_FWD_ACC_SET: process (pyleros_exec_0_pipe_dec_al_ena, pyleros_exec_0_pre_accu, pyleros_exec_0_pipe_dec_ah_ena, pyleros_exec_0_acc) is
begin
    if (pyleros_exec_0_pipe_dec_ah_ena = '1') then
        back_acc(16-1 downto 8) <= pyleros_exec_0_pre_accu(16-1 downto 8);
--        fwd_accu(16-1 downto 8) <= pyleros_exec_0_pre_accu(16-1 downto 8);
	 else 
		  back_acc(16-1 downto 8) <= pyleros_exec_0_acc(15 downto 8);
    end if;
    if (pyleros_exec_0_pipe_dec_al_ena = '1') then
        back_acc(8-1 downto 0) <= pyleros_exec_0_pre_accu(8-1 downto 0);
--        fwd_accu(8-1 downto 0) <= pyleros_exec_0_pre_accu(8-1 downto 0);
	 else
		  back_acc(7 downto 0) <= pyleros_exec_0_acc(7 downto 0);
    end if;
end process PYLEROS_PYLEROS_EXEC_0_FWD_ACC_SET;


PYLEROS_PYLEROS_EXEC_0_MUX_WRITE_DM: process (pipe_pc, pyleros_exec_0_pipe_dec_store, pyleros_exec_0_acc, pyleros_exec_0_dm_wr_addr_dly, pyleros_exec_0_pipe_dec_jal) is
begin
    if (pyleros_exec_0_pipe_dec_store = '1') then
        pyleros_exec_0_dm_wr_en <= '1';
    else
        pyleros_exec_0_dm_wr_en <= '0';
    end if;
    pyleros_exec_0_dm_wr_addr <= pyleros_exec_0_dm_wr_addr_dly;
    if (pyleros_exec_0_pipe_dec_jal = '1') then
        pyleros_exec_0_dm_wr_data <= resize(pipe_pc, 16);
    else
        pyleros_exec_0_dm_wr_data <= pyleros_exec_0_acc;
    end if;
end process PYLEROS_PYLEROS_EXEC_0_MUX_WRITE_DM;


PYLEROS_PYLEROS_EXEC_0_PYLEROS_ALU_0_OP_ADD_SUB: process (pyleros_exec_0_pyleros_alu_0_dec_add_sub, pyleros_exec_0_acc, pyleros_exec_0_opd, pipe_alu_op) is
variable tmp_var : signed (16 downto 0) := (others => '0');
begin
    
    if (pyleros_exec_0_pyleros_alu_0_dec_add_sub = '0') then
		  tmp_var := resize(signed(pyleros_exec_0_acc + pyleros_exec_0_opd), 17);
        pyleros_exec_0_pyleros_alu_0_res_arith <=  unsigned(tmp_var(16-1 downto 0));
        
    else
			tmp_var := signed(resize(pyleros_exec_0_acc, 17)) - signed(resize(pyleros_exec_0_opd, 17));
        pyleros_exec_0_pyleros_alu_0_res_arith <= unsigned(tmp_var(16-1 downto 0));
    end if;
    if (pipe_alu_op = OP_LD) then
        pyleros_exec_0_pyleros_alu_0_res_log <= pyleros_exec_0_opd;
    elsif (pipe_alu_op = OP_AND) then
        pyleros_exec_0_pyleros_alu_0_res_log <= (pyleros_exec_0_acc and pyleros_exec_0_opd);
    elsif (pipe_alu_op =OP_OR) then
        pyleros_exec_0_pyleros_alu_0_res_log <= (pyleros_exec_0_acc or pyleros_exec_0_opd);
    elsif (pipe_alu_op = OP_XOR) then
        pyleros_exec_0_pyleros_alu_0_res_log <= (pyleros_exec_0_acc xor pyleros_exec_0_opd);
	 else 
			pyleros_exec_0_pyleros_alu_0_res_log <= (others => '0');
		  end if;
end process PYLEROS_PYLEROS_EXEC_0_PYLEROS_ALU_0_OP_ADD_SUB;


PYLEROS_PYLEROS_EXEC_0_PYLEROS_ALU_0_ACC_MUX: process (pipe_alu_op, pyleros_exec_0_pyleros_alu_0_ioin_rd_data, pyleros_exec_0_pyleros_alu_0_res_arith, pyleros_exec_0_pyleros_alu_0_res_log, pyleros_exec_0_pyleros_alu_0_dec_shr, pipe_dec_inp, pyleros_exec_0_pyleros_alu_0_dec_log_add, pyleros_exec_0_acc) is
begin

    if (pyleros_exec_0_pyleros_alu_0_dec_log_add = '1') then
        pyleros_exec_0_pre_accu <= pyleros_exec_0_pyleros_alu_0_res_arith;
    elsif (pyleros_exec_0_pyleros_alu_0_dec_shr = '1') then
        pyleros_exec_0_pre_accu <= shift_right(pyleros_exec_0_acc, 1)(16-1 downto 0);
    elsif (pipe_dec_inp = '1') then
        pyleros_exec_0_pre_accu <= pyleros_exec_0_pyleros_alu_0_ioin_rd_data;
    elsif (not (pipe_alu_op = NOP)) then
        pyleros_exec_0_pre_accu <= pyleros_exec_0_pyleros_alu_0_res_log;
	 else
		  pyleros_exec_0_pre_accu <= pyleros_exec_0_acc;
    end if;
end process PYLEROS_PYLEROS_EXEC_0_PYLEROS_ALU_0_ACC_MUX;


PYLEROS_PYLEROS_EXEC_0_PYLEROS_DM_0_READ_WRITE: process (clk, reset) is
begin
    if (reset = '1') then
        pyleros_exec_0_pyleros_dm_0_DM <= (others =>(others => '0'));
        pyleros_exec_0_dm_rd_data <= to_unsigned(0000, 16);
    elsif rising_edge(clk) then
        pyleros_exec_0_dm_rd_data <= pyleros_exec_0_pyleros_dm_0_DM(to_integer(pyleros_exec_0_dm_rd_addr));
        if (pyleros_exec_0_dm_wr_en = '1') then
            
            pyleros_exec_0_pyleros_dm_0_DM(to_integer(pyleros_exec_0_dm_wr_addr)) <= pyleros_exec_0_dm_wr_data;
        end if;
    end if;
end process PYLEROS_PYLEROS_EXEC_0_PYLEROS_DM_0_READ_WRITE;


PYLEROS_PYLEROS_EXEC_0_OPD_MUX: process (pyleros_exec_0_dm_rd_data, pyleros_exec_0_pipe_dec_sel_imm, pipe_imm_val) is
begin
    if (pyleros_exec_0_pipe_dec_sel_imm = '1') then
        pyleros_exec_0_opd <= pipe_imm_val;
    else
        pyleros_exec_0_opd <= pyleros_exec_0_dm_rd_data;
    end if;
end process PYLEROS_PYLEROS_EXEC_0_OPD_MUX;



pyleros_exec_0_pc_dly <= pipe_pc;



back_dm_data <= pyleros_exec_0_dm_rd_data;
pyleros_exec_0_dm_rd_addr <= pipe_dm_addr;


process (pipe_dec_inp, pipe_dec_outp, back_acc, pyleros_exec_0_acc, back_acc, pipe_imm_val) is
begin
	ioout_rd_strobe <= pipe_dec_inp;
	ioout_wr_strobe <= pipe_dec_outp;
	if pipe_dec_outp = '1' then
		ioout_wr_data <= back_acc;
	else
		ioout_wr_data <= pyleros_exec_0_acc;
	end if;
	ioout_io_addr <= pipe_imm_val;
end process;


PYLEROS_PYLEROS_FEDEC_0_PYLEROS_IM_0_READ: process (pyleros_fedec_0_im_addr) is
begin
    
    case to_integer(pyleros_fedec_0_im_addr) is
--        when 0 => pyleros_fedec_0_instr <= "0000000000000000";
--        when 1 => pyleros_fedec_0_instr <= "0000000000000000";
--        when 2 => pyleros_fedec_0_instr <= "0011110000000000";
--        when 3 => pyleros_fedec_0_instr <= "0011000000000010";
--        when 4 => pyleros_fedec_0_instr <= "0010000100000001";
--        when 5 => pyleros_fedec_0_instr <= "0011000000000011";
--        when 6 => pyleros_fedec_0_instr <= "0010000100001100";
--        when 7 => pyleros_fedec_0_instr <= "0100000000000001";
--        when 8 => pyleros_fedec_0_instr <= "0100100000001111";
--        when 9 => pyleros_fedec_0_instr <= "0000000000000000";
--        when 10 => pyleros_fedec_0_instr <= "0010000011111111";
--        when 11 => pyleros_fedec_0_instr <= "0011100000000001";
--        when 12 => pyleros_fedec_0_instr <= "0011110000000000";
--        when 13 => pyleros_fedec_0_instr <= "0101000000000011";
--        when 14 => pyleros_fedec_0_instr <= "0111000000000100";
--        when 15 => pyleros_fedec_0_instr <= "0010000000000011";
--        when 16 => pyleros_fedec_0_instr <= "0000100100000001";
--        when 17 => pyleros_fedec_0_instr <= "0011000000000011";
--        when 18 => pyleros_fedec_0_instr <= "0000110000000010";
--        when 19 => pyleros_fedec_0_instr <= "0100110011111001";
--        when 20 => pyleros_fedec_0_instr <= "0100100111111000";
--        when 21 => pyleros_fedec_0_instr <= "0010000000000001";
--        when 22 => pyleros_fedec_0_instr <= "0100000000000001";
--        when 23 => pyleros_fedec_0_instr <= "0010000100000000";
--        when 24 => pyleros_fedec_0_instr <= "0011000011111111";
--        when 25 => pyleros_fedec_0_instr <= "0010000000000010";
--        when 26 => pyleros_fedec_0_instr <= "0011000000011001";
--        when 27 => pyleros_fedec_0_instr <= "0000000000000000";
--        when 28 => pyleros_fedec_0_instr <= "0101000000011001";
--        when 29 => pyleros_fedec_0_instr <= "0110000000000100";
--        when 30 => pyleros_fedec_0_instr <= "0000100011111111";
--        when 31 => pyleros_fedec_0_instr <= "0011000011111111";
--        when 32 => pyleros_fedec_0_instr <= "0010000000011001";
--        when 33 => pyleros_fedec_0_instr <= "0000110100000001";
--        when 34 => pyleros_fedec_0_instr <= "0011000000011001";
--        when 35 => pyleros_fedec_0_instr <= "0100101011111001";
--        when 36 => pyleros_fedec_0_instr <= "0100100011100110";
--        when 37 => pyleros_fedec_0_instr <= "0000000000000000";
--        when others => pyleros_fedec_0_instr <= "0000000000000000";
			   when 0 => pyleros_fedec_0_instr <= "0000000000000000";
				when 1 => pyleros_fedec_0_instr <= "0000000000000000";
				when 2 => pyleros_fedec_0_instr <= "0010000100000000";
				when 3 => pyleros_fedec_0_instr <= "0011000000100001";
				when 4 => pyleros_fedec_0_instr <= "0010000100001111";
				when 5 => pyleros_fedec_0_instr <= "0011000000000010";
				when 6 => pyleros_fedec_0_instr <= "0010000100000001";
				when 7 => pyleros_fedec_0_instr <= "0011000000000011";
				when 8 => pyleros_fedec_0_instr <= "0010000100010001";
				when 9 => pyleros_fedec_0_instr <= "0100000000000001";
				when 10 => pyleros_fedec_0_instr <= "0100100000010100";
				when 11 => pyleros_fedec_0_instr <= "0000000000000000";
				when 12 => pyleros_fedec_0_instr <= "0010000011111111";
				when 13 => pyleros_fedec_0_instr <= "0011100000000001";
				when 14 => pyleros_fedec_0_instr <= "0000000000000000";
				when 15 => pyleros_fedec_0_instr <= "0000000000000000";
				when 16 => pyleros_fedec_0_instr <= "0100100011111110";
				when 17 => pyleros_fedec_0_instr <= "0010000000100001";
				when 18 => pyleros_fedec_0_instr <= "0000100100000001";
				when 19 => pyleros_fedec_0_instr <= "0011000000100001";
				when 20 => pyleros_fedec_0_instr <= "0101000000000011";
				when 21 => pyleros_fedec_0_instr <= "0111000000000100";
				when 22 => pyleros_fedec_0_instr <= "0010000000000011";
				when 23 => pyleros_fedec_0_instr <= "0000100100000001";
				when 24 => pyleros_fedec_0_instr <= "0011000000000011";
				when 25 => pyleros_fedec_0_instr <= "0000110000000010";
				when 26 => pyleros_fedec_0_instr <= "0100110011110111";
				when 27 => pyleros_fedec_0_instr <= "0100100111110110";
				when 28 => pyleros_fedec_0_instr <= "0010000000000001";
				when 29 => pyleros_fedec_0_instr <= "0100000000000001";
				when 30 => pyleros_fedec_0_instr <= "0010000100000000";
				when 31 => pyleros_fedec_0_instr <= "0011000011111111";
				when 32 => pyleros_fedec_0_instr <= "0010000000000010";
				when 33 => pyleros_fedec_0_instr <= "0011000000011001";
				when 34 => pyleros_fedec_0_instr <= "0000000000000000";
				when 35 => pyleros_fedec_0_instr <= "0101000000011001";
				when 36 => pyleros_fedec_0_instr <= "0110000000000100";
				when 37 => pyleros_fedec_0_instr <= "0000100011111111";
				when 38 => pyleros_fedec_0_instr <= "0011000011111111";
				when 39 => pyleros_fedec_0_instr <= "0010000000011001";
				when 40 => pyleros_fedec_0_instr <= "0000110100000001";
				when 41 => pyleros_fedec_0_instr <= "0011000000011001";
				when 42 => pyleros_fedec_0_instr <= "0100101011111001";
				when 43 => pyleros_fedec_0_instr <= "0100100011100001";
				when others => pyleros_fedec_0_instr <= "0000000000000000";
			
    end case;
end process PYLEROS_PYLEROS_FEDEC_0_PYLEROS_IM_0_READ;


process (pyleros_fedec_0_pc, pyleros_fedec_0_pc_op) is
variable tmp_var : unsigned (8 downto 0) := (others => '0');
begin
	tmp_var := pyleros_fedec_0_pc + pyleros_fedec_0_pc_op;
	pyleros_fedec_0_pc_add <= tmp_var;
end process;


pyleros_fedec_0_instr_hi <= pyleros_fedec_0_instr(16-1 downto 8);
pyleros_fedec_0_im_addr <= pyleros_fedec_0_pc;


PYLEROS_PYLEROS_FEDEC_0_MUX_DM_ADDR: process (pyleros_fedec_0_decode_indls, back_dm_data, pyleros_fedec_0_instr) is
    variable offset_addr: unsigned(7 downto 0);
	 variable tmp_var : unsigned (15 downto 0) := (others => '0');
begin
	 tmp_var := back_dm_data + pyleros_fedec_0_instr(8-1 downto 0);
    offset_addr := tmp_var(8-1 downto 0);
    if (pyleros_fedec_0_decode_indls = '1') then
        pipe_dm_addr <= offset_addr(8-1 downto 0);
    else
        pipe_dm_addr <= pyleros_fedec_0_instr(8-1 downto 0);
    end if;
end process PYLEROS_PYLEROS_FEDEC_0_MUX_DM_ADDR;


PYLEROS_PYLEROS_FEDEC_0_PYLEROS_DECODER_0_DECODER: process (pyleros_fedec_0_instr_hi) is
    variable ins_ckh: integer;
begin
    
    pyleros_fedec_0_alu_op <= NOP;
    pyleros_fedec_0_decode_al_ena <= '0';
    pyleros_fedec_0_decode_ah_ena <= '0';
    pyleros_fedec_0_decode_log_add <= '0';
    pyleros_fedec_0_decode_add_sub <= '0';
    pyleros_fedec_0_decode_shr <= '0';
    pyleros_fedec_0_decode_sel_imm <= '0';
    pyleros_fedec_0_decode_store <= '0';
    pyleros_fedec_0_decode_outp <= '0';
    pyleros_fedec_0_decode_inp <= '0';
    pyleros_fedec_0_decode_outp <= '0';
    pyleros_fedec_0_decode_br_op <= '0';
    pyleros_fedec_0_decode_jal <= '0';
    pyleros_fedec_0_decode_loadh <= '0';
    pyleros_fedec_0_decode_indls <= '0';
    ins_ckh := to_integer(pyleros_fedec_0_instr_hi(7 downto 3));
    if (not (ins_ckh = 5)) then
        pyleros_fedec_0_decode_sel_imm <= pyleros_fedec_0_instr_hi(0);
    end if;
    case ins_ckh is
        when 0 =>
            null;
        when 1 =>
            pyleros_fedec_0_decode_al_ena <= '1';
            pyleros_fedec_0_decode_ah_ena <= '1';
            pyleros_fedec_0_decode_log_add <= '1';
            pyleros_fedec_0_decode_add_sub <= pyleros_fedec_0_instr_hi(2);
        when 2 =>
            pyleros_fedec_0_decode_al_ena <= '1';
            pyleros_fedec_0_decode_ah_ena <= '1';
            pyleros_fedec_0_decode_shr <= '1';
        when 3 =>
            null;
        when 4 =>
            pyleros_fedec_0_decode_al_ena <= '1';
            pyleros_fedec_0_decode_ah_ena <= '1';
        when 5 =>
            pyleros_fedec_0_decode_loadh <= '1';
            pyleros_fedec_0_decode_ah_ena <= '1';
        when 6 =>
            pyleros_fedec_0_decode_store <= '1';
        when 7 =>
            if (pyleros_fedec_0_instr_hi(2) = '0') then
                pyleros_fedec_0_decode_outp <= '1';
            else
                pyleros_fedec_0_decode_inp <= '1';
                pyleros_fedec_0_decode_al_ena <= '1';
                pyleros_fedec_0_decode_ah_ena <= '1';
            end if;
        when 8 =>
            pyleros_fedec_0_decode_jal <= '1';
            pyleros_fedec_0_decode_store <= '1';
        when 9 =>
            pyleros_fedec_0_decode_br_op <= '1';
        when 10 =>
            null;
        when 12 =>
            pyleros_fedec_0_decode_al_ena <= '1';
            pyleros_fedec_0_decode_ah_ena <= '1';
            pyleros_fedec_0_decode_indls <= '1';
        when 14 =>
            pyleros_fedec_0_decode_indls <= '1';
            pyleros_fedec_0_decode_store <= '1';
        when others =>
            pyleros_fedec_0_decode_ah_ena <= '0';
            pyleros_fedec_0_decode_al_ena <= '0';
    end case;
    if ((ins_ckh = 4) or (ins_ckh = 5) or (ins_ckh = 12)) then
        if (pyleros_fedec_0_instr_hi(3-1 downto 1) = 0) then
            pyleros_fedec_0_alu_op <= OP_LD;
        elsif (pyleros_fedec_0_instr_hi(3-1 downto 1) = 1) then
            pyleros_fedec_0_alu_op <= OP_AND;
        elsif (pyleros_fedec_0_instr_hi(3-1 downto 1) = 2) then
            pyleros_fedec_0_alu_op <=OP_OR;
        elsif (pyleros_fedec_0_instr_hi(3-1 downto 1) = 3) then
            pyleros_fedec_0_alu_op <= OP_XOR;
        else
            pyleros_fedec_0_alu_op <= NOP;
        end if;
    end if;
end process PYLEROS_PYLEROS_FEDEC_0_PYLEROS_DECODER_0_DECODER;


PYLEROS_PYLEROS_FEDEC_0_PC_ADDR: process (pyleros_fedec_0_instr, pyleros_fedec_0_branch_en) is
begin
    if (pyleros_fedec_0_branch_en = '1') then
        pyleros_fedec_0_pc_op <= unsigned(resize(signed(pyleros_fedec_0_instr(8-1 downto 0)), 9));
    else
        pyleros_fedec_0_pc_op <= to_unsigned(1, 9);
    end if;
end process PYLEROS_PYLEROS_FEDEC_0_PC_ADDR;


PYLEROS_PYLEROS_FEDEC_0_PC_MUX: process (pyleros_fedec_0_pc_add, pyleros_fedec_0_decode_jal, back_acc) is
begin
    if (pyleros_fedec_0_decode_jal = '1') then
        pyleros_fedec_0_pc_next <= back_acc(9-1 downto 0);
    else
        pyleros_fedec_0_pc_next <= pyleros_fedec_0_pc_add;
    end if;
end process PYLEROS_PYLEROS_FEDEC_0_PC_MUX;


PYLEROS_PYLEROS_FEDEC_0_INTR_PIPE: process (clk, reset) is
-- variable t_sig : std_logic := '0';
begin
    if (reset = '1') then
        pyleros_exec_0_pyleros_alu_0_dec_shr <= '0';
        pyleros_exec_0_pipe_dec_store <= '0';
        pipe_dec_outp <= '0';
        pyleros_fedec_0_pipe_dec_br_op <= '0';
        pyleros_exec_0_pipe_dec_jal <= '0';
        pyleros_fedec_0_pipe_dec_loadh <= '0';
        pipe_pc <= to_unsigned(000, 9);
        pyleros_fedec_0_pc <= to_unsigned(000, 9);
        pyleros_fedec_0_pipe_dec_indls <= '0';
        pyleros_exec_0_pipe_dec_al_ena <= '0';
        pipe_imm_val <= to_unsigned(0000, 16);
        pipe_alu_op <= NOP;
        pipe_dec_inp <= '0';
        pyleros_exec_0_pipe_dec_ah_ena <= '0';
        pyleros_exec_0_pyleros_alu_0_dec_add_sub <= '0';
        pyleros_exec_0_pipe_dec_sel_imm <= '0';
        pyleros_exec_0_pyleros_alu_0_dec_log_add <= '0';
    elsif rising_edge(clk) then
        if (pyleros_fedec_0_decode_loadh = '1') then
            
            pipe_imm_val(16-1 downto 8) <= pyleros_fedec_0_instr(8-1 downto 0);
            pipe_imm_val(8-1 downto 0) <= to_unsigned(0, 8);
        else
            pipe_imm_val <= resize(pyleros_fedec_0_instr(8-1 downto 0), 16);
        end if;
        pipe_pc <= pyleros_fedec_0_pc_add;
        pyleros_exec_0_pipe_dec_al_ena <= pyleros_fedec_0_decode_al_ena;
        pyleros_exec_0_pipe_dec_ah_ena <= pyleros_fedec_0_decode_ah_ena;
        pyleros_exec_0_pyleros_alu_0_dec_log_add <= pyleros_fedec_0_decode_log_add;
        pyleros_exec_0_pyleros_alu_0_dec_add_sub <= pyleros_fedec_0_decode_add_sub;
        pyleros_exec_0_pyleros_alu_0_dec_shr <= pyleros_fedec_0_decode_shr;
        pyleros_exec_0_pipe_dec_sel_imm <= pyleros_fedec_0_decode_sel_imm;
        pyleros_exec_0_pipe_dec_store <= pyleros_fedec_0_decode_store;
        pipe_dec_outp <= pyleros_fedec_0_decode_outp;
        pipe_dec_inp <= pyleros_fedec_0_decode_inp;
        pyleros_fedec_0_pipe_dec_br_op <= pyleros_fedec_0_decode_br_op;
        pyleros_exec_0_pipe_dec_jal <= pyleros_fedec_0_decode_jal;
        pyleros_fedec_0_pipe_dec_loadh <= pyleros_fedec_0_decode_loadh;
        pyleros_fedec_0_pipe_dec_indls <= pyleros_fedec_0_decode_indls;
        pipe_alu_op <= pyleros_fedec_0_alu_op;
        pyleros_fedec_0_pc <= pyleros_fedec_0_pc_next;
    end if;
end process PYLEROS_PYLEROS_FEDEC_0_INTR_PIPE;


PYLEROS_PYLEROS_FEDEC_0_BRANCH_SEL: process (pyleros_fedec_0_decode_br_op, pyleros_fedec_0_instr, back_acc) is
    variable br_type: unsigned(15 downto 0);
    variable acc_z: std_logic;
begin
    acc_z := '1';
    if (back_acc = 0) then
        acc_z := '1';
    else
        acc_z := '0';
    end if;
    pyleros_fedec_0_branch_en <= '0';
    if (pyleros_fedec_0_decode_br_op = '1') then
        br_type := resize(pyleros_fedec_0_instr(11-1 downto 8), 16);
        if (br_type = 0) then
            pyleros_fedec_0_branch_en <= '1';
        elsif (br_type = 1) then
            if (acc_z = '1') then
                pyleros_fedec_0_branch_en <= '1';
            else
                pyleros_fedec_0_branch_en <= '0';
            end if;
        elsif (br_type = 2) then
            if (not ((acc_z) = '1')) then
                pyleros_fedec_0_branch_en <= '1';
            else
                pyleros_fedec_0_branch_en <= '0';
            end if;
        elsif (br_type = 3) then
            if (not ((back_acc(15)) = '1')) then
                pyleros_fedec_0_branch_en <= '1';
            else
                pyleros_fedec_0_branch_en <= '0';
            end if;
        elsif (br_type = 4) then
            if (back_acc(15) = '1') then
                pyleros_fedec_0_branch_en <= '1';
            else
                pyleros_fedec_0_branch_en <= '0';
            end if;
        end if;
    end if;
end process PYLEROS_PYLEROS_FEDEC_0_BRANCH_SEL;

end architecture MyHDL;
