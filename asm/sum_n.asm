// Take n as the first input.
// Subsequently take n numbers and add them,
// then give output as the sum.

// first instruction is NOP, by conv.
	nop
	nop
	in 0 // input n
	store r2 // DM[0] is 0x0000, DM[1] is reserved for jal
	load 1
	store r3 // Counter for no. of inputs
	load <inp_lp
	jal r1
next:
	branch pre_sum_lp
	nop
end:
	load r255
	out 1

// Input loop, take n inputs
inp_lp:
	in 0
	loadaddr r3
	store (ar+4)
	load r3
	add 1
	store r3
	sub r2
	brn inp_lp
	brz inp_lp
	load r1
	jal r1


pre_sum_lp:
	load 0
	store r255
	load 1
	store r3
sum_lp: // Add n numbers, the result is always stored in DM[255]
	loadaddr r3
	load (ar+4)
	add r255
	store r255
	load r3
	add 1
	store r3
	sub r2
	brn sum_lp
	brz sum_lp
	branch end






