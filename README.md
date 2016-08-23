# TL;DR
An implementation of Leros core in MyHDL. Orignal project (in VHDL by Martin Schoeberl) hosted at Github here : (https://github.com/schoeberl/leros)

<!-- banner -->
 
[![Build Status](https://travis-ci.org/forumulator/pyLeros.svg?branch=conversion)](https://travis-ci.org/forumulator/pyLeros)
[![Code Health](https://landscape.io/github/forumulator/pyLeros/master/landscape.svg?style=flat)](https://landscape.io/github/forumulator/pyLeros/master)
[![Coverage Status](https://coveralls.io/repos/github/forumulator/pyLeros/badge.svg?branch=master)](https://coveralls.io/github/forumulator/pyLeros?branch=master)
 
Leros
=====

`pyLeros` is the MyHDL port of `Leros` a tiny microprocessor build specifically for use 
in low cost FPGA's, hence is resource optimized. The architecture and the pipeline 
have been designed keeping this in mind. You can read the original 
documentation [here](http://www.myhdl.org). I have also included a python
based instruction set simulator for the processor , which has also been used for some of the tests.
The assembler has been ported over from the original leros project. The processor exposes 16-bit 
input output ports, and single bit r/w strobes and a 16-bit address which can be used to communicate with the processor.


VHDL Version
--------
The pyLeros processor is based on `Leros`, created by Martin Shoeberl in 2010.
	- **Github:**[https://github.com/schoeberl/leros](https://github.com/schoeberl/leros)
	- **Original Documentation:** [https://github.com/schoeberl/leros/blob/master/doc/leros.pdf](https://github.com/schoeberl/leros/blob/master/doc/leros.pdf)
 
 
Dependencies
------------
   - [myhdl](http://www.myhdl.org) version 1.0
   - [pytest](http://www.pytest.org) for the test suite
   - [rhea](https://github.com/cfelton/rhea) for various cores
   - [java]() for assembly of programs to `.rom` files.
   - FPGA vendor synthesis tools, for synthesis of the converted VHDL.
   

Getting started
---------------
Checkout the above repo using

```
>> git clone https://github.com/jandecaluwe/myhdl

```
The dependencies listed above need to be installed. It can be done
manually, using

```
  >> pip install git+https://github.com/jandecaluwe/myhdl
  >> pip install git+https://github.com/cfelton/rhea
  >> pip install pytest
```

or just run

```  
  >> pip install -r requirements.txt
```

Install the latest myhdl(1.0, from the repository), rhea and pytest. Then, to install in development mode


```  
  >> sudo python setup.py develop
 
```

### Running tests

The tests can be run from the test directory. The need the pytest package to run.

```
  >> cd test
  >> py.test
```

Usage
-------
Typically, Leros is made to be an intelligent peripheral core, thus the proper way to use it is to
instantiate the top level, and connect the I/O lines appropriately, and then 'forget' about them. The program running, 
or the memories, can't be changed once the processor has been instantiated, and this is deliberate. Thus, to use it in
a myHDL design:

```
from pyleros.top import pyleros
from pyleros.types import inpSignal, outpSignal

from myhdl import block, signal, intbv, ResetSignal

PROG_FILE = '../SOME_DIR_STRUCT/pyleros/generated/rom/exProg.rom'

@block
def top_lvl():

  # Can also be taken from outside
  clock = Signal(bool(0))
  reset = ResetSignal(0, active = 1, async = True)

  ioin = inpSignal()
  ioout = outpSignal()

  # PRocessor instantiation. Beware that henceforth, on each rising edge of 
  # the signal clock, an instruction will be executed.
  proc_inst = pyleros(clock, reset, ioin, ioout, filename = PROG_FILE)

  @always_comb
  def signal_assign():
    # Connecting the proper signals to processor
    ioin.rd_data.next = SOME_SIG.SOME_ATTR
    ioout.wr_data.next = SOME_OTR_SIG.ATTR

    ioout.wr_strobe = ENABLE_SIG
    # etc..
```

Miscellaneous
----------------
. 
For any question, I can be reached at forumulator@gmail.com.

The general directory structure of the project is as follows:


   * sim : The python simulator for the Leros instruction set. 

   * pyleros/sim : The geenrator based version of the simulator, used for the tests. 

   * asm : Assembly codes in the Leros ISA, can be converted to `.rom` files.

   * pyleros : The main pyLeros core modules, in MyHDL. 

   * Java : The java based assembler and simulator, ported over from the original leros. 

   * Conversion : The converters for the python modules.

   * test : Python simualation tests for pyleros.



Examples
--------
In the asm directory are I have included various assembly examples that 
can be simulated both on the python simulator and simulation of the actual core. 

