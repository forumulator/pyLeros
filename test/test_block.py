from myhdl import *
from rhea.utils.test import run_testbench


@block
def block1(clk, reset, a, b):

	# combinatorial
	@always_seq(clk.posedge, reset=reset)
	def block1_func():

		b.next = a + 1

	return instances()



@block
def fedblock(clk, reset, c, d):

	a = Signal(int(0))
	b = Signal(int(0))

	inst = block1(clk, reset, a, b)

	@always_comb
	def conn():
		raise Exception
		a.next = c + 1
		
	@always_seq(clk.posedge, reset=reset)
	def out():
		c.next = int(c + 1)
		d.next = b + 1

	return instances()

# Note: using n always_seq blocks will require 
# a modified clock with 1/n th of the frequency

@block
def main():

	clk = Signal(bool(0))
	clk2 = Signal(bool(0))
	reset = ResetSignal(0, active=1, async=True)
	c = 0
	d = 0

	@always(delay(10))
	def tbclk():
		clk.next = not clk

	@always(clk.posedge)
	def tbclk2():
		clk2.next = not clk2

	instfed = fedblock(clk, reset, c, d)

	@instance
	def functest():

		c = 0
		yield clk.posedge

		for i in range(10):

			c = i + 1

			yield clk.posedge
			yield delay(1)

			assert d == i + 3

		raise StopSimulation

	return instances()

	




#This works currently
@block
def fedblock1(clk, reset, d):

	a = Signal(int(0))
	b = Signal(int(0))
	c = Signal(int(0))

	inst = block1(clk, reset, a, b)

	@always_comb
	def conn():
		a.next = c + 1
		
	@always_seq(clk.posedge, reset=reset)
	def out():
		c.next = int(c + 1)
		d.next = b + 1

	return instances()

# Note: using n always_seq blocks will require 
# a modified clock with 1/n th of the frequency

@block
def main1():

	clk = Signal(bool(0))
	clk2 = Signal(bool(0))
	reset = ResetSignal(0, active=1, async=True)
	# c = Signal(int(0))
	d = Signal(int(0))

	@always(delay(10))
	def tbclk():
		clk.next = not clk

	@always(clk.posedge)
	def tbclk2():
		clk2.next = not clk2

	instfed = fedblock1(clk, reset, d)

	@instance
	def functest():

		yield clk.posedge

		for i in range(10):

			yield clk.posedge
			yield delay(1)

			assert d == i + 3

		raise StopSimulation

	return instances()



def test_set_val_from_external():
	top_inst = main()
	top_inst.run_sim()


def test_set_value_in_instance():
	inst_block = main1()
	inst_block.run_sim()