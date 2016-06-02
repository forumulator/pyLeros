from codes import *


def pass1(filename):
	
	f=open(filename+'_tr','r')
	
	sym_tab={}
	lc = 0
	pass1_o = []

	for line in f:
		#remove the comment part
		line = line.split('//')[0]

		# empty except for comments
		if (line == ''):
			continue
		
		temp = line.split()
		
		# storing the label in the sym_table	
		if(':' in temp[0]):
			label = temp[0]
			label = label.replace(':','')
			sym_tab[label] = lc
			# remove the label from the from pass 1 output
			continue
	
		asm_instr = temp[0]
		if asm_instr != 'DB' and asm_instr != 'DA':
			
			hex_instr = opttab[asm_instr]

			# no operand instruction, like SHR
			if (len(temp) == 1):
				pass1_o.append([hex_instr, 0, line,True])
				lc += 1
				continue
			else:
				operand = temp[1]

			# check for integer values
			# ADDI, LOAD, LOADH

			# HEX
			if (operand[0:2] == '0x'):
				#immediate value
				try:
					operand = int(operand, 16)
					pass1_o.append([hex_instr, operand, line, True])

				except Exception:
					return 1
				

			else:

				# Integer
				try:
					operand = int(operand, 16)
					pass1_o.append([hex_instr, operand, line, True])

				# Symbol
				except ValueError:
					pass1_o.append([hex_instr, operand, line, False])
				

			lc += 1


		else:
			# Add DB and DA to the ASM if necessary
			if(temp[0]=='DB'):
				res='DL#1 '+to_bin(temp[1],8)
			# temp[1] may not exist so make declarations like var a part of DA			
				lc+=1
			# tell prashant about eq assembler directive
			
			elif(temp[0]=='DA'):
				res='DL#2 '+temp[1]
				lc+=int(temp[1])


	f.close()

	fw = open(filename + '_p1', "wb")

	for o_line in pass1_o:
		print(hex(o_line[0]) + ' ' + str(o_line[1]) + ' //' + str(o_line[2]) + "\n")

	fw.close()
	return sym_tab,lc