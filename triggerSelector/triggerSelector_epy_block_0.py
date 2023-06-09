import numpy as np
from gnuradio import gr

class blk(gr.sync_block):

	def __init__(self, number_Of_Inputs = 3):  # only default arguments here
		gr.sync_block.__init__(
		self,
		name='Trigger selector',
		in_sig=[np.float32 for x in range(number_Of_Inputs+1)],
		out_sig=[np.float32]
		)
		
		self.currentInputIndex = 1
		self.previous = 0.0;
		self.number_Of_Inputs = number_Of_Inputs;

		

	def work(self, input_items, output_items):
		
		for i in range(len(input_items[0])):
			if(input_items[0][i] == 1.0 and self.previous == 0.0):
				
				if(self.currentInputIndex != self.number_Of_Inputs):
					self.currentInputIndex = self.currentInputIndex + 1
				else:
					self.currentInputIndex = 1

				output_items[0][i] = input_items[self.currentInputIndex][i]
				self.previous = 1.0
			elif(input_items[0][i] == 1.0 and self.previous == 1.0):
				output_items[0][i] = input_items[self.currentInputIndex][i]
				self.previous=1.0
			else:
				output_items[0][i] = input_items[self.currentInputIndex][i]
				self.previous=0.0

		return len(output_items[0])
	
	
