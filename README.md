# TL;DR
An implementation of Leros core in MyHDL. Orignal project (in VHDL by Martin Schoeberl) hosted at Github here : (https://github.com/schoeberl/leros)

<!-- banner -->
 
 
Leros
=====

`pyLeros` is the MyHDL port of `Leros` a tiny microprocessor build specifically for use 
in low cost FPGA's, hence is resource optimized. The architecture and the pipeline 
have been designed keeping this in mind. You can read the original 
documentation [here](http://www.myhdl.org). I have also included a python
based instruction set simulator for the processor and an assembler. 


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
   

Miscellaneous
----------------

This code/package is licensed under the MIT license, which allows for 
free and full use of the code without limitations. 
For any question, I can be reached at forumulator@gmail.com.

The general directory structure of the project is as follows:


   * sim : The python simulator for the Leros instruction set. 

   * asm : Python based assembler and linker for the Leros instruction set. 

   * pyLeros : The main pyLeros core, in MyHDL. 

   * docs : Documentation for the project, in Sphinx 

   * examples: Some examples of successfully simulated programs.



Examples
--------
In the example directory are I have included various assembly examples that 
can be simulated both on the python simulator and simulation of the actual core. 

