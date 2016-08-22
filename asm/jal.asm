// Test the JAL instruction


nop // First instruction.
in 0
in 0
store r2
load 5
xor 27
load <next
jal r1
nop
nop
load r2
out 1

next:
	load 5
	load r1
	jal r1
	load 10
	out 1
