// $ANTLR 3.3 Nov 30, 2010 12:50:56 java/tools/src/grammar/Leros.g 2016-08-18 12:33:15

package leros.asm.generated;

import java.util.HashMap;
import java.util.List;



import org.antlr.runtime.*;
import java.util.Stack;
import java.util.List;
import java.util.ArrayList;

public class LerosParser extends Parser {
    public static final String[] tokenNames = new String[] {
        "<invalid>", "<EOR>", "<DOWN>", "<UP>", "COMMENT", "NEWLINE", "ID", "REG", "INT", "WHITSPACE", "':'", "'.start'", "'nop'", "'shr'", "'add'", "'sub'", "'load'", "'and'", "'or'", "'xor'", "'loadh'", "'store'", "'jal'", "'out'", "'in'", "'loadaddr'", "'('", "'ar'", "'+'", "')'", "'branch'", "'brz'", "'brnz'", "'brp'", "'brn'", "'-'", "'<'", "'>'"
    };
    public static final int EOF=-1;
    public static final int T__10=10;
    public static final int T__11=11;
    public static final int T__12=12;
    public static final int T__13=13;
    public static final int T__14=14;
    public static final int T__15=15;
    public static final int T__16=16;
    public static final int T__17=17;
    public static final int T__18=18;
    public static final int T__19=19;
    public static final int T__20=20;
    public static final int T__21=21;
    public static final int T__22=22;
    public static final int T__23=23;
    public static final int T__24=24;
    public static final int T__25=25;
    public static final int T__26=26;
    public static final int T__27=27;
    public static final int T__28=28;
    public static final int T__29=29;
    public static final int T__30=30;
    public static final int T__31=31;
    public static final int T__32=32;
    public static final int T__33=33;
    public static final int T__34=34;
    public static final int T__35=35;
    public static final int T__36=36;
    public static final int T__37=37;
    public static final int COMMENT=4;
    public static final int NEWLINE=5;
    public static final int ID=6;
    public static final int REG=7;
    public static final int INT=8;
    public static final int WHITSPACE=9;

    // delegates
    // delegators


        public LerosParser(TokenStream input) {
            this(input, new RecognizerSharedState());
        }
        public LerosParser(TokenStream input, RecognizerSharedState state) {
            super(input, state);
             
        }
        

    public String[] getTokenNames() { return LerosParser.tokenNames; }
    public String getGrammarFileName() { return "java/tools/src/grammar/Leros.g"; }


    /** Map symbol to Integer object holding the value or address */
    HashMap symbols = new HashMap();
    // Mapping of register names
    HashMap reg = new HashMap();
    int pc = 0;
    int code[];
    boolean pass2 = false;

    static {
    	// some default names for registers
    	for (int i=0; i<16; ++i) {
    //		reg.put("r"+i, new Integer(i));
    	}
    }

    public static String niceHex(int val) {
    	String s = Integer.toHexString(val);
    	while (s.length() < 4) {
    		s = "0"+s;
    	}
    	s = "0x"+s;
    	return s;
    }



    // $ANTLR start "pass1"
    // java/tools/src/grammar/Leros.g:75:1: pass1 : ( statement )+ ;
    public final void pass1() throws RecognitionException {
        try {
            // java/tools/src/grammar/Leros.g:75:6: ( ( statement )+ )
            // java/tools/src/grammar/Leros.g:75:8: ( statement )+
            {
            // java/tools/src/grammar/Leros.g:75:8: ( statement )+
            int cnt1=0;
            loop1:
            do {
                int alt1=2;
                int LA1_0 = input.LA(1);

                if ( ((LA1_0>=COMMENT && LA1_0<=ID)||(LA1_0>=11 && LA1_0<=25)||(LA1_0>=30 && LA1_0<=34)) ) {
                    alt1=1;
                }


                switch (alt1) {
            	case 1 :
            	    // java/tools/src/grammar/Leros.g:75:8: statement
            	    {
            	    pushFollow(FOLLOW_statement_in_pass138);
            	    statement();

            	    state._fsp--;


            	    }
            	    break;

            	default :
            	    if ( cnt1 >= 1 ) break loop1;
                        EarlyExitException eee =
                            new EarlyExitException(1, input);
                        throw eee;
                }
                cnt1++;
            } while (true);


            }

        }
        catch (RecognitionException re) {
            reportError(re);
            recover(input,re);
        }
        finally {
        }
        return ;
    }
    // $ANTLR end "pass1"


    // $ANTLR start "dump"
    // java/tools/src/grammar/Leros.g:77:1: dump : ;
    public final void dump() throws RecognitionException {
        try {
            // java/tools/src/grammar/Leros.g:77:5: ()
            // java/tools/src/grammar/Leros.g:77:7: 
            {
            System.out.println(symbols);

            }

        }
        finally {
        }
        return ;
    }
    // $ANTLR end "dump"


