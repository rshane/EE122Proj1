import random
from time import sleep
from BasicTest import *

DELAY_TIME = 0.1

#This test delays every transmission by 100 ms... how rude.

class DelayTest(BasicTest):
    def handle_packet(self):
        for p in self.forwarder.in_queue:
            time.sleep(DELAY_TIME)
            self.forwarder.out_queue.append(p)
        self.forwarder.out_queue=[]
