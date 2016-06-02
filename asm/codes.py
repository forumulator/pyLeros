opttab={'NOP':0x00}

opttab['DB']=[2,]
opttab['DA']=[2,]

opttab['ADD'] = 0x08
opttab['ADDI'] = 0x09
opttab['SUB'] = 0x0c
opttab['SUBI'] = 0x08

# Shift Right
opttab['SHR'] = 0x10

# Load immediate
opttab['LOAD'] = 0x21

opttab['AND'] = 0x22
opttab['ANDI'] = 0x23

opttab['OR'] = 0x24
opttab['ORI'] = 0x25
opttab['XOR'] = 0x26
opttab['XORI'] = 0x27

opttab['LOADH'] = 0x28
opttab['LDHI'] = 0x29

opttab['STORE'] = 0x30

opttab['OUT'] = 0x38
opttab['IN'] = 0x3c

opttab['JAL'] = 0x40

opttab['LOADADDR'] = 0x50

# Load accumulator indirect
opttab['LDAX'] = 0x60
opttab['STAX'] = 0x70


def to_bin(x,num):
	x=int(x)
	ans=str('')
	for i in range(num):
		ans=str(x%2)+ans
		x=int(x/2)

	return ans	