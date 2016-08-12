

class LerosIO:


	UART_STATUS = 2
	UART_IO = 3
	LED = 0

	command = [10, 10, 30, 20, 1, 10]

	def __init__(self):
		self.commandIndex = 0


	def read(self, addr):

		ret = 0

		if addr == LerosIO.UART_STATUS:
			# 11111111
			ret = 255
			print(LerosIO.command[2])

		elif addr == LerosIO.UART_IO:

			ret = LerosIO.command[self.commandIndex]
			self.commandIndex += 1
			self.commandIndex %= len(LerosIO.command)

		else:
			raise IOError("Invalid IO Address " + hex(addr))

		return ret
			

	def write(self, addr, data):

		if addr == LerosIO.UART_IO:
			print(data)

		elif addr == LerosIO.LED:
			print( "LED = " + str(data) )

		else:
			raise IOError("Invalid IO Address " + hex(addr))
