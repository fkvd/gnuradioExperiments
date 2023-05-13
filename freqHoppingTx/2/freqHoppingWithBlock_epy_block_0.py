import numpy as np
from gnuradio import gr
import timeit

class blk(gr.sync_block):
	""" Selector with time - This blocks choose next input after timeout occurs
	You can change number of parameters by editing default value of numInputs
	Note: This is not a time precise block
	"""

	def __init__(self, timeout=1):
	
		numInputs = 3	# You can change this parameter
		
		gr.sync_block.__init__(
			self,
			name='Selector with time',
			in_sig=[np.complex64 for x in range(numInputs)],
			out_sig=[np.complex64]
		)
		self.timeout = timeout
		self.numInputs = numInputs
		self.startTime = timeit.default_timer()
		self.currentIndex = 0

	def work(self, input_items, output_items):
		currentTime = timeit.default_timer()
		timeDiff = currentTime - self.startTime
		if timeDiff > self.timeout:
			self.currentIndex = (self.currentIndex + 1) % self.numInputs
			self.startTime = currentTime
		
		output_items[0][:] = input_items[self.currentIndex]
		
		return len(output_items[0])
	
