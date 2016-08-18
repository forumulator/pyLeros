-- File: ../generated/vhdl/pyleros_fedec.vhd
-- Generated by MyHDL 1.0dev
-- Date: Thu Aug 18 20:10:46 2016



package pck_pyleros_fedec is

attribute enum_encoding: string;

    type t_enum_alu_op_type_1 is (
    NOP,
    LD,
    AND,
    OR,
    XOR
);

end package pck_pyleros_fedec;

library IEEE;
use IEEE.std_logic_1164.all;
use IEEE.numeric_std.all;
use std.textio.all;

use work.pck_myhdl_10.all;

use work.pck_pyleros_fedec.all;

entity pyleros_fedec is
    port (
        clk: in std_logic;
        reset: in std_logic;
        back_acc: in unsigned(15 downto 0);
        back_dm_data: in unsigned(15 downto 0);
        fwd_accu: in unsigned(15 downto 0);
        pipe_alu_op: out t_enum_alu_op_type_1;
        pipe_imme: out unsigned(15 downto 0);
        pipe_dm_addr: out unsigned(7 downto 0);
        pipe_pc: out unsigned(8 downto 0);
        pipe_dec_loadh: out std_logic;
        pipe_dec_store: out std_logic;
        pipe_dec_log_add: out std_logic;
        pipe_dec_ah_ena: out std_logic;
        pipe_dec_br_op: out std_logic;
        pipe_dec_inp: out std_logic;
        pipe_dec_shr: out std_logic;
        pipe_dec_sel_imm: out std_logic;
        pipe_dec_al_ena: out std_logic;
        pipe_dec_add_sub: out std_logic;
        pipe_dec_jal: out std_logic;
        pipe_dec_outp: out std_logic;
        pipe_dec_indls: out std_logic
    );
end entity pyleros_fedec;
-- The fedec module for pyleros, that is, the fetch
-- and decode pipeline stage. The modules is purely 
-- combinatorial, except for the updating the pipeline 
-- register. The IM is instantied and only accessed
-- in this stage. The main functions done here are decoding
-- of instruction, setting up branch control signals, selection
-- of other control signals(including the ALU ones), selection 
-- of DM address. an ALU operation on two local variables takes
-- two cycles to execute and another cycle if the result needs 
-- to written back to a local variable
-- 
-- Arguments (ports):
--     clk: IN Clock signal
--     reset: IN Async reset signal
--     back_acc: IN Acc value accessed here, not written. This is
--         needed for setting the branch control signals and
--         for memory addredd of JAL
--     back_dm_data: IN The data read from the DM, which is needed for
--         an direct add or and indirect load/ store(which follows)
--     fwd_accu: IN The value of the accumulator, forwarded from the 
--             execute stage to provide proper branching. Currently unused. 
--     pipe_dec: OUT List of the decode signals, pass on to the execute stage
--     pipe_imme: OUT Immediate value, as taken from the lower bits 
--             of the instruction, pass on to execute stage
--     pipe_dm_addr: OUT DM read addr, pipeline register
--     pipe_pc: OUT the value of PC, pipeline register
-- 
-- Parameters:
-- 
--     filename: Name of the file or a list containing the instructions
--     debug: Debugging mode, the processor prints various error messages

architecture MyHDL of pyleros_fedec is



signal decode_sel_imm: std_logic;
signal alu_op: t_enum_alu_op_type_1;
signal branch_en: std_logic;
signal pc: unsigned(8 downto 0);
signal instr_hi: unsigned(7 downto 0);
signal decode_indls: std_logic;
signal decode_br_op: std_logic;
signal decode_inp: std_logic;
signal pc_next: unsigned(8 downto 0);
signal decode_log_add: std_logic;
signal decode_loadh: std_logic;
signal decode_al_ena: std_logic;
signal decode_store: std_logic;
signal decode_outp: std_logic;
signal decode_jal: std_logic;
signal decode_add_sub: std_logic;
signal pc_add: unsigned(8 downto 0);
signal nxt_dm_addr: unsigned(7 downto 0);
signal im_addr: unsigned(8 downto 0);
signal decode_ah_ena: std_logic;
signal decode_shr: std_logic;
signal pc_op: unsigned(15 downto 0);
signal instr: unsigned(15 downto 0);

begin





PYLEROS_FEDEC_BRANCH_SEL: process (back_acc, instr, decode_br_op) is
    variable br_type: unsigned(15 downto 0);
    variable acc_z: std_logic;
