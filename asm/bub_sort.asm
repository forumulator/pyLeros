// Take n as the first input.
// Subsequently take n numbers and add them,
// then give output as the sum.

// first instruction is NOP, by conv.
	nop
	nop
	in 0 // input n
	store r2
	store r3 // DM[0] is 0x0000, DM[1] is reserved for jal
	store r4 // Counter for no. of inputs
	load <inp_lp
	jal r1
sort:
	load <outr_loop
	jal r1
outpu:
	load <outp_lp
	jal r1
nop_lp:
	nop
	branch nop_lp


// Input loop, take n inputs
inp_lp:
	in 0
	loadaddr r4
	store (ar+4)
	load r4
	sub 1
	store r4
	brnz inp_lp
	load r1
	jal r1

outp_lp:  // Loop for output of n numbers. 
	loadaddr r2
	load (ar+4)
	out 1
	load r2
	sub 1
	store r2
	brnz outp_lp
	load r1
	jal r1

outr_loop:   // Sorting loop
	load 1
	store r4
	load r3
	sub 1
	store r3
inr_loop: 
	loadaddr r4
	load (ar+4)
	store r252
	loadaddr r4
	load (ar+5)
	sub r252
	brn swap
ret_swap:
	load r4
	add 1
	store r4
	sub r3
	brn inr_loop
	brz inr_loop
	load r3
	brnz outr_loop
	load r1
	jal r1


swap:   // For the wap
	loadaddr r4
	load (ar+5)
	loadaddr r4
	store (ar+4)
	load r252
	loadaddr r4
	store (ar+5)
	branch ret_swap




