# contains the opcodes
from codes import opttab
# assembler passes
from assembler import pass1, pass2
from linker import *


SYM_tab={}
N_tab={}
RELOC_tab={}
LINK_tab={}
LEN_tab={}
var_tab={}

def assemble(fname, offset):

    f = open(fname,'r')

    for line in f:
        filename=line.split()[0]
        trans(filename)

    f.seek(0,0)
    # pass 1 of the assembler for each file.
    for line in f:
        filename=line.split()[0]

        # pass1 of assembler
        SYM_tab[filename], LEN_tab[filename] = pass1(filename)

    f.seek(0,0)
    print("symbol table", SYM_tab)

    # pass 2 of assembler for each file
    for line in f:
       filename = line.split()[0]
        # pass2 of assembler
        RELOC_tab[filename], LINK_tab[filename] = pass2(filename, SYM_tab[filename])

    f.seek(0,0)
    print("reloc table",RELOC_tab,"\nlink table",LINK_tab)

    relocate_add = int(offset)
    temp = relocate_add

    # loading
    for line in f:
        filename=line.split()[0]
        N_tab[filename]=temp
        temp+=LEN_tab[filename]

    f.seek(0,0)
    print("N_TAB",N_tab)
    # linking the files
    for line in f:
        filename=line.split()[0]
        link_(filename,N_tab,RELOC_tab[filename],LINK_tab[filename],SYM_tab)

    f.seek(0,0)

    # get the final code ready for simulation
    fw=open('sim.txt','w')
  

    lc=relocate_add
    for line in f:
        filename=line.split()[0]
        f=open(filename+'_tr','r')
        for line in f:
            line=line.split()

            res=str(lc)+'   '

            if ':' in line[0]:
                line=line[1:3]

            res+=line[0]+' '
            if(opttab[line[0]][0]==1):

                lc+=opttab[line[0]][2]
                for op in line[1].split(','):
                    temp2=op.split('+')
                    op=temp2[0]
                    if len(temp2)>1:
                        extra=int(temp2[1])

                    else:
                        extra=0

                    if op in SYM_tab[filename].keys():
                        res+=str(SYM_tab[filename][op]+N_tab[filename]+extra)+' '
                        var_tab[SYM_tab[filename][op]+N_tab[filename]+extra]=op

                    elif op in ['A','B','C','D','E','H','L','M'] or op.isdigit():
                        res+=op+' '

                    else:

                        for fil in N_tab.keys():
                            if op in SYM_tab[fil].keys():
                                res+=str(SYM_tab[fil][op]+N_tab[fil]+extra)+' '
                                var_tab[SYM_tab[fil][op]+N_tab[fil]+extra]=op
                                break

            elif(opttab[line[0]][0]==2):
                if line[0]=='DB':
                    lc+=1
                else:
                    lc+=int(line[1])
                res+=line[1]

            else:
                lc+=1


            fw.write(res+'\n')
            
    print(SYM_tab)

    f.close()
    return var_tab