begin
    acc_z := '1';
    if (back_acc = 0) then
        acc_z := '1';
    else
        acc_z := '0';
    end if;
    branch_en <= '0';
    if bool(decode_br_op) then
        br_type := resize(instr(11-1 downto 8), 16);
        if (br_type = 0) then
            branch_en <= '1';
        elsif (br_type = 1) then
            if bool(acc_z) then
                branch_en <= '1';
            else
                branch_en <= '0';
            end if;
        elsif (br_type = 2) then
            if (not bool(acc_z)) then
                branch_en <= '1';
            else
                branch_en <= '0';
            end if;
        elsif (br_type = 3) then
            if (not bool(back_acc(15))) then
                branch_en <= '1';
            else
                branch_en <= '0';
            end if;
        elsif (br_type = 4) then
            if bool(back_acc(15)) then
                branch_en <= '1';
            else
                branch_en <= '0';
            end if;
        end if;
    end if;
end process PYLEROS_FEDEC_BRANCH_SEL;


PYLEROS_FEDEC_INTR_PIPE: process (clk, reset) is
begin
    if (reset = '1') then
        pipe_dec_indls <= '0';
        pipe_dec_store <= '0';
        pipe_dec_inp <= '0';
        pipe_alu_op <= NOP;
        pipe_dm_addr <= to_unsigned(00, 8);
        pipe_dec_jal <= '0';
        pipe_dec_log_add <= '0';
        pipe_dec_sel_imm <= '0';
        pc <= to_unsigned(000, 9);
        pipe_dec_outp <= '0';
        pipe_dec_loadh <= '0';
        pipe_dec_br_op <= '0';
        pipe_dec_ah_ena <= '0';
        pipe_dec_al_ena <= '0';
        pipe_dec_shr <= '0';
        pipe_dec_add_sub <= '0';
        pipe_pc <= to_unsigned(000, 9);
        pipe_imme <= to_unsigned(0000, 16);
    elsif rising_edge(clk) then
        if bool(decode_loadh) then
            
            pipe_imme(16-1 downto 8) <= instr(8-1 downto 0);
            pipe_imme(8-1 downto 0) <= to_unsigned(0, 8);
        else
            pipe_imme <= resize(instr(8-1 downto 0), 16);
        end if;
        pipe_pc <= pc_add;
        pipe_dec_al_ena <= decode_al_ena;
        pipe_dec_ah_ena <= decode_ah_ena;
        pipe_dec_log_add <= decode_log_add;
        pipe_dec_add_sub <= decode_add_sub;
        pipe_dec_shr <= decode_shr;
        pipe_dec_sel_imm <= decode_sel_imm;
        pipe_dec_store <= decode_store;
        pipe_dec_outp <= decode_outp;
        pipe_dec_inp <= decode_inp;
        pipe_dec_br_op <= decode_br_op;
        pipe_dec_jal <= decode_jal;
        pipe_dec_loadh <= decode_loadh;
        pipe_dec_indls <= decode_indls;
        pipe_alu_op <= alu_op;
        pipe_dm_addr <= nxt_dm_addr;
        pc <= pc_next;
    end if;
end process PYLEROS_FEDEC_INTR_PIPE;


PYLEROS_FEDEC_PC_ADDR: process (branch_en, instr) is
    variable sign_tmp: unsigned(8 downto 0);
begin
    if (branch_en = '1') then
        sign_tmp := instr(8-1 downto 0)(9-1 downto 0);
        if (instr(7) = '1') then
            sign_tmp := resize(((instr(8-1 downto 0) xor to_unsigned(-1, 8)) + 1)(8-1 downto 0), 9);
            sign_tmp := ((sign_tmp xor to_unsigned(-1, 9)) + 1)(9-1 downto 0);
        end if;
        pc_op <= resize(sign_tmp, 16);
    else
        pc_op <= to_unsigned(1, 16);
    end if;
end process PYLEROS_FEDEC_PC_ADDR;


PYLEROS_FEDEC_PC_MUX: process (pc_add, back_acc, decode_jal) is
begin
    if bool(decode_jal) then
        pc_next <= back_acc(9-1 downto 0);
    else
        pc_next <= pc_add;
    end if;
end process PYLEROS_FEDEC_PC_MUX;



pc_add <= (pc + pc_op)(9-1 downto 0);



instr_hi <= instr(16-1 downto 8);
im_addr <= pc;


PYLEROS_FEDEC_MUX_DM_ADDR: process (decode_indls, instr, back_dm_data) is
    variable offset_addr: unsigned(7 downto 0);
begin
    offset_addr := (back_dm_data + instr(8-1 downto 0))(8-1 downto 0);
    if bool(decode_indls) then
        nxt_dm_addr <= offset_addr(8-1 downto 0);
    else
        nxt_dm_addr <= instr(8-1 downto 0);
    end if;
