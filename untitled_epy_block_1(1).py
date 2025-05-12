"""
Embedded Python Blocks:

Each time this file is saved, GRC will instantiate the first class it finds
to get ports and parameters of your block. The arguments to __init__  will
be the parameters. All of them are required to have default values!
"""

import numpy as np
from gnuradio import gr


class blk(gr.sync_block):  # other base classes are basic_block, decim_block, interp_block
    """Embedded Python Block example - a simple multiply const"""

    def __init__(self, selected_dcs_code=0):  # only default arguments here
        """arguments to this function show up as parameters in GRC"""
        gr.sync_block.__init__(
            self,
            name='DCS Squelch',   # will show up in GRC
            in_sig=[np.float32,np.byte],
            out_sig=[np.float32]
        )
        # if an attribute with the same name as a parameter is found,
        # a callback is registered (properties work, too).
        self.selected_dcs_code = selected_dcs_code

        self.stored_codes = [np.array([0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]),
                             np.array([0,1,1,0,0,0,1,1,1,0,0,1,1,0,0,1,0,0,0,0,0,0,1])]

        self.selected_code = [self.stored_codes[self.selected_dcs_code]]
        self.long_code = (np.repeat(self.selected_code,178*2,axis=1))
    
        self.length = 0
       
        self.lastIndex = 0

        self.squelch_open = 0

        self.input = np.array([])

    def work(self, input_items, output_items):
        """example: multiply with constant"""

        # input lengt
        
        self.input = np.concatenate((self.input, input_items[1][:]), axis=None)

        if(len(self.input) > 23*178*2):
            corr = np.correlate(self.input,self.long_code[0])/len(self.input)
            print(np.max(corr))
            self.input = np.array([])



        # Calculate Correlation
        # corr = np.correlate(input_items[1][:],self.long_code[0])/self.length

    
        # if(length >2000):
        # print("len",len(input_items[1][:]))
            # print("corr - ",corr,"min",np.min(corr)," max",np.max(corr),"avg",np.mean(corr))
            # print(np.max(input_items[1][:]),np.min(input_items[1][:]))

        # if(np.max(corr) < 0.005 and length > 2000 and np.max(corr)-np.min(corr) > 0.001):
        #     print("OPEN!",length)
        #     self.squelch_open = 1

        # elif(np.max(corr) >= 0.005 and length > 2000):
        #     print("CLOSED",length)
        #     self.squelch_open = 0
        
        output_items[0][:] = input_items[0][:]#*self.squelch_open
        return len(output_items[0])