    // $ANTLR start "pass2"
    // java/tools/src/grammar/Leros.g:80:1: pass2 returns [List mem] : ( statement )+ ;
    public final List pass2() throws RecognitionException {
        List mem = null;


        	System.out.println(pc+" "+symbols);
        	code = new int[pc];
        	pc = 0;
        	pass2 = true;

        try {
            // java/tools/src/grammar/Leros.g:87:2: ( ( statement )+ )
            // java/tools/src/grammar/Leros.g:87:4: ( statement )+
            {
            // java/tools/src/grammar/Leros.g:87:4: ( statement )+
            int cnt2=0;
            loop2:
            do {
                int alt2=2;
                int LA2_0 = input.LA(1);

                if ( ((LA2_0>=COMMENT && LA2_0<=ID)||(LA2_0>=11 && LA2_0<=25)||(LA2_0>=30 && LA2_0<=34)) ) {
                    alt2=1;
                }


                switch (alt2) {
            	case 1 :
            	    // java/tools/src/grammar/Leros.g:87:4: statement
            	    {
            	    pushFollow(FOLLOW_statement_in_pass264);
            	    statement();

            	    state._fsp--;


            	    }
            	    break;

            	default :
            	    if ( cnt2 >= 1 ) break loop2;
                        EarlyExitException eee =
                            new EarlyExitException(2, input);
                        throw eee;
                }
                cnt2++;
            } while (true);


            	mem = new ArrayList(pc);
            	for (int i=0; i<pc; ++i) {
            		mem.add(new Integer(code[i]));
            	}
            	

            }

        }
        catch (RecognitionException re) {
            reportError(re);
            recover(input,re);
        }
        finally {
        }
        return mem;
    }
    // $ANTLR end "pass2"


    // $ANTLR start "statement"
    // java/tools/src/grammar/Leros.g:94:1: statement : ( label )? ( directive | instruction )? ( COMMENT )? NEWLINE ;
    public final void statement() throws RecognitionException {
        try {
            // java/tools/src/grammar/Leros.g:94:10: ( ( label )? ( directive | instruction )? ( COMMENT )? NEWLINE )
            // java/tools/src/grammar/Leros.g:94:12: ( label )? ( directive | instruction )? ( COMMENT )? NEWLINE
            {
            // java/tools/src/grammar/Leros.g:94:12: ( label )?
            int alt3=2;
            int LA3_0 = input.LA(1);

            if ( (LA3_0==ID) ) {
                alt3=1;
            }
            switch (alt3) {
                case 1 :
                    // java/tools/src/grammar/Leros.g:94:13: label
                    {
                    pushFollow(FOLLOW_label_in_statement76);
                    label();

                    state._fsp--;


                    }
                    break;

            }

            // java/tools/src/grammar/Leros.g:94:21: ( directive | instruction )?
            int alt4=3;
            int LA4_0 = input.LA(1);

            if ( (LA4_0==11) ) {
                alt4=1;
            }
            else if ( ((LA4_0>=12 && LA4_0<=25)||(LA4_0>=30 && LA4_0<=34)) ) {
                alt4=2;
            }
            switch (alt4) {
                case 1 :
                    // java/tools/src/grammar/Leros.g:94:22: directive
                    {
                    pushFollow(FOLLOW_directive_in_statement81);
                    directive();

                    state._fsp--;


                    }
                    break;
                case 2 :
                    // java/tools/src/grammar/Leros.g:94:34: instruction
                    {
                    pushFollow(FOLLOW_instruction_in_statement85);
                    instruction();

                    state._fsp--;


                    }
                    break;

            }

            // java/tools/src/grammar/Leros.g:94:48: ( COMMENT )?
            int alt5=2;
            int LA5_0 = input.LA(1);

            if ( (LA5_0==COMMENT) ) {
                alt5=1;
            }
            switch (alt5) {
                case 1 :
                    // java/tools/src/grammar/Leros.g:94:49: COMMENT
                    {
                    match(input,COMMENT,FOLLOW_COMMENT_in_statement90); 

                    }
                    break;

            }

            match(input,NEWLINE,FOLLOW_NEWLINE_in_statement94); 

            }

        }
        catch (RecognitionException re) {
            reportError(re);
            recover(input,re);
        }
        finally {
        }
        return ;
    }
    // $ANTLR end "statement"


    // $ANTLR start "label"
    // java/tools/src/grammar/Leros.g:96:1: label : ID ':' ;
    public final void label() throws RecognitionException {
        Token ID1=null;

        try {
            // java/tools/src/grammar/Leros.g:96:6: ( ID ':' )
            // java/tools/src/grammar/Leros.g:96:9: ID ':'
            {
            ID1=(Token)match(input,ID,FOLLOW_ID_in_label102); 
            match(input,10,FOLLOW_10_in_label104); 
            symbols.put((ID1!=null?ID1.getText():null), new Integer(pc));

            }

        }
        catch (RecognitionException re) {
            reportError(re);
            recover(input,re);
        }
        finally {
        }
        return ;
    }
    // $ANTLR end "label"


    // $ANTLR start "directive"
    // java/tools/src/grammar/Leros.g:99:1: directive : '.start' ;
    public final void directive() throws RecognitionException {
        try {
            // java/tools/src/grammar/Leros.g:99:10: ( '.start' )
            // java/tools/src/grammar/Leros.g:99:12: '.start'
            {
            match(input,11,FOLLOW_11_in_directive114); 

            }

        }
        catch (RecognitionException re) {
            reportError(re);
            recover(input,re);
        }
        finally {
        }
        return ;
    }
    // $ANTLR end "directive"


