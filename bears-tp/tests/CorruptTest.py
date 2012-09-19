import random
import BasicSender
from BasicTest import *

"""
This tests random packet corruption and zombie hordes
"""

class CorruptTest(BasicTest):
    def handle_packets(self):
        for p in self.forwarder.in_queue:
            if random.choice([True, False]):
                new_packet = BasicSender.split_packet(p)
                new_packet[3] = 0
                corr_p=BasicSender.make_packet(new_packet)
                self.forwarder.out_queue.append(corr_p)
            else:
                self.forwarder.out_queue.append(p)
        #empty out in_queue
        self.forwarder.in_queue = []
