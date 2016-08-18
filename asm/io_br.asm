// Add 5 numbers, taken as input and output their sum

nop // First instruction
in 0 //Dummy input
load 5
store r1
load 0
store r2
branch outlp
end:
	load r2
	out 1

outlp: 
	in 0
	add r2
	store r2
	load r1
	sub 1
	store r1
	brnz outlp
	branch end