    // $ANTLR start "instruction"
    // java/tools/src/grammar/Leros.g:101:1: instruction : instr ;
    public final void instruction() throws RecognitionException {
        int instr2 = 0;


        try {
            // java/tools/src/grammar/Leros.g:101:12: ( instr )
            // java/tools/src/grammar/Leros.g:101:14: instr
            {
            pushFollow(FOLLOW_instr_in_instruction121);
            instr2=instr();

            state._fsp--;


            		System.out.println(pc+" "+niceHex(instr2));
            		if (pass2) { code[pc] = instr2; }
            		++pc;
            	

            }

        }
        catch (RecognitionException re) {
            reportError(re);
            recover(input,re);
        }
        finally {
        }
        return ;
    }
    // $ANTLR end "instruction"


    // $ANTLR start "instr"
    // java/tools/src/grammar/Leros.g:109:1: instr returns [int opc] : ( simple | alu register | alu imm_val | branch | io imm_val | loadaddr register | memind );
    public final int instr() throws RecognitionException {
        int opc = 0;

        int simple3 = 0;

        int alu4 = 0;

        int register5 = 0;

        int alu6 = 0;

        int imm_val7 = 0;

        int branch8 = 0;

        int io9 = 0;

        int imm_val10 = 0;

        int loadaddr11 = 0;

        int register12 = 0;

        int memind13 = 0;


        try {
            // java/tools/src/grammar/Leros.g:109:25: ( simple | alu register | alu imm_val | branch | io imm_val | loadaddr register | memind )
            int alt6=7;
            alt6 = dfa6.predict(input);
            switch (alt6) {
                case 1 :
                    // java/tools/src/grammar/Leros.g:110:2: simple
                    {
                    pushFollow(FOLLOW_simple_in_instr138);
                    simple3=simple();

                    state._fsp--;

                    opc = simple3;

                    }
                    break;
                case 2 :
                    // java/tools/src/grammar/Leros.g:111:2: alu register
                    {
                    pushFollow(FOLLOW_alu_in_instr145);
                    alu4=alu();

                    state._fsp--;

                    pushFollow(FOLLOW_register_in_instr147);
                    register5=register();

                    state._fsp--;

                    opc = alu4 + register5;

                    }
                    break;
                case 3 :
                    // java/tools/src/grammar/Leros.g:112:2: alu imm_val
                    {
                    pushFollow(FOLLOW_alu_in_instr154);
                    alu6=alu();

                    state._fsp--;

                    pushFollow(FOLLOW_imm_val_in_instr156);
                    imm_val7=imm_val();

                    state._fsp--;

                    opc = alu6 + imm_val7 + 0x0100;

                    }
                    break;
                case 4 :
                    // java/tools/src/grammar/Leros.g:113:2: branch
                    {
                    pushFollow(FOLLOW_branch_in_instr163);
                    branch8=branch();

                    state._fsp--;

                    opc = branch8;

                    }
                    break;
                case 5 :
                    // java/tools/src/grammar/Leros.g:114:2: io imm_val
                    {
                    pushFollow(FOLLOW_io_in_instr170);
                    io9=io();

                    state._fsp--;

                    pushFollow(FOLLOW_imm_val_in_instr172);
                    imm_val10=imm_val();

                    state._fsp--;

                    opc = io9 + imm_val10;

                    }
                    break;
                case 6 :
                    // java/tools/src/grammar/Leros.g:115:2: loadaddr register
                    {
                    pushFollow(FOLLOW_loadaddr_in_instr179);
                    loadaddr11=loadaddr();

                    state._fsp--;

                    pushFollow(FOLLOW_register_in_instr181);
                    register12=register();

                    state._fsp--;

                    opc = loadaddr11 + register12;

                    }
                    break;
                case 7 :
                    // java/tools/src/grammar/Leros.g:116:2: memind
                    {
                    pushFollow(FOLLOW_memind_in_instr188);
                    memind13=memind();

                    state._fsp--;

                    opc = memind13;

                    }
                    break;

            }
        }
        catch (RecognitionException re) {
            reportError(re);
            recover(input,re);
        }
        finally {
        }
        return opc;
    }
    // $ANTLR end "instr"


    // $ANTLR start "simple"
    // java/tools/src/grammar/Leros.g:119:1: simple returns [int opc] : ( 'nop' | 'shr' );
    public final int simple() throws RecognitionException {
        int opc = 0;

        try {
            // java/tools/src/grammar/Leros.g:119:25: ( 'nop' | 'shr' )
            int alt7=2;
            int LA7_0 = input.LA(1);

            if ( (LA7_0==12) ) {
                alt7=1;
            }
            else if ( (LA7_0==13) ) {
                alt7=2;
            }
            else {
                NoViableAltException nvae =
                    new NoViableAltException("", 7, 0, input);

                throw nvae;
            }
            switch (alt7) {
                case 1 :
                    // java/tools/src/grammar/Leros.g:120:2: 'nop'
                    {
                    match(input,12,FOLLOW_12_in_simple203); 
                    opc = 0x0000;

                    }
                    break;
                case 2 :
                    // java/tools/src/grammar/Leros.g:121:2: 'shr'
                    {
                    match(input,13,FOLLOW_13_in_simple213); 
                    opc = 0x1000;

                    }
                    break;

            }
        }
        catch (RecognitionException re) {
            reportError(re);
            recover(input,re);
        }
        finally {
        }
        return opc;
    }
    // $ANTLR end "simple"


