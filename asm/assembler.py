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
		print(hex(o_line[0]) + ' ' + str(o_line[1]) + ' //' + str(o_line[2]) + "\n", file = fw)

	fw.close()
	return sym_tab, lc



def pass2(filename, pass1, sym_tab):

	f = open(filename+'_p1','r')
	lc = 0

	reloc_tab={}
	link_tab={}

	pass2_o = []

	for line in f:

		#remove the comment part
		line = line.split('//')[0]

		# empty except for comments
		if (line == ''):
			continue

		curr_line = [lc]

		temp = line.split()

		# to be added later, the DA, DB asm 
		# directives
		if('DL' in temp[0]):
			if '#1' in temp[0]:
				res+=temp[1]
				lc+=1
				fw.write(res+'\n')

			elif '#2' in temp[0]:
				for i in range(int(temp[1])):
					fw.write(str(lc)+'\n')
					lc+=1

		else:
			hex_instr = temp[0]
			curr_line.append(int(hex_instr, 16))

			if (len(temp) > 1):

				operand = temp[1]
				# implies temp[1] is a literal			 
				if operand.isdigit():
	
					curr_line.append(operand)
					curr_line.append(True)
					lc+=1

				else:
					# when temp[1] is not a literal	
					opsplit = operand.split('+')
					extra = opsplit[1] if len(opsplit) > 1 else 0
					operand = opsplit[0]

					if (temp[1] in sym_tab.keys()):
						# When the symbol is defined in the same file
						

						# here the address of the symbol might change due to relocation
						reloc_tab[str(lc)] = sym_tab[operand] + int(extra)
						curr_line.append(sym_tab[operand] + int(extra))
						curr_line.append(False)					
						
					else:
						# When the symbol needs to be linked to a diff file
						link_tab[str(lc)] = operand
						curr_line.append(0)
						curr_line.append[False]

					lc += 1

		pass2_o.append(curr_line)

	f.close()
	
	fw = open(filename + '_p2', "wb")
	for line in pass2_o:

		print(str(line[0]) + ' ' + bin(line[1])[2:] + ' ' + bin(line[2])[2:], file = fw)
	#print(link_tab)
	fw.close()
	
	return reloc_tab,link_tab