end process PYLEROS_FEDEC_MUX_DM_ADDR;


PYLEROS_FEDEC_PYLEROS_DECODER_0_DECODER: process (instr_hi) is
    variable ins_ckh: integer;
begin
    
    alu_op <= NOP;
    decode_al_ena <= '0';
    decode_ah_ena <= '0';
    decode_log_add <= '0';
    decode_add_sub <= '0';
    decode_shr <= '0';
    decode_sel_imm <= '0';
    decode_store <= '0';
    decode_outp <= '0';
    decode_inp <= '0';
    decode_outp <= '0';
    decode_br_op <= '0';
    decode_jal <= '0';
    decode_loadh <= '0';
    decode_indls <= '0';
    ins_ckh := to_integer((instr_hi and to_unsigned(248, 8)));
    if (not (ins_ckh = 72)) then
        decode_sel_imm <= instr_hi(0);
    end if;
    case ins_ckh is
        when 0 =>
            null;
        when 1 =>
            decode_al_ena <= '1';
            decode_ah_ena <= '1';
            decode_log_add <= '1';
            decode_add_sub <= instr_hi(2);
        when 2 =>
            decode_al_ena <= '1';
            decode_ah_ena <= '1';
            decode_shr <= '1';
        when 3 =>
            null;
        when 4 =>
            decode_al_ena <= '1';
            decode_ah_ena <= '1';
        when 5 =>
            decode_loadh <= '1';
            decode_ah_ena <= '1';
        when 6 =>
            decode_store <= '1';
        when 7 =>
            if (instr_hi(2) = '0') then
                decode_outp <= '1';
            else
                decode_inp <= '1';
                decode_al_ena <= '1';
                decode_ah_ena <= '1';
            end if;
        when 8 =>
            decode_jal <= '1';
            decode_store <= '1';
        when 9 =>
            decode_br_op <= '1';
        when 10 =>
            null;
        when 11 =>
            decode_al_ena <= '1';
            decode_ah_ena <= '1';
            decode_indls <= '1';
        when 12 =>
            decode_indls <= '1';
            decode_store <= '1';
        when others =>
            decode_ah_ena <= '0';
            decode_al_ena <= '0';
    end case;
    if ((ins_ckh = 32) or (ins_ckh = 40) or (ins_ckh = 96)) then
        if (instr_hi(3-1 downto 1) = 0) then
            alu_op <= LD;
        elsif (instr_hi(3-1 downto 1) = 1) then
            alu_op <= AND;
        elsif (instr_hi(3-1 downto 1) = 2) then
            alu_op <= OR;
        elsif (instr_hi(3-1 downto 1) = 3) then
            alu_op <= XOR;
        else
            alu_op <= NOP;
        end if;
    end if;
end process PYLEROS_FEDEC_PYLEROS_DECODER_0_DECODER;