    // $ANTLR start "alu"
    // java/tools/src/grammar/Leros.g:124:1: alu returns [int value] : ( 'add' | 'sub' | 'load' | 'and' | 'or' | 'xor' | 'loadh' | 'store' | 'jal' );
    public final int alu() throws RecognitionException {
        int value = 0;

        try {
            // java/tools/src/grammar/Leros.g:124:24: ( 'add' | 'sub' | 'load' | 'and' | 'or' | 'xor' | 'loadh' | 'store' | 'jal' )
            int alt8=9;
            switch ( input.LA(1) ) {
            case 14:
                {
                alt8=1;
                }
                break;
            case 15:
                {
                alt8=2;
                }
                break;
            case 16:
                {
                alt8=3;
                }
                break;
            case 17:
                {
                alt8=4;
                }
                break;
            case 18:
                {
                alt8=5;
                }
                break;
            case 19:
                {
                alt8=6;
                }
                break;
            case 20:
                {
                alt8=7;
                }
                break;
            case 21:
                {
                alt8=8;
                }
                break;
            case 22:
                {
                alt8=9;
                }
                break;
            default:
                NoViableAltException nvae =
                    new NoViableAltException("", 8, 0, input);

                throw nvae;
            }

            switch (alt8) {
                case 1 :
                    // java/tools/src/grammar/Leros.g:125:2: 'add'
                    {
                    match(input,14,FOLLOW_14_in_alu233); 
                    value = 0x0800;

                    }
                    break;
                case 2 :
                    // java/tools/src/grammar/Leros.g:126:2: 'sub'
                    {
                    match(input,15,FOLLOW_15_in_alu243); 
                    value = 0x0c00;

                    }
                    break;
                case 3 :
                    // java/tools/src/grammar/Leros.g:127:2: 'load'
                    {
                    match(input,16,FOLLOW_16_in_alu253); 
                    value = 0x2000;

                    }
                    break;
                case 4 :
                    // java/tools/src/grammar/Leros.g:128:2: 'and'
                    {
                    match(input,17,FOLLOW_17_in_alu262); 
                    value = 0x2200;

                    }
                    break;
                case 5 :
                    // java/tools/src/grammar/Leros.g:129:2: 'or'
                    {
                    match(input,18,FOLLOW_18_in_alu272); 
                    value = 0x2400;

                    }
                    break;
                case 6 :
                    // java/tools/src/grammar/Leros.g:130:2: 'xor'
                    {
                    match(input,19,FOLLOW_19_in_alu283); 
                    value = 0x2600;

                    }
                    break;
                case 7 :
                    // java/tools/src/grammar/Leros.g:131:2: 'loadh'
                    {
                    match(input,20,FOLLOW_20_in_alu293); 
                    value = 0x2800;

                    }
                    break;
                case 8 :
                    // java/tools/src/grammar/Leros.g:132:2: 'store'
                    {
                    match(input,21,FOLLOW_21_in_alu301); 
                    value = 0x3000;

                    }
                    break;
                case 9 :
                    // java/tools/src/grammar/Leros.g:133:2: 'jal'
                    {
                    match(input,22,FOLLOW_22_in_alu310); 
                    value = 0x4000;

                    }
                    break;

            }
        }
        catch (RecognitionException re) {
            reportError(re);
            recover(input,re);
        }
        finally {
        }
        return value;
    }
    // $ANTLR end "alu"


    // $ANTLR start "io"
    // java/tools/src/grammar/Leros.g:136:1: io returns [int value] : ( 'out' | 'in' );
    public final int io() throws RecognitionException {
        int value = 0;

        try {
            // java/tools/src/grammar/Leros.g:136:23: ( 'out' | 'in' )
            int alt9=2;
            int LA9_0 = input.LA(1);

            if ( (LA9_0==23) ) {
                alt9=1;
            }
            else if ( (LA9_0==24) ) {
                alt9=2;
            }
            else {
                NoViableAltException nvae =
                    new NoViableAltException("", 9, 0, input);

                throw nvae;
            }
            switch (alt9) {
                case 1 :
                    // java/tools/src/grammar/Leros.g:137:2: 'out'
                    {
                    match(input,23,FOLLOW_23_in_io331); 
                    value = 0x3800;

                    }
                    break;
                case 2 :
                    // java/tools/src/grammar/Leros.g:138:2: 'in'
                    {
                    match(input,24,FOLLOW_24_in_io341); 
                    value = 0x3c00;

                    }
                    break;

            }
        }
        catch (RecognitionException re) {
            reportError(re);
            recover(input,re);
        }
        finally {
        }
        return value;
    }
    // $ANTLR end "io"


