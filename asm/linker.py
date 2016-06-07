from codes import *


def link_(filename,n_tab,reloc_tab,link_tab,SYM_tab):
	f=open(filename+'_p2','r')
	fw=open(filename+'_l','w')

	lc=n_tab[filename]
	marker=0
	for line in f:
		line=line.split()

		if(line!=[] and marker==0):

			if line[0] in reloc_tab.keys():
				x=reloc_tab[line[0]]
				x+=n_tab[filename]
				bin_=to_bin(x,16)
				marker=1
				res=str(lc)+'   '+bin_[8:16]+'\n'
				lc+=1
				res+=str(lc)+'   '+bin_[0:8]+'\n'
				lc+=1

				fw.write(res)

			elif line[0] in link_tab.keys():
				gh=link_tab[line[0]]
				print(link_tab)
				req_fil=''
				for fil in n_tab.keys():
					if gh in SYM_tab[fil].keys():
						req_fil,add=fil,SYM_tab[fil][gh]
						break

				if req_fil=='':
					print( 'CANT FIND a value',gh)

				else:

					add+=n_tab[req_fil]
					bin_=to_bin(add,16)
					marker=1
					res=str(lc)+'   '+bin_[8:16]+'\n'
					lc+=1
					res+=str(lc)+'   '+bin_[0:8]+'\n'
					lc+=1

				fw.write(res)
				

			else:
				if len(line)>1:
					res=str(lc)+'   '+line[1]+'\n'

				else:
					res=str(lc)+'\n'

				lc+=1
				fw.write(res)


		elif marker==1:
			marker=0

		else:
			fw.write('\n')		


				