PYLEROS_FEDEC_PYLEROS_IM_0_READ: process (im_addr) is
begin
    
    case to_integer(im_addr) is
        when 0 => instr <= "0000000000000000";
        when 1 => instr <= "0000000000000000";
        when 2 => instr <= "0011110000000000";
        when 3 => instr <= "0011000000000010";
        when 4 => instr <= "0011000000000011";
        when 5 => instr <= "0010000100001011";
        when 6 => instr <= "0100000000000001";
        when 7 => instr <= "0100100000001101";
        when 8 => instr <= "0000000000000000";
        when 9 => instr <= "0010000011111111";
        when 10 => instr <= "0011100000000001";
        when 11 => instr <= "0011110000000000";
        when 12 => instr <= "0101000000000011";
        when 13 => instr <= "0111000000000100";
        when 14 => instr <= "0010000000000011";
        when 15 => instr <= "0000110100000001";
        when 16 => instr <= "0011000000000011";
        when 17 => instr <= "0100101011111010";
        when 18 => instr <= "0010000000000001";
        when 19 => instr <= "0100000000000001";
        when 20 => instr <= "0010000100000000";
        when 21 => instr <= "0011000011111111";
        when 22 => instr <= "0010000000000011";
        when 23 => instr <= "0000100100000001";
        when 24 => instr <= "0011000000000011";
        when 25 => instr <= "0101000000000011";
        when 26 => instr <= "0110000000000100";
        when 27 => instr <= "0000100011111111";
        when 28 => instr <= "0011000011111111";
        when 29 => instr <= "0010000000000011";
        when 30 => instr <= "0000110000000010";
        when 31 => instr <= "0100100111101010";
        when 32 => instr <= "0100100011110110";
        when 33 => instr <= "0000000000000000";
        when 34 => instr <= "0000000000000000";
        when 35 => instr <= "0000000000000000";
        when 36 => instr <= "0000000000000000";
        when 37 => instr <= "0000000000000000";
        when 38 => instr <= "0000000000000000";
        when 39 => instr <= "0000000000000000";
        when 40 => instr <= "0000000000000000";
        when 41 => instr <= "0000000000000000";
        when 42 => instr <= "0000000000000000";
        when 43 => instr <= "0000000000000000";
        when 44 => instr <= "0000000000000000";
        when 45 => instr <= "0000000000000000";
        when 46 => instr <= "0000000000000000";
        when 47 => instr <= "0000000000000000";
        when 48 => instr <= "0000000000000000";
        when 49 => instr <= "0000000000000000";
        when 50 => instr <= "0000000000000000";
        when 51 => instr <= "0000000000000000";
        when 52 => instr <= "0000000000000000";
        when 53 => instr <= "0000000000000000";
        when 54 => instr <= "0000000000000000";
        when 55 => instr <= "0000000000000000";
        when 56 => instr <= "0000000000000000";
        when 57 => instr <= "0000000000000000";
        when 58 => instr <= "0000000000000000";
        when 59 => instr <= "0000000000000000";
        when 60 => instr <= "0000000000000000";
        when 61 => instr <= "0000000000000000";
        when 62 => instr <= "0000000000000000";
        when 63 => instr <= "0000000000000000";
        when 64 => instr <= "0000000000000000";
        when 65 => instr <= "0000000000000000";
        when 66 => instr <= "0000000000000000";
        when 67 => instr <= "0000000000000000";
        when 68 => instr <= "0000000000000000";
        when 69 => instr <= "0000000000000000";
        when 70 => instr <= "0000000000000000";
        when 71 => instr <= "0000000000000000";
        when 72 => instr <= "0000000000000000";
        when 73 => instr <= "0000000000000000";
        when 74 => instr <= "0000000000000000";
        when 75 => instr <= "0000000000000000";
        when 76 => instr <= "0000000000000000";
        when 77 => instr <= "0000000000000000";
        when 78 => instr <= "0000000000000000";
        when 79 => instr <= "0000000000000000";
        when 80 => instr <= "0000000000000000";
        when 81 => instr <= "0000000000000000";
        when 82 => instr <= "0000000000000000";
        when 83 => instr <= "0000000000000000";
        when 84 => instr <= "0000000000000000";
        when 85 => instr <= "0000000000000000";
        when 86 => instr <= "0000000000000000";
        when 87 => instr <= "0000000000000000";
        when 88 => instr <= "0000000000000000";
        when 89 => instr <= "0000000000000000";
        when 90 => instr <= "0000000000000000";
        when 91 => instr <= "0000000000000000";
        when 92 => instr <= "0000000000000000";
        when 93 => instr <= "0000000000000000";
        when 94 => instr <= "0000000000000000";
        when 95 => instr <= "0000000000000000";
        when 96 => instr <= "0000000000000000";
        when 97 => instr <= "0000000000000000";
        when 98 => instr <= "0000000000000000";
        when 99 => instr <= "0000000000000000";
        when 100 => instr <= "0000000000000000";
        when 101 => instr <= "0000000000000000";
        when 102 => instr <= "0000000000000000";
        when 103 => instr <= "0000000000000000";
        when 104 => instr <= "0000000000000000";
        when 105 => instr <= "0000000000000000";
        when 106 => instr <= "0000000000000000";
        when 107 => instr <= "0000000000000000";
        when 108 => instr <= "0000000000000000";
        when 109 => instr <= "0000000000000000";
        when 110 => instr <= "0000000000000000";
        when 111 => instr <= "0000000000000000";
        when 112 => instr <= "0000000000000000";
        when 113 => instr <= "0000000000000000";
        when 114 => instr <= "0000000000000000";
        when 115 => instr <= "0000000000000000";
        when 116 => instr <= "0000000000000000";
        when 117 => instr <= "0000000000000000";
        when 118 => instr <= "0000000000000000";
        when 119 => instr <= "0000000000000000";
        when 120 => instr <= "0000000000000000";
        when 121 => instr <= "0000000000000000";
        when 122 => instr <= "0000000000000000";
        when 123 => instr <= "0000000000000000";
        when 124 => instr <= "0000000000000000";
        when 125 => instr <= "0000000000000000";
        when 126 => instr <= "0000000000000000";
        when 127 => instr <= "0000000000000000";
        when 128 => instr <= "0000000000000000";
        when 129 => instr <= "0000000000000000";
        when 130 => instr <= "0000000000000000";
        when 131 => instr <= "0000000000000000";
        when 132 => instr <= "0000000000000000";
        when 133 => instr <= "0000000000000000";
        when 134 => instr <= "0000000000000000";
        when 135 => instr <= "0000000000000000";
        when 136 => instr <= "0000000000000000";
        when 137 => instr <= "0000000000000000";
        when 138 => instr <= "0000000000000000";
        when 139 => instr <= "0000000000000000";
        when 140 => instr <= "0000000000000000";
        when 141 => instr <= "0000000000000000";
        when 142 => instr <= "0000000000000000";
        when 143 => instr <= "0000000000000000";
        when 144 => instr <= "0000000000000000";
        when 145 => instr <= "0000000000000000";
        when 146 => instr <= "0000000000000000";
        when 147 => instr <= "0000000000000000";
        when 148 => instr <= "0000000000000000";
        when 149 => instr <= "0000000000000000";
        when 150 => instr <= "0000000000000000";
        when 151 => instr <= "0000000000000000";
        when 152 => instr <= "0000000000000000";
        when 153 => instr <= "0000000000000000";
        when 154 => instr <= "0000000000000000";
        when 155 => instr <= "0000000000000000";
        when 156 => instr <= "0000000000000000";
        when 157 => instr <= "0000000000000000";
        when 158 => instr <= "0000000000000000";
        when 159 => instr <= "0000000000000000";
        when 160 => instr <= "0000000000000000";
        when 161 => instr <= "0000000000000000";
        when 162 => instr <= "0000000000000000";
        when 163 => instr <= "0000000000000000";
        when 164 => instr <= "0000000000000000";
        when 165 => instr <= "0000000000000000";
        when 166 => instr <= "0000000000000000";
        when 167 => instr <= "0000000000000000";
        when 168 => instr <= "0000000000000000";
        when 169 => instr <= "0000000000000000";
        when 170 => instr <= "0000000000000000";
        when 171 => instr <= "0000000000000000";
        when 172 => instr <= "0000000000000000";
        when 173 => instr <= "0000000000000000";
        when 174 => instr <= "0000000000000000";
        when 175 => instr <= "0000000000000000";
        when 176 => instr <= "0000000000000000";
        when 177 => instr <= "0000000000000000";
        when 178 => instr <= "0000000000000000";
        when 179 => instr <= "0000000000000000";
        when 180 => instr <= "0000000000000000";
        when 181 => instr <= "0000000000000000";
        when 182 => instr <= "0000000000000000";
        when 183 => instr <= "0000000000000000";
        when 184 => instr <= "0000000000000000";
        when 185 => instr <= "0000000000000000";
        when 186 => instr <= "0000000000000000";
        when 187 => instr <= "0000000000000000";
        when 188 => instr <= "0000000000000000";
        when 189 => instr <= "0000000000000000";
        when 190 => instr <= "0000000000000000";
        when 191 => instr <= "0000000000000000";
        when 192 => instr <= "0000000000000000";
        when 193 => instr <= "0000000000000000";
        when 194 => instr <= "0000000000000000";
        when 195 => instr <= "0000000000000000";
        when 196 => instr <= "0000000000000000";
        when 197 => instr <= "0000000000000000";
        when 198 => instr <= "0000000000000000";
        when 199 => instr <= "0000000000000000";
        when 200 => instr <= "0000000000000000";
        when 201 => instr <= "0000000000000000";
        when 202 => instr <= "0000000000000000";
        when 203 => instr <= "0000000000000000";
        when 204 => instr <= "0000000000000000";
        when 205 => instr <= "0000000000000000";
        when 206 => instr <= "0000000000000000";
        when 207 => instr <= "0000000000000000";
        when 208 => instr <= "0000000000000000";
        when 209 => instr <= "0000000000000000";
        when 210 => instr <= "0000000000000000";
        when 211 => instr <= "0000000000000000";
        when 212 => instr <= "0000000000000000";
        when 213 => instr <= "0000000000000000";
        when 214 => instr <= "0000000000000000";
        when 215 => instr <= "0000000000000000";
        when 216 => instr <= "0000000000000000";
        when 217 => instr <= "0000000000000000";
        when 218 => instr <= "0000000000000000";
        when 219 => instr <= "0000000000000000";
        when 220 => instr <= "0000000000000000";
        when 221 => instr <= "0000000000000000";
        when 222 => instr <= "0000000000000000";
        when 223 => instr <= "0000000000000000";
        when 224 => instr <= "0000000000000000";
        when 225 => instr <= "0000000000000000";
        when 226 => instr <= "0000000000000000";
        when 227 => instr <= "0000000000000000";
        when 228 => instr <= "0000000000000000";
        when 229 => instr <= "0000000000000000";
        when 230 => instr <= "0000000000000000";
        when 231 => instr <= "0000000000000000";
        when 232 => instr <= "0000000000000000";
        when 233 => instr <= "0000000000000000";
        when 234 => instr <= "0000000000000000";
        when 235 => instr <= "0000000000000000";
        when 236 => instr <= "0000000000000000";
        when 237 => instr <= "0000000000000000";
        when 238 => instr <= "0000000000000000";
        when 239 => instr <= "0000000000000000";
        when 240 => instr <= "0000000000000000";
        when 241 => instr <= "0000000000000000";
        when 242 => instr <= "0000000000000000";
        when 243 => instr <= "0000000000000000";
        when 244 => instr <= "0000000000000000";
        when 245 => instr <= "0000000000000000";
        when 246 => instr <= "0000000000000000";
        when 247 => instr <= "0000000000000000";
        when 248 => instr <= "0000000000000000";
        when 249 => instr <= "0000000000000000";
        when 250 => instr <= "0000000000000000";
        when 251 => instr <= "0000000000000000";
        when 252 => instr <= "0000000000000000";
        when 253 => instr <= "0000000000000000";
        when 254 => instr <= "0000000000000000";
        when 255 => instr <= "0000000000000000";
        when 256 => instr <= "0000000000000000";
        when 257 => instr <= "0000000000000000";
        when 258 => instr <= "0000000000000000";
        when 259 => instr <= "0000000000000000";
        when 260 => instr <= "0000000000000000";
        when 261 => instr <= "0000000000000000";
        when 262 => instr <= "0000000000000000";
        when 263 => instr <= "0000000000000000";
        when 264 => instr <= "0000000000000000";
        when 265 => instr <= "0000000000000000";
        when 266 => instr <= "0000000000000000";
        when 267 => instr <= "0000000000000000";
        when 268 => instr <= "0000000000000000";
        when 269 => instr <= "0000000000000000";
        when 270 => instr <= "0000000000000000";
        when 271 => instr <= "0000000000000000";
        when 272 => instr <= "0000000000000000";
        when 273 => instr <= "0000000000000000";
        when 274 => instr <= "0000000000000000";
        when 275 => instr <= "0000000000000000";
        when 276 => instr <= "0000000000000000";
        when 277 => instr <= "0000000000000000";
        when 278 => instr <= "0000000000000000";
        when 279 => instr <= "0000000000000000";
        when 280 => instr <= "0000000000000000";
        when 281 => instr <= "0000000000000000";
        when 282 => instr <= "0000000000000000";
        when 283 => instr <= "0000000000000000";
        when 284 => instr <= "0000000000000000";
        when 285 => instr <= "0000000000000000";
        when 286 => instr <= "0000000000000000";
        when 287 => instr <= "0000000000000000";
        when 288 => instr <= "0000000000000000";
        when 289 => instr <= "0000000000000000";
        when 290 => instr <= "0000000000000000";
        when 291 => instr <= "0000000000000000";
        when 292 => instr <= "0000000000000000";
        when 293 => instr <= "0000000000000000";
        when 294 => instr <= "0000000000000000";
        when 295 => instr <= "0000000000000000";
        when 296 => instr <= "0000000000000000";
        when 297 => instr <= "0000000000000000";
        when 298 => instr <= "0000000000000000";
        when 299 => instr <= "0000000000000000";
        when 300 => instr <= "0000000000000000";
        when 301 => instr <= "0000000000000000";
        when 302 => instr <= "0000000000000000";
        when 303 => instr <= "0000000000000000";
        when 304 => instr <= "0000000000000000";
        when 305 => instr <= "0000000000000000";
        when 306 => instr <= "0000000000000000";
        when 307 => instr <= "0000000000000000";
        when 308 => instr <= "0000000000000000";
        when 309 => instr <= "0000000000000000";
        when 310 => instr <= "0000000000000000";
        when 311 => instr <= "0000000000000000";
        when 312 => instr <= "0000000000000000";
        when 313 => instr <= "0000000000000000";
        when 314 => instr <= "0000000000000000";
        when 315 => instr <= "0000000000000000";
        when 316 => instr <= "0000000000000000";
        when 317 => instr <= "0000000000000000";
        when 318 => instr <= "0000000000000000";
        when 319 => instr <= "0000000000000000";
        when 320 => instr <= "0000000000000000";
        when 321 => instr <= "0000000000000000";
        when 322 => instr <= "0000000000000000";
        when 323 => instr <= "0000000000000000";
        when 324 => instr <= "0000000000000000";
        when 325 => instr <= "0000000000000000";
        when 326 => instr <= "0000000000000000";
        when 327 => instr <= "0000000000000000";
        when 328 => instr <= "0000000000000000";
        when 329 => instr <= "0000000000000000";
        when 330 => instr <= "0000000000000000";
        when 331 => instr <= "0000000000000000";
        when 332 => instr <= "0000000000000000";
        when 333 => instr <= "0000000000000000";
        when 334 => instr <= "0000000000000000";
        when 335 => instr <= "0000000000000000";
        when 336 => instr <= "0000000000000000";
        when 337 => instr <= "0000000000000000";
        when 338 => instr <= "0000000000000000";
        when 339 => instr <= "0000000000000000";
        when 340 => instr <= "0000000000000000";
        when 341 => instr <= "0000000000000000";
        when 342 => instr <= "0000000000000000";
        when 343 => instr <= "0000000000000000";
        when 344 => instr <= "0000000000000000";
        when 345 => instr <= "0000000000000000";
        when 346 => instr <= "0000000000000000";
        when 347 => instr <= "0000000000000000";
        when 348 => instr <= "0000000000000000";
        when 349 => instr <= "0000000000000000";
        when 350 => instr <= "0000000000000000";
        when 351 => instr <= "0000000000000000";
        when 352 => instr <= "0000000000000000";
        when 353 => instr <= "0000000000000000";
        when 354 => instr <= "0000000000000000";
        when 355 => instr <= "0000000000000000";
        when 356 => instr <= "0000000000000000";
        when 357 => instr <= "0000000000000000";
        when 358 => instr <= "0000000000000000";
        when 359 => instr <= "0000000000000000";
        when 360 => instr <= "0000000000000000";
        when 361 => instr <= "0000000000000000";
        when 362 => instr <= "0000000000000000";
        when 363 => instr <= "0000000000000000";
        when 364 => instr <= "0000000000000000";
        when 365 => instr <= "0000000000000000";
        when 366 => instr <= "0000000000000000";
        when 367 => instr <= "0000000000000000";
        when 368 => instr <= "0000000000000000";
        when 369 => instr <= "0000000000000000";
        when 370 => instr <= "0000000000000000";
        when 371 => instr <= "0000000000000000";
        when 372 => instr <= "0000000000000000";
        when 373 => instr <= "0000000000000000";
        when 374 => instr <= "0000000000000000";
        when 375 => instr <= "0000000000000000";
        when 376 => instr <= "0000000000000000";
        when 377 => instr <= "0000000000000000";
        when 378 => instr <= "0000000000000000";
        when 379 => instr <= "0000000000000000";
        when 380 => instr <= "0000000000000000";
        when 381 => instr <= "0000000000000000";
        when 382 => instr <= "0000000000000000";
        when 383 => instr <= "0000000000000000";
        when 384 => instr <= "0000000000000000";
        when 385 => instr <= "0000000000000000";
        when 386 => instr <= "0000000000000000";
        when 387 => instr <= "0000000000000000";
        when 388 => instr <= "0000000000000000";
        when 389 => instr <= "0000000000000000";
        when 390 => instr <= "0000000000000000";
        when 391 => instr <= "0000000000000000";
        when 392 => instr <= "0000000000000000";
        when 393 => instr <= "0000000000000000";
        when 394 => instr <= "0000000000000000";
        when 395 => instr <= "0000000000000000";
        when 396 => instr <= "0000000000000000";
        when 397 => instr <= "0000000000000000";
        when 398 => instr <= "0000000000000000";
        when 399 => instr <= "0000000000000000";
        when 400 => instr <= "0000000000000000";
        when 401 => instr <= "0000000000000000";
        when 402 => instr <= "0000000000000000";
        when 403 => instr <= "0000000000000000";
        when 404 => instr <= "0000000000000000";
        when 405 => instr <= "0000000000000000";
        when 406 => instr <= "0000000000000000";
        when 407 => instr <= "0000000000000000";
        when 408 => instr <= "0000000000000000";
        when 409 => instr <= "0000000000000000";
        when 410 => instr <= "0000000000000000";
        when 411 => instr <= "0000000000000000";
        when 412 => instr <= "0000000000000000";
        when 413 => instr <= "0000000000000000";
        when 414 => instr <= "0000000000000000";
        when 415 => instr <= "0000000000000000";
        when 416 => instr <= "0000000000000000";
        when 417 => instr <= "0000000000000000";
        when 418 => instr <= "0000000000000000";
        when 419 => instr <= "0000000000000000";
        when 420 => instr <= "0000000000000000";
        when 421 => instr <= "0000000000000000";
        when 422 => instr <= "0000000000000000";
        when 423 => instr <= "0000000000000000";
        when 424 => instr <= "0000000000000000";
        when 425 => instr <= "0000000000000000";
        when 426 => instr <= "0000000000000000";
        when 427 => instr <= "0000000000000000";
        when 428 => instr <= "0000000000000000";
        when 429 => instr <= "0000000000000000";
        when 430 => instr <= "0000000000000000";
        when 431 => instr <= "0000000000000000";
        when 432 => instr <= "0000000000000000";
        when 433 => instr <= "0000000000000000";
        when 434 => instr <= "0000000000000000";
        when 435 => instr <= "0000000000000000";
        when 436 => instr <= "0000000000000000";
        when 437 => instr <= "0000000000000000";
        when 438 => instr <= "0000000000000000";
        when 439 => instr <= "0000000000000000";
        when 440 => instr <= "0000000000000000";
        when 441 => instr <= "0000000000000000";
        when 442 => instr <= "0000000000000000";
        when 443 => instr <= "0000000000000000";
        when 444 => instr <= "0000000000000000";
        when 445 => instr <= "0000000000000000";
        when 446 => instr <= "0000000000000000";
        when 447 => instr <= "0000000000000000";
        when 448 => instr <= "0000000000000000";
        when 449 => instr <= "0000000000000000";
        when 450 => instr <= "0000000000000000";
        when 451 => instr <= "0000000000000000";
        when 452 => instr <= "0000000000000000";
        when 453 => instr <= "0000000000000000";
        when 454 => instr <= "0000000000000000";
        when 455 => instr <= "0000000000000000";
        when 456 => instr <= "0000000000000000";
        when 457 => instr <= "0000000000000000";
        when 458 => instr <= "0000000000000000";
        when 459 => instr <= "0000000000000000";
        when 460 => instr <= "0000000000000000";
        when 461 => instr <= "0000000000000000";
        when 462 => instr <= "0000000000000000";
        when 463 => instr <= "0000000000000000";
        when 464 => instr <= "0000000000000000";
        when 465 => instr <= "0000000000000000";
        when 466 => instr <= "0000000000000000";
        when 467 => instr <= "0000000000000000";
        when 468 => instr <= "0000000000000000";
        when 469 => instr <= "0000000000000000";
        when 470 => instr <= "0000000000000000";
        when 471 => instr <= "0000000000000000";
        when 472 => instr <= "0000000000000000";
        when 473 => instr <= "0000000000000000";
        when 474 => instr <= "0000000000000000";
        when 475 => instr <= "0000000000000000";
        when 476 => instr <= "0000000000000000";
        when 477 => instr <= "0000000000000000";
        when 478 => instr <= "0000000000000000";
        when 479 => instr <= "0000000000000000";
        when 480 => instr <= "0000000000000000";
        when 481 => instr <= "0000000000000000";
        when 482 => instr <= "0000000000000000";
        when 483 => instr <= "0000000000000000";
        when 484 => instr <= "0000000000000000";
        when 485 => instr <= "0000000000000000";
        when 486 => instr <= "0000000000000000";
        when 487 => instr <= "0000000000000000";
        when 488 => instr <= "0000000000000000";
        when 489 => instr <= "0000000000000000";
        when 490 => instr <= "0000000000000000";
        when 491 => instr <= "0000000000000000";
        when 492 => instr <= "0000000000000000";
        when 493 => instr <= "0000000000000000";
        when 494 => instr <= "0000000000000000";
        when 495 => instr <= "0000000000000000";
        when 496 => instr <= "0000000000000000";
        when 497 => instr <= "0000000000000000";
        when 498 => instr <= "0000000000000000";
        when 499 => instr <= "0000000000000000";
        when 500 => instr <= "0000000000000000";
        when 501 => instr <= "0000000000000000";
        when 502 => instr <= "0000000000000000";
        when 503 => instr <= "0000000000000000";
        when 504 => instr <= "0000000000000000";
        when 505 => instr <= "0000000000000000";
        when 506 => instr <= "0000000000000000";
        when 507 => instr <= "0000000000000000";
        when 508 => instr <= "0000000000000000";
        when 509 => instr <= "0000000000000000";
        when 510 => instr <= "0000000000000000";
        when 511 => instr <= "0000000000000000";
        when 512 => instr <= "0000000000000000";
        when 513 => instr <= "0000000000000000";
        when 514 => instr <= "0000000000000000";
        when 515 => instr <= "0000000000000000";
        when others => instr <= "0000000000000000";
    end case;
end process PYLEROS_FEDEC_PYLEROS_IM_0_READ;

end architecture MyHDL;