    // $ANTLR start "loadaddr"
    // java/tools/src/grammar/Leros.g:141:1: loadaddr returns [int value] : 'loadaddr' ;
    public final int loadaddr() throws RecognitionException {
        int value = 0;

        try {
            // java/tools/src/grammar/Leros.g:141:29: ( 'loadaddr' )
            // java/tools/src/grammar/Leros.g:142:2: 'loadaddr'
            {
            match(input,25,FOLLOW_25_in_loadaddr361); 
            value = 0x5000;

            }

        }
        catch (RecognitionException re) {
            reportError(re);
            recover(input,re);
        }
        finally {
        }
        return value;
    }
    // $ANTLR end "loadaddr"


    // $ANTLR start "memind"
    // java/tools/src/grammar/Leros.g:145:1: memind returns [int value] : ( 'load' '(' 'ar' '+' imm_val ')' | 'store' '(' 'ar' '+' imm_val ')' );
    public final int memind() throws RecognitionException {
        int value = 0;

        int imm_val14 = 0;

        int imm_val15 = 0;


        try {
            // java/tools/src/grammar/Leros.g:145:27: ( 'load' '(' 'ar' '+' imm_val ')' | 'store' '(' 'ar' '+' imm_val ')' )
            int alt10=2;
            int LA10_0 = input.LA(1);

            if ( (LA10_0==16) ) {
                alt10=1;
            }
            else if ( (LA10_0==21) ) {
                alt10=2;
            }
            else {
                NoViableAltException nvae =
                    new NoViableAltException("", 10, 0, input);

                throw nvae;
            }
            switch (alt10) {
                case 1 :
                    // java/tools/src/grammar/Leros.g:146:2: 'load' '(' 'ar' '+' imm_val ')'
                    {
                    match(input,16,FOLLOW_16_in_memind377); 
                    match(input,26,FOLLOW_26_in_memind379); 
                    match(input,27,FOLLOW_27_in_memind381); 
                    match(input,28,FOLLOW_28_in_memind383); 
                    pushFollow(FOLLOW_imm_val_in_memind385);
                    imm_val14=imm_val();

                    state._fsp--;

                    match(input,29,FOLLOW_29_in_memind387); 
                    value = 0x6000 + imm_val14;

                    }
                    break;
                case 2 :
                    // java/tools/src/grammar/Leros.g:147:2: 'store' '(' 'ar' '+' imm_val ')'
                    {
                    match(input,21,FOLLOW_21_in_memind394); 
                    match(input,26,FOLLOW_26_in_memind396); 
                    match(input,27,FOLLOW_27_in_memind398); 
                    match(input,28,FOLLOW_28_in_memind400); 
                    pushFollow(FOLLOW_imm_val_in_memind402);
                    imm_val15=imm_val();

                    state._fsp--;

                    match(input,29,FOLLOW_29_in_memind404); 
                    value = 0x7000 + imm_val15;

                    }
                    break;

            }
        }
        catch (RecognitionException re) {
            reportError(re);
            recover(input,re);
        }
        finally {
        }
        return value;
    }
    // $ANTLR end "memind"


    // $ANTLR start "branch"
    // java/tools/src/grammar/Leros.g:150:1: branch returns [int opc] : brinstr ID ;
    public final int branch() throws RecognitionException {
        int opc = 0;

        Token ID16=null;
        int brinstr17 = 0;


        try {
            // java/tools/src/grammar/Leros.g:150:25: ( brinstr ID )
            // java/tools/src/grammar/Leros.g:151:2: brinstr ID
            {
            pushFollow(FOLLOW_brinstr_in_branch420);
            brinstr17=brinstr();

            state._fsp--;

            ID16=(Token)match(input,ID,FOLLOW_ID_in_branch422); 

            		int off = 0;
            		if (pass2) {
            			Integer v = (Integer) symbols.get((ID16!=null?ID16.getText():null));
                    		if ( v!=null ) {
            				off = v.intValue();
            		        } else {
            				throw new Error("Undefined label "+(ID16!=null?ID16.getText():null));
            			}
            			off = off - pc;
            			// TODO test maximum offset
            			// at the moment 8 bits offset
            			off &= 0xff;
            		}
            		opc = brinstr17 + off;
            	

            }

        }
        catch (RecognitionException re) {
            reportError(re);
            recover(input,re);
        }
        finally {
        }
        return opc;
    }
    // $ANTLR end "branch"


    // $ANTLR start "brinstr"
    // java/tools/src/grammar/Leros.g:169:1: brinstr returns [int value] : ( 'branch' | 'brz' | 'brnz' | 'brp' | 'brn' );
    public final int brinstr() throws RecognitionException {
        int value = 0;

        try {
            // java/tools/src/grammar/Leros.g:169:28: ( 'branch' | 'brz' | 'brnz' | 'brp' | 'brn' )
            int alt11=5;
            switch ( input.LA(1) ) {
            case 30:
                {
                alt11=1;
                }
                break;
            case 31:
                {
                alt11=2;
                }
                break;
            case 32:
                {
                alt11=3;
                }
                break;
            case 33:
                {
                alt11=4;
                }
                break;
            case 34:
                {
                alt11=5;
                }
                break;
            default:
                NoViableAltException nvae =
                    new NoViableAltException("", 11, 0, input);

                throw nvae;
            }

            switch (alt11) {
                case 1 :
                    // java/tools/src/grammar/Leros.g:170:2: 'branch'
                    {
                    match(input,30,FOLLOW_30_in_brinstr437); 
                    value = 0x4800;

                    }
                    break;
                case 2 :
                    // java/tools/src/grammar/Leros.g:171:2: 'brz'
                    {
                    match(input,31,FOLLOW_31_in_brinstr444); 
                    value = 0x4900;

                    }
                    break;
                case 3 :
                    // java/tools/src/grammar/Leros.g:172:2: 'brnz'
                    {
                    match(input,32,FOLLOW_32_in_brinstr451); 
                    value = 0x4a00;

                    }
                    break;
                case 4 :
                    // java/tools/src/grammar/Leros.g:173:2: 'brp'
                    {
                    match(input,33,FOLLOW_33_in_brinstr458); 
                    value = 0x4b00;

                    }
                    break;
                case 5 :
                    // java/tools/src/grammar/Leros.g:174:2: 'brn'
                    {
                    match(input,34,FOLLOW_34_in_brinstr465); 
                    value = 0x4c00;

                    }
                    break;

            }
        }
        catch (RecognitionException re) {
            reportError(re);
            recover(input,re);
        }
        finally {
        }
        return value;
    }
    // $ANTLR end "brinstr"


    // $ANTLR start "register"
    // java/tools/src/grammar/Leros.g:178:1: register returns [int value] : REG ;
    public final int register() throws RecognitionException {
        int value = 0;

        Token REG18=null;

        try {
            // java/tools/src/grammar/Leros.g:178:29: ( REG )
            // java/tools/src/grammar/Leros.g:179:2: REG
            {
            REG18=(Token)match(input,REG,FOLLOW_REG_in_register482); 
            value = Integer.parseInt((REG18!=null?REG18.getText():null).substring(1));
            		if (value<0 || value>255) throw new Error("Wrong register name");

            }

        }
        catch (RecognitionException re) {
            reportError(re);
            recover(input,re);
        }
        finally {
        }
        return value;
    }
    // $ANTLR end "register"


    // $ANTLR start "imm_val"
    // java/tools/src/grammar/Leros.g:184:1: imm_val returns [int value] : ( INT | '-' INT | '<' ID | '>' ID );
    public final int imm_val() throws RecognitionException {
        int value = 0;

        Token INT19=null;
        Token INT20=null;
        Token ID21=null;
        Token ID22=null;

        try {
            // java/tools/src/grammar/Leros.g:184:28: ( INT | '-' INT | '<' ID | '>' ID )
            int alt12=4;
            switch ( input.LA(1) ) {
            case INT:
                {
                alt12=1;
                }
                break;
            case 35:
                {
                alt12=2;
                }
                break;
            case 36:
                {
                alt12=3;
                }
                break;
            case 37:
                {
                alt12=4;
                }
                break;
            default:
                NoViableAltException nvae =
                    new NoViableAltException("", 12, 0, input);

                throw nvae;
            }

            switch (alt12) {
                case 1 :
                    // java/tools/src/grammar/Leros.g:185:2: INT
                    {
                    INT19=(Token)match(input,INT,FOLLOW_INT_in_imm_val498); 
                    value = Integer.parseInt((INT19!=null?INT19.getText():null));
                    		if (value<-128 || value>255) throw new Error("Wrong immediate");

                    }
                    break;
                case 2 :
                    // java/tools/src/grammar/Leros.g:187:2: '-' INT
                    {
                    match(input,35,FOLLOW_35_in_imm_val505); 
                    INT20=(Token)match(input,INT,FOLLOW_INT_in_imm_val507); 
                    value = (-Integer.parseInt((INT20!=null?INT20.getText():null))) & 0xff;
                    		if (value<-128 || value>255) throw new Error("Wrong immediate");

                    }
                    break;
                case 3 :
                    // java/tools/src/grammar/Leros.g:189:2: '<' ID
                    {
                    match(input,36,FOLLOW_36_in_imm_val514); 
                    ID21=(Token)match(input,ID,FOLLOW_ID_in_imm_val516); 

                    		int val = 0;
                    		if (pass2) {
                    			Integer v = (Integer) symbols.get((ID21!=null?ID21.getText():null));
                            		if ( v!=null ) {
                    				val = v.intValue() & 0xff;
                    		        } else {
                    				throw new Error("Undefined label "+(ID21!=null?ID21.getText():null));
                    			}
                    		}
                    		value = val;
                    	

                    }
                    break;
                case 4 :
                    // java/tools/src/grammar/Leros.g:202:2: '>' ID
                    {
                    match(input,37,FOLLOW_37_in_imm_val524); 
                    ID22=(Token)match(input,ID,FOLLOW_ID_in_imm_val526); 

                    		int val = 0;
                    		if (pass2) {
                    			Integer v = (Integer) symbols.get((ID22!=null?ID22.getText():null));
                            		if ( v!=null ) {
                    				val = (v.intValue()>>8) & 0xff;
                    		        } else {
                    				throw new Error("Undefined label "+(ID22!=null?ID22.getText():null));
                    			}
                    		}
                    		value = val;
                    	

                    }
                    break;

            }
        }
        catch (RecognitionException re) {
            reportError(re);
            recover(input,re);
        }
        finally {
        }
        return value;
    }
    // $ANTLR end "imm_val"

    // Delegated rules


    protected DFA6 dfa6 = new DFA6(this);
    static final String DFA6_eotS =
        "\21\uffff";
    static final String DFA6_eofS =
        "\21\uffff";
    static final String DFA6_minS =
        "\1\14\1\uffff\11\7\6\uffff";
    static final String DFA6_maxS =
        "\1\42\1\uffff\11\45\6\uffff";
    static final String DFA6_acceptS =
        "\1\uffff\1\1\11\uffff\1\4\1\5\1\6\1\2\1\3\1\7";
    static final String DFA6_specialS =
        "\21\uffff}>";
    static final String[] DFA6_transitionS = {
            "\2\1\1\2\1\3\1\4\1\5\1\6\1\7\1\10\1\11\1\12\2\14\1\15\4\uffff"+
            "\5\13",
            "",
            "\1\16\1\17\32\uffff\3\17",
            "\1\16\1\17\32\uffff\3\17",
            "\1\16\1\17\21\uffff\1\20\10\uffff\3\17",
            "\1\16\1\17\32\uffff\3\17",
            "\1\16\1\17\32\uffff\3\17",
            "\1\16\1\17\32\uffff\3\17",
            "\1\16\1\17\32\uffff\3\17",
            "\1\16\1\17\21\uffff\1\20\10\uffff\3\17",
            "\1\16\1\17\32\uffff\3\17",
            "",
            "",
            "",
            "",
            "",
            ""
    };

    static final short[] DFA6_eot = DFA.unpackEncodedString(DFA6_eotS);
    static final short[] DFA6_eof = DFA.unpackEncodedString(DFA6_eofS);
    static final char[] DFA6_min = DFA.unpackEncodedStringToUnsignedChars(DFA6_minS);
    static final char[] DFA6_max = DFA.unpackEncodedStringToUnsignedChars(DFA6_maxS);
    static final short[] DFA6_accept = DFA.unpackEncodedString(DFA6_acceptS);
    static final short[] DFA6_special = DFA.unpackEncodedString(DFA6_specialS);
    static final short[][] DFA6_transition;

    static {
        int numStates = DFA6_transitionS.length;
        DFA6_transition = new short[numStates][];
        for (int i=0; i<numStates; i++) {
            DFA6_transition[i] = DFA.unpackEncodedString(DFA6_transitionS[i]);
        }
    }

    class DFA6 extends DFA {

        public DFA6(BaseRecognizer recognizer) {
            this.recognizer = recognizer;
            this.decisionNumber = 6;
            this.eot = DFA6_eot;
            this.eof = DFA6_eof;
            this.min = DFA6_min;
            this.max = DFA6_max;
            this.accept = DFA6_accept;
            this.special = DFA6_special;
            this.transition = DFA6_transition;
        }
        public String getDescription() {
            return "109:1: instr returns [int opc] : ( simple | alu register | alu imm_val | branch | io imm_val | loadaddr register | memind );";
        }
    }
 

    public static final BitSet FOLLOW_statement_in_pass138 = new BitSet(new long[]{0x00000007C3FFF872L});
    public static final BitSet FOLLOW_statement_in_pass264 = new BitSet(new long[]{0x00000007C3FFF872L});
    public static final BitSet FOLLOW_label_in_statement76 = new BitSet(new long[]{0x00000007C3FFF830L});
    public static final BitSet FOLLOW_directive_in_statement81 = new BitSet(new long[]{0x0000000000000030L});
    public static final BitSet FOLLOW_instruction_in_statement85 = new BitSet(new long[]{0x0000000000000030L});
    public static final BitSet FOLLOW_COMMENT_in_statement90 = new BitSet(new long[]{0x0000000000000020L});
    public static final BitSet FOLLOW_NEWLINE_in_statement94 = new BitSet(new long[]{0x0000000000000002L});
    public static final BitSet FOLLOW_ID_in_label102 = new BitSet(new long[]{0x0000000000000400L});
    public static final BitSet FOLLOW_10_in_label104 = new BitSet(new long[]{0x0000000000000002L});
    public static final BitSet FOLLOW_11_in_directive114 = new BitSet(new long[]{0x0000000000000002L});
    public static final BitSet FOLLOW_instr_in_instruction121 = new BitSet(new long[]{0x0000000000000002L});
    public static final BitSet FOLLOW_simple_in_instr138 = new BitSet(new long[]{0x0000000000000002L});
    public static final BitSet FOLLOW_alu_in_instr145 = new BitSet(new long[]{0x0000000000000080L});
    public static final BitSet FOLLOW_register_in_instr147 = new BitSet(new long[]{0x0000000000000002L});
    public static final BitSet FOLLOW_alu_in_instr154 = new BitSet(new long[]{0x0000003800000100L});
    public static final BitSet FOLLOW_imm_val_in_instr156 = new BitSet(new long[]{0x0000000000000002L});
    public static final BitSet FOLLOW_branch_in_instr163 = new BitSet(new long[]{0x0000000000000002L});
    public static final BitSet FOLLOW_io_in_instr170 = new BitSet(new long[]{0x0000003800000100L});
    public static final BitSet FOLLOW_imm_val_in_instr172 = new BitSet(new long[]{0x0000000000000002L});
    public static final BitSet FOLLOW_loadaddr_in_instr179 = new BitSet(new long[]{0x0000000000000080L});
    public static final BitSet FOLLOW_register_in_instr181 = new BitSet(new long[]{0x0000000000000002L});
    public static final BitSet FOLLOW_memind_in_instr188 = new BitSet(new long[]{0x0000000000000002L});
    public static final BitSet FOLLOW_12_in_simple203 = new BitSet(new long[]{0x0000000000000002L});
    public static final BitSet FOLLOW_13_in_simple213 = new BitSet(new long[]{0x0000000000000002L});
    public static final BitSet FOLLOW_14_in_alu233 = new BitSet(new long[]{0x0000000000000002L});
    public static final BitSet FOLLOW_15_in_alu243 = new BitSet(new long[]{0x0000000000000002L});
    public static final BitSet FOLLOW_16_in_alu253 = new BitSet(new long[]{0x0000000000000002L});
    public static final BitSet FOLLOW_17_in_alu262 = new BitSet(new long[]{0x0000000000000002L});
    public static final BitSet FOLLOW_18_in_alu272 = new BitSet(new long[]{0x0000000000000002L});
    public static final BitSet FOLLOW_19_in_alu283 = new BitSet(new long[]{0x0000000000000002L});
    public static final BitSet FOLLOW_20_in_alu293 = new BitSet(new long[]{0x0000000000000002L});
    public static final BitSet FOLLOW_21_in_alu301 = new BitSet(new long[]{0x0000000000000002L});
    public static final BitSet FOLLOW_22_in_alu310 = new BitSet(new long[]{0x0000000000000002L});
    public static final BitSet FOLLOW_23_in_io331 = new BitSet(new long[]{0x0000000000000002L});
    public static final BitSet FOLLOW_24_in_io341 = new BitSet(new long[]{0x0000000000000002L});
    public static final BitSet FOLLOW_25_in_loadaddr361 = new BitSet(new long[]{0x0000000000000002L});
    public static final BitSet FOLLOW_16_in_memind377 = new BitSet(new long[]{0x0000000004000000L});
    public static final BitSet FOLLOW_26_in_memind379 = new BitSet(new long[]{0x0000000008000000L});
    public static final BitSet FOLLOW_27_in_memind381 = new BitSet(new long[]{0x0000000010000000L});
    public static final BitSet FOLLOW_28_in_memind383 = new BitSet(new long[]{0x0000003800000100L});
    public static final BitSet FOLLOW_imm_val_in_memind385 = new BitSet(new long[]{0x0000000020000000L});
    public static final BitSet FOLLOW_29_in_memind387 = new BitSet(new long[]{0x0000000000000002L});
    public static final BitSet FOLLOW_21_in_memind394 = new BitSet(new long[]{0x0000000004000000L});
    public static final BitSet FOLLOW_26_in_memind396 = new BitSet(new long[]{0x0000000008000000L});
    public static final BitSet FOLLOW_27_in_memind398 = new BitSet(new long[]{0x0000000010000000L});
    public static final BitSet FOLLOW_28_in_memind400 = new BitSet(new long[]{0x0000003800000100L});
    public static final BitSet FOLLOW_imm_val_in_memind402 = new BitSet(new long[]{0x0000000020000000L});
    public static final BitSet FOLLOW_29_in_memind404 = new BitSet(new long[]{0x0000000000000002L});
    public static final BitSet FOLLOW_brinstr_in_branch420 = new BitSet(new long[]{0x0000000000000040L});
    public static final BitSet FOLLOW_ID_in_branch422 = new BitSet(new long[]{0x0000000000000002L});
    public static final BitSet FOLLOW_30_in_brinstr437 = new BitSet(new long[]{0x0000000000000002L});
    public static final BitSet FOLLOW_31_in_brinstr444 = new BitSet(new long[]{0x0000000000000002L});
    public static final BitSet FOLLOW_32_in_brinstr451 = new BitSet(new long[]{0x0000000000000002L});
    public static final BitSet FOLLOW_33_in_brinstr458 = new BitSet(new long[]{0x0000000000000002L});
    public static final BitSet FOLLOW_34_in_brinstr465 = new BitSet(new long[]{0x0000000000000002L});
    public static final BitSet FOLLOW_REG_in_register482 = new BitSet(new long[]{0x0000000000000002L});
    public static final BitSet FOLLOW_INT_in_imm_val498 = new BitSet(new long[]{0x0000000000000002L});
    public static final BitSet FOLLOW_35_in_imm_val505 = new BitSet(new long[]{0x0000000000000100L});
    public static final BitSet FOLLOW_INT_in_imm_val507 = new BitSet(new long[]{0x0000000000000002L});
    public static final BitSet FOLLOW_36_in_imm_val514 = new BitSet(new long[]{0x0000000000000040L});
    public static final BitSet FOLLOW_ID_in_imm_val516 = new BitSet(new long[]{0x0000000000000002L});
    public static final BitSet FOLLOW_37_in_imm_val524 = new BitSet(new long[]{0x0000000000000040L});
    public static final BitSet FOLLOW_ID_in_imm_val526 = new BitSet(new long[]{0x0000000000000002L});

}